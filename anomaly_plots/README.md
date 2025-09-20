Methodology for Tree-Ring Chronology Analysis
Data Processing Pipeline
The analysis follows a standardized dendrochronological approach to combine multiple tree-ring measurement files into a unified chronology for examining growth anomalies in relation to historical events.

1. Data Input and Preparation
Ring Width Measurement Files (.rwl): The analysis processes multiple RWL (Ring Width Library) files from the Ethiopian region, located in the Africa measurements directory. Each file contains raw ring width measurements from multiple tree cores or trees.

Historical Event Data: Two CSV files containing famine and war periods are loaded, with years specified either as single years or year ranges (e.g., "1983-1985").

2. Individual Chronology Development
For each RWL file, the following steps are performed:

a) Raw Data Loading: Ring width measurements are read using the dplR package's read.rwl() function.

b) Chronology Construction: The chron() function processes the raw measurements by:

Averaging ring width values across all samples/trees within each file for each year
Applying standardization techniques to remove age-related growth trends
Creating a single representative chronology per site/file
c) Standardization: Each chronology is converted to z-scores using scale(), which:

Centers the data around zero (subtracts the mean)
Scales to unit variance (divides by standard deviation)
Creates standardized growth indices where positive values indicate above-average growth and negative values indicate below-average growth
d) Temporal Filtering: Only data from 1950 onwards is retained to focus on the modern period with better temporal overlap across sites.

3. Multi-Site Chronology Integration
a) Temporal Alignment: All individual chronologies are merged by year into a single data matrix, covering the period from 1950 to the latest available year across all sites.

b) Mean Chronology Calculation: A master chronology is computed using rowMeans() with na.rm=TRUE, which:

Calculates the arithmetic mean of standardized growth indices across all sites for each year
Handles missing data by excluding NA values from the calculation
Produces a regional signal that represents average tree growth conditions
4. Historical Event Integration
Year Range Parsing: A helper function processes historical event years, handling both single years and ranges with various dash formats (–, —, -).

Event Categorization:

Famine periods: Extracted from historical records and represented as orange shading
War periods: Military conflicts and civil wars represented as red shading
5. Visualization and Output
Combined Chronology Plot: The analysis generates a time-series visualization showing:

Blue line representing the mean standardized growth index
Horizontal reference line at zero indicating average growth
Color-coded background shading for historical events
Temporal coverage from 1950 to present
Statistical Interpretation: The z-score scale allows for direct interpretation:

Values > +1: Above-average growth (good growing conditions)
Values < -1: Below-average growth (stress conditions)
Values near 0: Average growth conditions
6. Analytical Approach
This methodology enables examination of:

Climate-growth relationships: Identifying periods of favorable vs. unfavorable growing conditions
Historical impact assessment: Evaluating whether documented famines and wars correspond to reduced tree growth
Regional growth patterns: Understanding broad-scale environmental changes across the study region
Temporal anomalies: Detecting unusual growth periods that may indicate extreme climatic events
The combined approach provides a robust framework for paleoenvironmental reconstruction and historical correlation analysis using dendrochronological data.

