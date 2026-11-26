# Geospatial Development Journal: Maine Lake Ice Phenology

## Entry 1: Hydrologic Basin & County Ingestion (`EPSG:26919`)
* **Objective:** Extract authoritative lake polygons and basin morphometry metrics (`area_km2`, `shoreline_km`, Shoreline Development Index) for Readfield and the Belgrade Lakes watershed alongside surrounding county borders.
* **Technical Solutions:** Queried the USGS National Hydrography Dataset (`NHDWaterbody`) and Census TIGERweb REST APIs, standardizing all vector layers to `NAD83 / UTM Zone 19N (EPSG:26919)`.

## Entry 2: Sentinel-2 L2A STAC NDSI & Lake-Mask Calibration
* **Objective:** Track spring ice-out decay from March through April 2025 without manual scene downloads.
* **Technical Solutions:** Queried AWS Earth Search STAC filtered to Sentinel-2 MGRS tile `19TDK`, computed `NDSI = (Green - SWIR1) / (Green + SWIR1)` on a unified `20 m` `EPSG:26919` grid, and masked surrounding terrestrial snow using `rasterio.mask.mask` (`_clipped.tif`) so NDSI color ramps isolated open-water vs. lake-ice dynamics cleanly.

## Entry 3: Statistical Validation & Cartography
* **Objective:** Quantify lake-size control on spring ice persistence and produce an `ANSI B` (`17" × 11"`) cartographic poster in QGIS 3.44.
* **Technical Solutions:** Verified positive rank correlation between lake surface area and April 1 ice retention (`Spearman ρ = 0.72, p < 0.0001`) and compiled a dual-map layout pairing March 14 and April 1 NDSI rasters with `EPSG:4326` degree-minute graticules.
