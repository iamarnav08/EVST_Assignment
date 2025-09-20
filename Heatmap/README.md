# Tree-Ring Growth Anomalies Heatmap (Ethiopia)

## Purpose of the Heatmap
The heatmap is a visual tool designed to represent **tree-ring growth anomalies** across various sites in Ethiopia over time.  
It highlights deviations in tree-ring growth, which can be linked to **environmental stress** (e.g., droughts).  

This visualization is particularly useful for:
- Identifying patterns in tree growth.
- Correlating anomalies with historical events such as **famines, migrations, or wars**.

---

## Methodology

### 1. Data Collection
- Tree-ring width data was collected from **`.rwl` files** for multiple Ethiopian sites.
- Each `.rwl` file contains **annual tree-ring measurements** for individual trees.

### 2. Data Parsing
- `.rwl` files were parsed to extract:
  - **Site names**
  - **Tree IDs**
  - **Years**
  - **Ring width measurements**
- Data structured into a tabular format with columns:  
  **Site | TreeID | Year | RingWidth**

### 3. Site-Level Aggregation
- Annual tree-ring widths for all trees at a site were **averaged** to compute a **site-level chronology** for each year.

### 4. Z-Score Normalization
- **Z-scores** were calculated to normalize data:  

  \[
  Z = \frac{(X - \mu)}{\sigma}
  \]

  where:
  - \(X\) = ring width,
  - \(\mu\) = mean,
  - \(\sigma\) = standard deviation.

- Highlights **anomalies** by showing deviations from the mean.

### 5. Temporal Filtering
- Data filtered to include only the years **1950–2000** (period of interest).

### 6. Aggregation into Time Bins
- Data aggregated into **1-year bins** for high temporal resolution.

### 7. Pivoting for Heatmap
- Data pivoted into a matrix:
  - **Rows** → Sites
  - **Columns** → Years
  - **Cell Values** → Z-scores

### 8. Heatmap Visualization
  - **Color Scheme**:
    - Red → Negative anomalies (below-average growth)  
    - Yellow → Average growth (mostly negative in our case)  
    - Green → Positive anomalies (above-average growth)  
  - **Vertical Lines**: Dashed lines to separate years for readability.

---

## Utility of the Heatmap

- **Year-Site Analysis**: Easily identify years (x-axis) and sites (y-axis) with anomalies.  
  - Example: Many red cells in one year → widespread drought/tree stress.
- **Pattern Identification**: Detect **temporal** and **spatial patterns**, e.g., drought clusters.
- **Correlation with History**: Overlay with **famine/war data** to reveal environment-society links.
- **Site Comparison**: Compare regions to find **severe/frequent anomalies**.
