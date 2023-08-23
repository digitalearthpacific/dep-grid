import geopandas as gpd

grid = gpd.read_file("grid_pacific.geojson")
land = gpd.read_file("pacific_admin_polygon.geojson").to_crs(grid.crs).unary_union
intersection = grid.intersection(land)

grid.geometry = intersection
output = grid[~grid.is_empty]
output.to_file("grid_pacific_land.geojson")
