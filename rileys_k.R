# Load necessary packages
install.packages("spatstat")
library("spatstat")
library("rgdal") # Need this to import shapefiles

# Set working directory
setwd("/home/ygritte/Classes/GEOG_578/project_data/")
# setwd("c:/path/to/steves/inferior/windows/working/directory/")

# Read in raster or point shape file with research intensity data.
#researchIntensity <- readShapePoints("research_frequency_points.shp") # Point data will be easier

# Read in raster or point shape file with university locations.
ogrInfo(".", "CollegesUniversities.shp") # Report info about dataset

# Transform data into dataframe with fields latitude, longitude, and # of resarch instances

# Separate dataframes into subsets. Each value of # of research instances.

# Transform each dataframe into an R ppp point pattern object.

# (Might need to combine university point and resarch instance data)

# Run Riley's K between univeristy point and resarch instance data. Loop through each instance value.
# (k <- Kest(point.locations))

# Print out report for each Riley's K

# Plot each K Statstic output on same axis.

# Smooth across newly created 3d plane.