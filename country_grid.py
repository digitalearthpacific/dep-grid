#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import geopandas as gpd
import numpy as np
from fiona.crs import from_epsg
import shapely
import warnings
warnings.filterwarnings('ignore')

#definitions
GRID_SIZE = 0.01 * 9.6 #1km2
COASTAL_BUFFER = 0.01 * 2 #1km

gdf_admin = gpd.read_file("pacific_admin_polygon.geojson")
countries = list(gdf_admin.NAME)
print(countries)

for country in countries:
    print("GRIDDING: " + country)
    gdf = gdf_admin[gdf_admin.NAME == country]
    gid = gdf.iloc[0]['ISO2']
    #gid

    buffer_df = gdf.geometry.buffer(COASTAL_BUFFER, cap_style = 3)
    gdf = buffer_df

    xmin, ymin, xmax, ymax = gdf.total_bounds

    cell_width = GRID_SIZE
    cell_height = GRID_SIZE

    max_region = max(gdf.geometry, key=lambda a: a.area)
    grid_area = max_region

    grid_cells = []
    for x0 in np.arange(xmin, xmax + cell_width, cell_width):
        for y0 in np.arange(ymin, ymax + cell_height, cell_height):
            x1 = x0 - cell_width
            y1 = y0 + cell_height
            new_cell = shapely.geometry.box(x0, y0, x1, y1)
            if new_cell.intersects(grid_area):
                grid_cells.append(new_cell)
            else:
                pass

    grid_df = gpd.GeoDataFrame(grid_cells, columns=['geometry'], crs=from_epsg(8859))

    grid_df["country"] = country
    grid_df["code"] = gid
    grid_df["gid"] = grid_df.index + 1

    #export
    grid_df.to_file("grid_" + gid.lower() + ".geojson", driver='GeoJSON')

print("Finished.")

