import pandas as pd
import glob
import re
import matplotlib.pyplot as plt
import numpy as np

# --- Function to read .rwl files ---
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

# --- Read all RWL files ---
all_files = glob.glob("eth*.rwl")
df_list = [read_rwl(f) for f in all_files]
df = pd.concat(df_list, ignore_index=True)

# Optional: filter years
df = df[(df["Year"] >= 1950) & (df["Year"] <= 2000)]

# --- Calculate site-level anomalies ---
site_chronology = df.groupby(["Site", "Year"])["RingWidth"].mean().reset_index()
# z-score per site
site_chronology['Z'] = site_chronology.groupby("Site")["RingWidth"].transform(
    lambda x: (x - x.mean()) / x.std()
)

print(site_chronology.head())
# Identify drought years per site (negative anomaly)
site_chronology['Drought'] = site_chronology['Z'] < -0.38  # True if drought

# --- Count number of sites in drought per year ---
drought_count = site_chronology.groupby("Year")['Drought'].sum().reset_index()
total_sites = df['Site'].nunique()
drought_count['PercentSites'] = drought_count['Drought'] / total_sites * 100

print(total_sites)

# --- Load famine and war data ---
famine_data = pd.read_csv("famine.csv")
war_data = pd.read_csv("war.csv")

# --- Parse famine data ---
famine_periods = []
for _, row in famine_data.iterrows():
    years = row['Year']
    if '-' in years:
        start, end = map(int, years.split('-'))
        famine_periods.append((start, end))
    else:
        famine_periods.append((int(years), int(years)))

# --- Parse war data ---
war_periods = []
for _, row in war_data.iterrows():
    years = row['Year']
    if '–' in years:  # En dash
        start, end = map(int, years.split('–'))
        war_periods.append((start, end))
    elif '-' in years:  # Hyphen
        start, end = map(int, years.split('-'))
        war_periods.append((start, end))
    else:
        war_periods.append((int(years), int(years)))
        
# Filter famine periods to only include years between 1950 and 2000
famine_periods = [(max(start, 1950), min(end, 2000)) for start, end in famine_periods if end >= 1950 and start <= 2000]

# Filter war periods to only include years between 1950 and 2000
war_periods = [(max(start, 1950), min(end, 2000)) for start, end in war_periods if end >= 1950 and start <= 2000]

# --- Combine famine and war periods ---
combined_periods = []
for famine_start, famine_end in famine_periods:
    for war_start, war_end in war_periods:
        overlap_start = max(famine_start, war_start)
        overlap_end = min(famine_end, war_end)
        if overlap_start <= overlap_end:  # Overlap exists
            combined_periods.append((overlap_start, overlap_end))


import pandas as pd
import matplotlib.pyplot as plt

# --- Plot line chart ---
plt.figure(figsize=(18, 8))  # Larger figure size for better readability

# Plot the percentage of sites in drought as a line
plt.plot(drought_count['Year'], drought_count['PercentSites'], color='green', linewidth=2, label='Percent of Sites in Drought')

# Add famine periods as blue background bands
for start, end in famine_periods:
    plt.axvspan(start, end, color='blue', alpha=0.3)

# Add war periods as red background bands
for start, end in war_periods:
    plt.axvspan(start, end, color='red', alpha=0.3)

for start, end in combined_periods:
    plt.axvspan(start, end, color='lightblue', alpha=0.1)  # Reapply blue
    plt.axvspan(start, end, color='lightblue', alpha=0.1)
    
plt.axhline(y=40, color='red', linestyle='--', linewidth=1.5, label='40% Threshold')

# Set axis labels and title
plt.xlabel("Year", fontsize=14)
plt.ylabel("Percent of Sites showing anomalies with respect to tree ring growth", fontsize=14)
plt.title("Percent of Sites showing anomalies with Famine and War Periods (1950-2000)", fontsize=16)

# Add gridlines
plt.grid(alpha=0.3)

# Simplified legend
handles = [
    plt.Line2D([0], [0], color='blue', lw=4, alpha=0.5, label='Famine'),
    plt.Line2D([0], [0], color='red', lw=4, alpha=0.5, label='War'),
    plt.Line2D([0], [0], color='green', lw=2, label='Percent of Sites'),
    plt.Line2D([0], [0], color='red', linestyle='--', lw=1.5, label='40% Threshold')
]
plt.legend(handles=handles, loc='upper left', bbox_to_anchor=(1, 1))

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig("Percent_Sites_Drought_with_Famine_and_War.png", dpi=300)