import ogr
import csv
import osr
import os

csv_path = "ScienceBaseResults.csv"


class Point:

    def __init__(self, x, y):
        self.x = x  # Longitude of point
        self.y = y  # Latitude of point


def construct_box(max_x, min_x, max_y, min_y, id):
    pt1 = Point(min_x, max_y)  # Top left
    pt2 = Point(max_x, max_y)  # Top right
    pt3 = Point(max_x, min_y)  # Bottom right
    pt4 = Point(min_x, min_y)  # Bottom left

    return [pt1, pt2, pt3, pt4, id]


def make_poly(bbox):
    extent = ogr.Geometry(ogr.wkbLinearRing)
    extent.AddPoint(bbox[0].x, bbox[0].y)
    extent.AddPoint(bbox[1].x, bbox[1].y)
    extent.AddPoint(bbox[2].x, bbox[2].y)
    extent.AddPoint(bbox[3].x, bbox[3].y)
    extent.AddPoint(bbox[0].x, bbox[0].y)

    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(extent)
    return polygon

def create_shapefile(polygon, id):


    id_path = str(id)+'.shp'
    print id_path

    driver = ogr.GetDriverByName("Esri Shapefile")

    source = driver.CreateDataSource(id_path)


    sr = osr.SpatialReference()
    sr.ImportFromEPSG(4326)

    layer = source.CreateLayer('bbox', sr, ogr.wkbPolygon)
    id_field = ogr.FieldDefn("ID", ogr.OFTString)
    id_field.SetWidth(25)
    layer.CreateField(id_field)

    feature = ogr.Feature(layer.GetLayerDefn())

    feature.SetGeometry(polygon)
    layer.CreateFeature(feature)


    feature.Destroy()
    source.Destroy()

def read_csv(my_csv):

    with open(my_csv, 'rb') as data:
        reader = csv.DictReader(data)
        for row in reader:
            max_x = float(row['spatial.boundingBox.maxX'])
            min_x = float(row['spatial.boundingBox.minX'])
            max_y = float(row['spatial.boundingBox.maxY'])
            min_y = float(row['spatial.boundingBox.minY'])
            id = row['id']
            bbox = construct_box(max_x, min_x, max_y, min_y, id)

            polygon = make_poly(bbox)
            create_shapefile(polygon, id)



read_csv(csv_path)