# Load necessary packages
  install.packages("spatstat")
  library("spatstat")
  install.packages("rgdal")
  library("rgdal")  # Need this to import shapefiles
  install.packages("maptools")
  library("maptools")  # Need this because it contains the as() coercion functions

# Set working directory
  #setwd("/home/ygritte/Classes/GEOG_578/project_data/")
  setwd("c:/Users/student/Downloads/project_data/")
  #setwd("c:/path/to/steves/working/directory/")

# Read in point shape files for research intensity and university location data
  research_intensity <- readOGR(".", "research_frequency_points") # Point data will be easier
  uni_points <- readOGR(getwd(), "CollegesUniversities")


# Tests to view projection, metadata and plots
  #print(proj4string(research_intensity)) # Report the projection information as string
  #print(proj4string(uni_points))
  #ogrInfo(".", "CollegesUniversities") # Report info about dataset
  #plot(research_intensity, pch=20, cex=0.8)
  #plot(uni_points, pch=20, cex=0.8)


# Transform data into dataframe with fields latitude, longitude, and # of resarch instances

# Separate dataframes into subsets. Each value of # of research instances.

# Transform each dataframe into an R ppp point pattern object.
  uni_points_ppp <- as.ppp(uni_points)
  research_intensity_ppp <- as.ppp(research_intensity)

# Combine university point and research instance data
  # Remove unesscessary marks, adding only the marks we need
    uni <- setmarks(unmark(uni_points_ppp), -1)
    research <- setmarks(unmark(research_intensity_ppp), research_intensity_ppp$marks$GRID_CODE)
  # Combine the two datasets
    #all <- superimpose(university=uni, instensity=research, W="convex")  # Is convex window ok? It avoids the error where 5 points are rejected for lying outside the specified window.
    all <- superimpose(uni, research, W="convex")
    all_cut <- cut(all, breaks=c(-1,0,332), labels=c("university","instensity"))
  
# Run Riley's K between univeristy point and resarch instance data. Loop through each instance value.
  #(k <- Kest(point.locations))
  K <- linearKcross.inhom(all_cut, all_cut$marks=="university", all_cut$marks=="intensity")

# Print out report for each Riley's K

# Plot each K Statstic output on same axis.

# Smooth across newly created 3d plane.