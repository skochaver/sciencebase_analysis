# Load necessary packages
install.packages("spatstat")
library("spatstat")
install.packages("rgdal")
library("rgdal") # Need this to import shapefiles

# Set working directory
# setwd("/home/ygritte/Classes/GEOG_578/project_data/")
setwd("c:/Users/student/Downloads/project_data/")
# setwd("c:/path/to/steves/inferior/windows/working/directory/")


### Read in raster or *point* shape file with research intensity data.
researchIntensity <- readOGR(".","research_frequency_points") # Point data will be easier
#print(proj4string(UniPoints)) # Report the projection information as string
#plot(researchIntensity, pch=20, cex=0.8)

### Read in raster or point shape file with university locations.
#ogrInfo(".", "CollegesUniversities") # Report info about dataset
UniPoints <- readOGR(".","CollegesUniversities")
#print(proj4string(UniPoints)) # Report the projection information as string
#plot(UniPoints, pch=20, cex=0.8)

# Transform data into dataframe with fields latitude, longitude, and # of resarch instances

# Separate dataframes into subsets. Each value of # of research instances.

# Transform each dataframe into an R ppp point pattern object.
uni_points <- as.ppp(UniPoints)
uni_points <- as(UniPoints, "ppp")

# (Might need to combine university point and resarch instance data)

# Run Riley's K between univeristy point and resarch instance data. Loop through each instance value.
# (k <- Kest(point.locations))

# Print out report for each Riley's K

# Plot each K Statstic output on same axis.

# Smooth across newly created 3d plane.