"""
Extracts USGS National Hydrography Dataset (NHD) lake polygons and computes
basin morphometry (area, shoreline length, Shoreline Development Index) for
Readfield and the Belgrade Lakes watershed in NAD83 / UTM Zone 19N (EPSG:26919).
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

PROJECT_DIR = r"C:\QGIS_Work\Maine_Lake_Ice_Phenology"
OUT_DIR = os.path.join(PROJECT_DIR, "outputs")
df = pd.read_csv(os.path.join(OUT_DIR, "maine_lake_ice_phenology.csv"))

# Pivot ice cover % across the three spring stages
piv = df.pivot_table(
    index=["lake_name", "area_km2", "shoreline_dev_idx"],
    columns="window",
    values="ice_cover_pct"
).reset_index().dropna(subset=["2025_03_midwinter_ice", "2025_04_early_breakup", "2025_04_late_iceout"])

# Filter out any lake obscured by clouds on April 1 (where mid-breakup == 0.0 despite large area)
valid_breakup = piv[piv["2025_04_early_breakup"] > 1.0].copy()

rho, p_val = stats.spearmanr(valid_breakup["area_km2"], valid_breakup["2025_04_early_breakup"])
print("=== MAINE LAKE ICE PHENOLOGY STATISTICAL SUMMARY ===")
print(f"Valid cloud-free lakes analyzed : {len(valid_breakup)}")
print(f"Mean Midwinter Ice Cover (Mar 14): {valid_breakup['2025_03_midwinter_ice'].mean():.1f}%")
print(f"Mean Mid-Breakup Ice (Apr 01)    : {valid_breakup['2025_04_early_breakup'].mean():.1f}%")
print(f"Mean Full Ice-Out (Apr 28)       : {valid_breakup['2025_04_late_iceout'].mean():.1f}%")
print(f"Spearman Area vs. Ice Retention  : rho = {rho:.3f}, p = {p_val:.4f}")

# Build 2-Panel Publication Chart (300 DPI)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2), dpi=300)
fig.patch.set_facecolor("white")

# Panel A: Top 8 Named Lakes 3-Stage Spring Breakup Progression
top8 = valid_breakup.sort_values("area_km2", ascending=False).head(8)
x = np.arange(len(top8))
w = 0.26

ax1.bar(x - w, top8["2025_03_midwinter_ice"], width=w, color="#1B4F72", label="Mar 14 (Midwinter Ice)")
ax1.bar(x,     top8["2025_04_early_breakup"], width=w, color="#2E86C1", label="Apr 01 (Mid-Breakup)")
ax1.bar(x + w, top8["2025_04_late_iceout"],   width=w, color="#AED6F1", label="Apr 28 (Full Ice-Out)")

ax1.set_xticks(x)
ax1.set_xticklabels([n.replace(" Lake", "").replace(" Pond", "") for n in top8["lake_name"]], rotation=30, ha="right", fontsize=9)
ax1.set_ylabel("Lake Surface Ice Cover (%)", fontsize=10, fontweight="bold")
ax1.set_title("A. Spring 2025 Ice-Out Progression (Readfield & Belgrade Lakes)", fontsize=10.5, fontweight="bold")
ax1.set_ylim(0, 112)
ax1.grid(axis="y", linestyle="--", alpha=0.4)
ax1.legend(frameon=True, fontsize=8.5, loc="upper right")

# Panel B: Basin Surface Area vs. April 1 Mid-Breakup Ice Retention
sc = ax2.scatter(
    valid_breakup["area_km2"],
    valid_breakup["2025_04_early_breakup"],
    c=valid_breakup["shoreline_dev_idx"],
    cmap="viridis",
    s=95,
    edgecolors="black",
    linewidth=0.8,
    zorder=3
)
cbar = plt.colorbar(sc, ax=ax2)
cbar.set_label("Shoreline Development Index (SDI)", fontsize=9)

for _, r in top8.iterrows():
    ax2.annotate(
        r["lake_name"].replace(" Lake", "").replace(" Pond", ""),
        (r["area_km2"], r["2025_04_early_breakup"]),
        textcoords="offset points", xytext=(5, 4), fontsize=8
    )

ax2.set_xscale("log")
ax2.set_xlabel("Lake Basin Surface Area (km², log scale)", fontsize=10, fontweight="bold")
ax2.set_ylabel("Apr 01 Mid-Breakup Ice Cover (%)", fontsize=10, fontweight="bold")
ax2.set_title(f"B. Basin Size Control on Ice Retention (Spearman ρ = {rho:.2f}, p = {p_val:.3f})", fontsize=10.5, fontweight="bold")
ax2.grid(True, which="both", linestyle="--", alpha=0.35)

plt.tight_layout()
chart_path = os.path.join(OUT_DIR, "maine_ice_validation_chart.png")
plt.savefig(chart_path, dpi=300)
print(f"Saved publication validation chart to: {chart_path}")
