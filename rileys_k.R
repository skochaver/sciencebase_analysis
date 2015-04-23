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
  uni_points <- readOGR(getwd(), "CollegesUniversities")
  research_intensity <- readOGR(getwd(), "albers_10km_majorityresample_nonzero") # Point data will be easier
  
# Tests to view projection, metadata and plots
  #print(proj4string(research_intensity)) # Report the projection information as string
  #print(proj4string(uni_points))
  #ogrInfo(".", "CollegesUniversities") # Report info about dataset
  #plot(research_intensity, pch=20, cex=0.8)
  #plot(uni_points, pch=20, cex=0.8)
  
# Interate over all research instances from unique values in GRID_CODE
  unique_i <- unique(research_intensity$GRID_CODE)  # Figure out the unique values for GRID_CODE
  for (i in unique_i) {
    # Transform each dataframe into an R ppp point pattern object.
      uni_points_ppp <- as.ppp(uni_points)
      research_subset <- subset(research_intensity, GRID_CODE==i)
      research_intensity_ppp <- as.ppp(research_subset)
    
    # Combine university point and research instance data
      # Remove unesscessary marks, adding only the marks we need
        uni <- setmarks(unmark(uni_points_ppp), -1)
        research <- setmarks(unmark(research_intensity_ppp), research_intensity_ppp$marks$GRID_CODE)
      # Combine the two datasets
        #all <- superimpose(university=uni, instensity=research, W="convex")  # Is convex window ok? It avoids the error where 5 points are rejected for lying outside the specified window.
        all <- superimpose(uni, research, W="convex")
        all_cut <- cut(all, breaks=c(-2,0,333), labels=c("university","instensity"))
      
    # Run Riley's K between univeristy point and resarch instance data. Loop through each instance value.
      K <- Kcross(all_cut)
      #Kest <- Kest(all_cut, 20000)  # An r of 20000m is chosen to prespresent 20km or twice the minimum distance between points
    
    # Print out report for each Riley's K
      write.table(K, file = paste("K_subset_", i, ".csv"), sep = ",", row.names = FALSE)  # Ouput csv file containing result of Kest to working directory
    
    # Plot each K Statstic output on same axis.
      png(paste("K_subset_plot", i, ".png"), width=6, height = 6, units="in", res=600)  # Output png to working directory
      plot(K)
      dev.off()  # Need this to finish output
      
    # Smooth across newly created 3d plane.
  }
