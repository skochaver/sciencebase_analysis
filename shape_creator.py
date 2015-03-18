import ogr
import csv
import osr
import os

__author__ = 'Steve Kochaver'

class Point:
    '''
    This is just a class to wrap latitudes and longitudes into a point. To be entirely honest the only reason this
    exists is because I think it's cool to call my geometries with .x and .y as attributes on an object.
    Also maybe something about organization or good practice.
    '''

    def __init__(self, x, y):
        self.x = x  # Longitude of point
        self.y = y  # Latitude of point


def construct_box(max_x, min_x, max_y, min_y, id):
    '''
    This function takes four values as decimal degrees and turns them into a list of point objects that define
    a bounding box. Also includes the id of the box at the end of the list. Assumes coordinate values are in EPSG:4326
    :param max_x: The maximum longitude of the bounding box.
    :param min_x: The minimum longitude of the bounding box.
    :param max_y: The maximum latitude of the bounding box.
    :param min_y: The minimum longitude of the bounding box.
    :param id: The string identifier of the bounding box.
    :return: Returns a list of my silly little point objects and the ID.
    '''
    pt1 = Point(min_x, max_y)  # Top left
    pt2 = Point(max_x, max_y)  # Top right
    pt3 = Point(max_x, min_y)  # Bottom right
    pt4 = Point(min_x, min_y)  # Bottom left

    return [pt1, pt2, pt3, pt4, id]


def make_poly(bbox):
    '''
    Takes a list of my custom point objects and creates a polygon of the bounding box they describe.
    :param bbox: This is a list of the points and the ID of the bbox.
    :return: Returns a well known binary polygon object.
    '''
    extent = ogr.Geometry(ogr.wkbLinearRing)
    extent.AddPoint(bbox[0].x, bbox[0].y)
    extent.AddPoint(bbox[1].x, bbox[1].y)
    extent.AddPoint(bbox[2].x, bbox[2].y)
    extent.AddPoint(bbox[3].x, bbox[3].y)
    # The first point is referenced twice to "complete" the ring.
    extent.AddPoint(bbox[0].x, bbox[0].y)

    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(extent)
    return polygon

def create_shapefile(polygon, id):
    '''
    Given a polygon and an ID this function will create a .shp polygon shapefile with the ID as the file name in the
    current working directory.
    :param polygon: A well known binary polygon object.
    :param id: The identifying string for the polygon to be the file name.
    :return: Assumes you know what you're doing in creating the file and doesn't return anything.
    '''
    id_path = os.path.join(os.getcwd(), 'shape_outputs', str(id)+'.shp')

    driver = ogr.GetDriverByName("Esri Shapefile")

    source = driver.CreateDataSource(id_path)

    sr = osr.SpatialReference()
    sr.ImportFromEPSG(4326)

    layer = source.CreateLayer('bbox', sr, ogr.wkbPolygon)
    # id_field = ogr.FieldDefn("ID", ogr.OFTString)
    # id_field.SetWidth(25)
    constant_field = ogr.FieldDefn("Constant", ogr.OFTInteger)
    constant_field.SetWidth(2)

    # layer.CreateField(id_field)
    layer.CreateField(constant_field)

    feature = ogr.Feature(layer.GetLayerDefn())

    feature.SetGeometry(polygon)
    # feature.SetField(0, id)
    feature.SetField(0, 1)
    layer.CreateFeature(feature)

    feature.Destroy()
    source.Destroy()

    return


def read_csv(my_csv):
    '''
    This is specific to the ScienceBase csv filetype query result. Takes the bounding box info and ID from each
    record for glorious GIS processing.
    :param my_csv: The path to the CSV file in question.
    :return: This is basically a runner function, and won't give you anything except the outputs on disk from create_shapefile.
    '''

    with open(my_csv, 'rb') as data:
        reader = csv.DictReader(data)
        for row in reader:
            if row['spatial.boundingBox.maxX']:
                max_x = float(row['spatial.boundingBox.maxX'])
                min_x = float(row['spatial.boundingBox.minX'])
                max_y = float(row['spatial.boundingBox.maxY'])
                min_y = float(row['spatial.boundingBox.minY'])
                id = row['id']
                print id
                bbox = construct_box(max_x, min_x, max_y, min_y, id)

                polygon = make_poly(bbox)
                create_shapefile(polygon, id)
    return
