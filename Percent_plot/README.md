# Percent of Sites Showing Tree-Ring Anomalies with Famine and War Periods


## Methodology

### 1. Data Collection
- **Tree-Ring Data**: `.rwl` files containing annual tree-ring width measurements for **7 Ethiopian sites**.  
- **Historical Data**: CSV files (`famine.csv`, `war.csv`) containing famine and war periods.

### 2. Data Parsing
- `.rwl` files parsed to extract:
  - Site names  
  - Tree IDs  
  - Years  
  - Ring width measurements  
- Data structured into tabular format with columns:  
  **Site | TreeID | Year | RingWidth**

### 3. Temporal Filtering
- Tree-ring data filtered to include only **1950–2000**, the period of interest.

### 4. Site-Level Aggregation
- Annual tree-ring widths averaged for each site to compute **site-level chronology** per year.

### 5. Z-Score Normalization
- **Z-scores** calculated:  

  \[
  Z = \frac{(X - \mu)}{\sigma}
  \]

  where:  
  - \(X\) = ring width  
  - \(\mu\) = mean  
  - \(\sigma\) = standard deviation  

- **Negative Z-scores below -0.38** identified as **drought years (tree-ring anomalies)**.

### 6. Drought Analysis
- Percentage of sites in drought for each year:  

  \[
  \text{PercentSites} = \frac{\text{Number of Sites in Drought}}{\text{Total Sites}} \times 100
  \]

### 7. Historical Data Integration
- **Famine and War Data**:
  - Parsed and filtered for **1950–2000**.  
  - Overlap detection used to identify **combined famine and war years**.

### 8. Visualization
- A **line chart** is plotted showing:
  - Percent of sites in drought (over time).  
  - **Famine periods** → Blue bands.  
  - **War periods** → Red bands.  
  - **Combined famine & war** → Light blue bands.  
  - **40% threshold line** → highlights significant drought years.  

---

## Usefulness of the Line Plot

### Event Alignment Check
- Allows researchers to see if **droughts preceded, overlapped, or followed** famine and war periods.  
- Helps in understanding **cause-effect relationships** between climate stress and societal crises.  

### Multi-Factor Comparison
- Enables **side-by-side visualization** of environmental (drought) and human (famine/war) stressors.  
- Makes it easier to analyze how **multiple pressures interacted** in shaping historical outcomes.  

### Severity Estimation
- The **height of the drought line (percent of sites)** shows how widespread the stress was.  
- Useful for assessing if **localized droughts** vs **widespread droughts** align differently with famine/war.  

### Threshold-Based Insights
- The **40% threshold line** provides a **reference benchmark**.  
- Years crossing the threshold may signal **critical stress events**, potentially triggering famine/war.  

### Trend Analysis
- Helps in spotting **long-term drought trends** and whether they correlate with **clusters of crises**.  
- Example: Multiple consecutive drought years may align with **prolonged societal stress**.  

### Cross-Validation with Historical Records
- Visual overlaps act as a **check for accuracy** of famine and war records.  
- If famine periods match widespread droughts, it **strengthens confidence** in historical data reliability.  

---

## More Usefulness

### 1. Historical Correlation
- Overlays **tree-ring anomalies** with **famine/war periods**, identifying years where **environmental stress** aligned with **societal stress**.

### 2. Pattern Identification
- Reveals **temporal patterns in droughts** and their **alignment with historical events**.  