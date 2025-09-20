import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
import glob
import numpy as np

def read_rwl(file_path):
    """Parse .rwl file into long dataframe."""
    data = []
    with open(file_path, "r") as f:
        for line in f:
            if len(line.strip()) > 0 and not line.startswith('#'):  # detect non-empty lines that don't start with comments
                parts = line.split()
                series_id = parts[0]
                year = int(parts[1])
                values = [int(v) for v in parts[2:] if v.isdigit()]
                for i, val in enumerate(values):
                    data.append({
                        "Site": file_path.split("/")[-1].replace(".rwl", ""),
                        "TreeID": series_id,
                        "Year": year + i,
                        "RingWidth": val / 100.0  # convert to mm
                    })
    return pd.DataFrame(data)

# Load all .rwl files
all_dfs = [read_rwl(file) for file in glob.glob("eth*.rwl")]
data = pd.concat(all_dfs, ignore_index=True)

print(data.head())

# Compute site-chronology (average per site-year)
site_chronology = data.groupby(["Site", "Year"])["RingWidth"].mean().reset_index()

# Z-score normalization per site
site_chronology["Zscore"] = site_chronology.groupby("Site")["RingWidth"].transform(
    lambda x: (x - x.mean()) / x.std()
)

# Filter from year 1800 onwards
site_chronology = site_chronology[(site_chronology["Year"] >= 1950) & (site_chronology["Year"] <= 2000)]

site_chronology["YearBin"] = (site_chronology["Year"] // 1) * 1
site_chronology = (
    site_chronology.groupby(["Site", "YearBin"])["Zscore"]
    .mean()
    .reset_index()
)

# Pivot for heatmap
heatmap_data = site_chronology.pivot(index="Site", columns="YearBin", values="Zscore")

# Clip to [-2, 2]
heatmap_data = heatmap_data.clip(-2, 2)

# ...existing code...

# Plot heatmap
plt.figure(figsize=(14, 6))
ax = sns.heatmap(
    heatmap_data,
    cmap="RdYlGn",    # red (negative) to yellow to green (positive)
    center=0,
    vmin=-1, vmax=1,  # Match the clipping range
    cbar_kws={"label": "Z-score"},
    xticklabels=1     # Show every year on the x-axis
)

# Add vertical lines between years
for i in range(len(heatmap_data.columns) - 1):
    ax.axvline(
        x=i + 1,  # Position between two years
        color="black",
        linestyle="--",
        linewidth=0.8,
        alpha=0.5
    )

plt.title("Tree-Ring Growth Anomalies in Ethiopia (1950-2000)", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Site (eth001 – eth007)")
plt.tight_layout()
plt.savefig("Heatmap.png", dpi=300)