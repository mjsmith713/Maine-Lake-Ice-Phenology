"""
Extracts USGS National Hydrography Dataset (NHD) lake polygons and computes
basin morphometry (area, shoreline length, Shoreline Development Index) for
Readfield and the Belgrade Lakes watershed in NAD83 / UTM Zone 19N (EPSG:26919).
"""

import os
import requests
import geopandas as gpd

PROJECT_DIR = r"C:\QGIS_Work\Maine_Lake_Ice_Phenology"
DATA_DIR = os.path.join(PROJECT_DIR, "data_raw")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(PROJECT_DIR, "rasters", "raw"), exist_ok=True)
os.makedirs(os.path.join(PROJECT_DIR, "rasters", "processed"), exist_ok=True)
os.makedirs(os.path.join(PROJECT_DIR, "outputs"), exist_ok=True)

TARGET_CRS = "EPSG:26919"  # NAD83 / UTM Zone 19N (Maine Statewide Metric CRS)
s = chr(47)
nhd_url = f"https:{s}{s}hydro.nationalmap.gov{s}arcgis{s}rest{s}services{s}nhd{s}MapServer{s}12{s}query"

print("Querying USGS National Hydrography Dataset (NHD) for Readfield & Belgrade Lakes...")
params = {
    "where": "GNIS_NAME IS NOT NULL AND AREASQKM >= 0.15",
    "geometry": "-70.05,44.32,-69.72,44.62",
    "geometryType": "esriGeometryEnvelope",
    "inSR": "4326",
    "spatialRel": "esriSpatialRelIntersects",
    "outFields": "GNIS_NAME,AREASQKM,FTYPE",
    "returnGeometry": "true",
    "outSR": "4326",
    "f": "geojson"
}

resp = requests.get(nhd_url, params=params, timeout=30)
resp.raise_for_status()
gdf = gpd.GeoDataFrame.from_features(resp.json()["features"], crs="EPSG:4326").to_crs(TARGET_CRS)

gdf = gdf.rename(columns={"GNIS_NAME": "lake_name"})
gdf = gdf.dissolve(by="lake_name", as_index=False)
gdf["area_km2"] = gdf.geometry.area / 1e6
gdf["shoreline_km"] = gdf.geometry.length / 1000.0
gdf["shoreline_dev_idx"] = gdf["shoreline_km"] / (2.0 * (3.14159265 * gdf["area_km2"]) ** 0.5)
gdf = gdf[gdf["area_km2"] >= 0.15].sort_values("area_km2", ascending=False)

out_path = os.path.join(DATA_DIR, "belgrade_readfield_lakes.gpkg")
gdf.to_file(out_path, driver="GPKG")

print(f"Saved {len(gdf)} official USGS NHD lake basins to: {out_path}")
print(gdf[["lake_name", "area_km2", "shoreline_km", "shoreline_dev_idx"]].head(12).to_string(index=False))
