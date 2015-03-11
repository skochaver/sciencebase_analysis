import ogr
import gdal
from gdalconst import *

gdal.UseExceptions()

def template_raster(base_raster_path, out_raster, data_type=gdal.GDT_Int32, no_data=-1):
    base_raster = gdal.Open(base_raster_path)

    cols = base_raster.RasterXSize
    rows = base_raster.RasterYSize
    projection = base_raster.GetProjection()
    geotransform = base_raster.GetGeoTransform()
    # bands = base_raster.RasterCount
    bands = 1

    driver = gdal.GetDriverByName("GTIFF")
    new_raster = driver.Create(out_raster, cols, rows, bands, data_type)
    new_raster.SetProjection(projection)
    new_raster.SetGeoTransform(geotransform)

    for i in range(bands):
        new_raster.GetRasterBand(i + 1).SetNoDataValue(no_data)  # Change these zeros if there is important data in base data or params
        new_raster.GetRasterBand(i + 1).Fill(no_data)   # Change these zeros if there is important data in base data or params

    return new_raster

def add_to_raster(base_raster, shape_file):

    vector = ogr.Open(shape_file)
    layer = vector.GetLayer()
    add_out = gdal.Open(base_raster, GA_Update)

    gdal.RasterizeLayer(add_out, [1], layer, burn_values=[1], options=['ALL_TOUCHED=TRUE', 'MERGE_ALG=ADD'])
    vector = None
    add_out = None

    return

def create_out_tiff(in_file, out_file, initial_shp):

    in_source = gdal.Open(in_file)
    out_source = gdal.GetDriverByName("GTiff").Create(out_file, in_source.RasterXSize, in_source.RasterYSize, 1, gdal.GDT_Int32)

    out_source.SetProjection(in_source.GetProjection())
    out_source.SetGeoTransform(in_source.GetGeoTransform())

    vector_source = ogr.Open(initial_shp)
    layer = vector_source.GetLayer()

    gdal.RasterizeLayer(out_source, [1], layer, burn_values=[0], options=['ALL_TOUCHED=TRUE'])

    in_source = None
    out_source = None
    vector_source = None
    return

def burn_without_add(in_raster, in_shape):

    shape_source = ogr.Open(in_shape)
    layer = shape_source.GetLayer()

    raster_source = gdal.Open(in_raster, GA_Update)

    gdal.RasterizeLayer(raster_source, [1], layer, burn_values=[1], options=['ALL_TOUCHED=TRUE'])

    shape_source = None
    raster_source = None
    return

country_shp = r"C:\Users\Owner\Downloads\full_us-2015-03-03\full_us\states.shp"
base_path = r"C:\Users\Owner\Downloads\full_us-2015-03-03\full_us\us_1km_raster.tif"
template_path = 'test_4326.tif'
shape_file = '54cbd05be4b01fabb3001d53.shp'
test = 'test_4326.tif'

burn_without_add(test, shape_file)