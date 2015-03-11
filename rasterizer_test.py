import gdal, ogr
from gdalconst import *
import osr

in_file = 'test_out.tif'
out_file = 'test_4326.tif'
country_shp = r"C:\Users\Owner\Downloads\full_us-2015-03-03\full_us\states.shp"
# country_shp = '54cbd05be4b01fabb3001d53.shp'

# Open the input dataset.
ds_in = gdal.Open(in_file)

# Open the vector dataset.
ds_vector = ogr.Open(country_shp)
lyr = ds_vector.GetLayer()

# Create a dataset to write to.
ds_out = gdal.GetDriverByName("GTiff").Create(out_file,
                                              ds_in.RasterXSize,
                                              ds_in.RasterYSize,
                                              1, gdal.GDT_Int32)
ds_out.SetProjection(ds_in.GetProjection())
ds_out.SetGeoTransform(ds_in.GetGeoTransform())


# add_out = gdal.Open(out_file, GA_Update)

# Rasterize.
gdal.RasterizeLayer(ds_out, [1], lyr, burn_values=[1], options=['ALL_TOUCHED=TRUE'])
# gdal.RasterizeLayer(add_out, [1], lyr, burn_values=[1], options=['ALL_TOUCHED=TRUE', 'MERGE_ALG=ADD'])

in_file = None
out_file = None
country_shp = None
add_out = None