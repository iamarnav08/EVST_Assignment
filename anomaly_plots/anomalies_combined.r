# -----------------------------
# Combined RWL Analysis with War & Famine Shading
# -----------------------------
library(dplR)

# ---- User inputs ----
input_dir <- "/home/arnavsharma/Arnav/UG_3.1/EST/Assignment/ethiopia_all_years/measurements/africa/"
output_dir <- "/home/arnavsharma/Arnav/UG_3.1/EST/Assignment/anomaly_plots/"
famine_csv <- "/home/arnavsharma/Arnav/UG_3.1/EST/Assignment/famine.csv"
war_csv <- "/home/arnavsharma/Arnav/UG_3.1/EST/Assignment/war.csv"

# Create output folder if not exists
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# ---- Helper: parse year or year ranges ----
parse_year_range <- function(year_str) {
  year_str <- trimws(year_str)
  year_str <- gsub("[–—]", "-", year_str)  # normalize dash
  if (grepl("-", year_str)) {
    parts <- strsplit(year_str, "-")[[1]]
    start <- as.numeric(parts[1])
    end <- as.numeric(parts[2])
  } else {
    start <- as.numeric(year_str)
    end <- as.numeric(year_str)
  }
  return(c(start, end))
}

# ---- Load famine and war periods ----
famine_df <- read.csv(famine_csv, stringsAsFactors = FALSE)
war_df <- read.csv(war_csv, stringsAsFactors = FALSE)

famine_periods <- t(sapply(famine_df$Year, parse_year_range))
colnames(famine_periods) <- c("start", "end")

war_periods <- t(sapply(war_df$Year, parse_year_range))
colnames(war_periods) <- c("start", "end")

# ---- Process all RWL files together ----
files <- list.files(input_dir, pattern="\\.rwl$", full.names=TRUE)

chron_list <- list()

for (f in files) {
  rwl <- read.rwl(f)
  ch <- chron(rwl)
  
  years <- as.numeric(rownames(ch))
  z_index <- scale(ch[,1])
  
  # Keep only years >= 1950
  mask <- years >= 1950
  years <- years[mask]
  z_index <- z_index[mask]
  
  chron_list[[basename(f)]] <- data.frame(year=years, z=z_index)
  cat("Processed:", basename(f), "\n")
}

# ---- Combine chronologies ----
all_years <- 1950:max(sapply(chron_list, function(df) max(df$year, na.rm=TRUE)))
combined <- data.frame(year=all_years)

# Merge each chronology by year
for (name in names(chron_list)) {
  combined <- merge(combined, chron_list[[name]], by="year", all.x=TRUE, suffixes=c("", paste0("_", name)))
  colnames(combined)[ncol(combined)] <- name
}

# Compute mean z-score across all files (row-wise mean, ignoring NAs)
combined$mean_z <- rowMeans(combined[,-1], na.rm=TRUE)

# ---- Plot combined chronology ----
png(filename=paste0(output_dir, "combined_chronology.png"),
    width=1200, height=500)

plot(combined$year, combined$mean_z, type="l", col="blue", lwd=2,
     xlab="Year (CE)", ylab="Standardized Growth (z-score)",
     main="Combined Tree-Ring Growth with War & Famine Shading")

abline(h=0, lty=2)

# Shade famine years
for (i in 1:nrow(famine_periods)) {
  start <- famine_periods[i,"start"]
  end <- famine_periods[i,"end"]
  if (end >= 1950) {
    rect(xleft=start, ybottom=par("usr")[3],
         xright=end, ytop=par("usr")[4],
         col=rgb(1, 0.6, 0, 0.3), border=NA)
  }
}

# Shade war years
for (i in 1:nrow(war_periods)) {
  start <- war_periods[i,"start"]
  end <- war_periods[i,"end"]
  if (end >= 1950) {
    rect(xleft=start, ybottom=par("usr")[3],
         xright=end, ytop=par("usr")[4],
         col=rgb(1, 0, 0, 0.3), border=NA)
  }
}

# Replot line on top
lines(combined$year, combined$mean_z, col="blue", lwd=2)

legend("topright", legend=c("Combined z-score index", "Famine", "War"),
       col=c("blue", rgb(1,0.6,0,0.5), rgb(1,0,0,0.5)),
       pch=c(NA, 15, 15), lty=c(1, NA, NA), lwd=c(2, NA, NA), bty="n")

dev.off()

cat("\nSaved combined chronology plot ->", paste0(output_dir, "combined_chronology.png"), "\n")
