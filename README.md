# Multi-Temporal Sentinel-2 NDSI & Basin Morphometry Modeling of Spring Lake Ice-Out Phenology (Readfield & Belgrade Lakes, Maine)

**Author:** Micah Smith | **Coordinate Reference System:** `NAD83 / UTM Zone 19N (EPSG:26919)`

## Executive Summary
Spring lake ice-out timing governs seasonal water-column stratification, summer hypolimnetic dissolved oxygen, and cold-water salmonid habitat across Maine's interior lakes. This project combines **ESA Sentinel-2 Level-2A optical imagery** (streamed via AWS Earth Search STAC across March–April 2025) with **USGS National Hydrography Dataset (NHD)** basin polygons and U.S. Census county boundaries to quantify ice-cover decay across **33 lakes and ponds** in **Readfield and the Belgrade Lakes watershed** (Kennebec, Somerset, Franklin, and Androscoggin Counties).

![Maine Lake Ice Phenology Poster](outputs/Maine_Lake_Ice_Poster.png)

---

## Key Limnological & Statistical Findings
* **Regional Spring Ice-Out Progression (`n = 27` cloud-free lakes on Sentinel-2 MGRS tile `19TDK`):**
  * **Midwinter Full Ice Cover (`March 14, 2025`):** Mean `96.2%` surface ice (`NDSI > 0.40`)
  * **Spring Mid-Breakup (`April 1, 2025`):** Mean `48.2%` surface ice
  * **Full Ice-Out (`April 28, 2025`):** Mean `0.1%` surface ice
* **Basin Morphometry Control (Spearman Rank Correlation):**
  * Larger, deeper basins retained significantly higher ice cover on April 1 (**Spearman `ρ = 0.72`**, **`p < 0.0001`**): e.g., **Long Pond (`10.35 km²`, `69.0%` ice)**, **Maranacook Lake (`7.35 km²`, `57.5%`)**, and **Great Pond (`34.53 km²`, `55.2%`)**, whereas smaller/shallower basins in Readfield melted much earlier, including **Wilson Pond (`2.40 km²`, `20.7%`)** and **Torsey Lake (`2.75 km²`, `27.0%`)**.

![Spring Ice-Out & Morphometry Validation](outputs/maine_ice_validation_chart.png)

---

## Repository Structure
```text
Maine_Lake_Ice_Phenology/
├── scripts/
│   ├── fetch_maine_lakes.py            # USGS NHD basin & morphometry extraction (EPSG:26919)
│   ├── compute_lake_ice_phenology.py   # Sentinel-2 L2A STAC NDSI & per-lake ice cover modeling
│   └── validate_maine_ice.py           # Spearman morphometry validation & 300-DPI chart
├── data_raw/                           # USGS NHD lake basins & Maine county GeoPackages
├── outputs/
│   ├── Maine_Lake_Ice_Poster.png       # 300-DPI 11"x17" QGIS cartographic poster
│   ├── maine_ice_validation_chart.png  # Multi-stage breakup & basin-size correlation figure
│   └── maine_lake_ice_phenology.csv    # Per-lake ice cover & NDSI telemetry table
├── Maine_Lake_Ice_Phenology.qgz        # Self-contained QGIS 3.44 project file
├── JOURNAL.md                          # Geospatial workflow & calibration log
└── README.md                           # Project documentation
```
