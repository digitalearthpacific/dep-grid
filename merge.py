import pandas as pd
import geopandas as gpd
import numpy as np
from fiona.crs import from_epsg
import shapely
import warnings
warnings.filterwarnings('ignore')

gdf_admin = gpd.read_file("pacific_admin_polygon.geojson")
countries = list(gdf_admin.country)
print(countries)
gdf_list = []
    
for COUNTRY in countries:
    gdf = gdf_admin[gdf_admin.country == COUNTRY]
    gid = gdf.iloc[0]['gid']

    file = "grid_" + gid.lower() + ".geojson"
    gdf = gpd.read_file(file)
    gdf_list.append(gdf)


#merge
gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
gdf.to_file("grid_pacific.geojson", driver='GeoJSON')


print("Finished.")