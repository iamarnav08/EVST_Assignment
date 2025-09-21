# ---------------------------
# Tree-ring RWL Plotter
# ---------------------------
# Requirements: install dplR once via:
# install.packages("dplR")

library(dplR)

# ---- User inputs ----
# Choose your .rwl file (change the path or use file.choose())
rwl_file <- file.choose()   # Opens a dialog box to pick your file

# Choose the year range
min_year <- 1980
max_year <- 1987

# ---- Read the RWL file ----
rwl <- read.rwl(rwl_file)

# ---- Subset data for chosen years ----
subset_data <- rwl[rownames(rwl) %in% min_year:max_year, ]

# Keep only columns (trees) with no missing values in that range
valid_trees <- colnames(subset_data)[colSums(is.na(subset_data)) == 0]
selected <- subset_data[, valid_trees, drop=FALSE]

# Convert row names (years) to numeric
years <- as.numeric(rownames(selected))

# ---- Plot setup ----
plot(range(years), range(selected, na.rm=TRUE), type="n",
     xlab="Year", ylab="Ring Width",
     main=paste("Tree-ring Widths", min_year, "-", max_year))

# ---- Plot each tree with green/red segments ----
for (tree in colnames(selected)) {
  values <- selected[, tree]
  
  for (i in 1:(length(years)-1)) {
    year_pair <- years[i:(i+1)]
    value_pair <- values[i:(i+1)]
    
    col <- ifelse(value_pair[2] > value_pair[1], "green", "red")
    lines(year_pair, value_pair, col=col, lwd=2)
  }
}

# ---- Legend ----
legend("topright", legend=c("Increase", "Decrease"),
       col=c("green","red"), lty=1, lwd=2)

