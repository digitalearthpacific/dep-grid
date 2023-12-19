from typing import Literal

import antimeridian
import geopandas as gpd
from geopandas import GeoDataFrame, GeoSeries
from odc.geo import XY, BoundingBox
from odc.geo.gridspec import GridSpec
from shapely.geometry import shape

PACIFIC_EPSG = 3832


def grid(
    resolution: int | float = 30,
    crs=PACIFIC_EPSG,
    return_type: Literal["GridSpec", "GeoSeries"] = "GridSpec",
    intersect_with: gpd.GeoDataFrame | None = None,
) -> GridSpec | gpd.GeoSeries:
    """Returns a GridSpec or GeoSeries representing the Pacific grid, optionally
    interesected with an area of interest.
    """

    if intersect_with is not None:
        full_grid = _geoseries(resolution, crs)
        return _intersect_grid(full_grid, intersect_with)

    return {"GridSpec": _gridspec, "GeoSeries": _geoseries}[return_type](
        resolution, crs
    )


def _intersect_grid(grid: GeoSeries | GeoDataFrame, areas_of_interest):
    return gpd.sjoin(
        gpd.GeoDataFrame(geometry=grid), areas_of_interest.to_crs(grid)
    ).drop(columns=["index_right"])


def _gridspec(resolution):
    gridspec_origin = XY(-3000000.0, -4000000.0)

    side_in_meters = 100_000
    shape = (side_in_meters / resolution, side_in_meters / resolution)

    return GridSpec(
        crs=PACIFIC_EPSG,
        tile_shape=shape,
        resolution=resolution,
        origin=gridspec_origin,
    )


def _geoseries(resolution, crs) -> GeoSeries:
    bounds = BoundingBox(120, -30, 280, 30, crs="EPSG:4326").to_crs(crs)
    tiles = _gridspec(resolution).tiles(bounds)
    geometry, index = zip(
        *[(a_tile[1].boundingbox.polygon.geom, a_tile[0]) for a_tile in tiles]
    )

    gs = gpd.GeoSeries(geometry, index, crs=PACIFIC_EPSG)
    if crs != PACIFIC_EPSG:
        gs = gs.to_crs(crs)
        if crs == 4326:
            gs = gs.apply(lambda geom: shape(antimeridian.fix_shape(geom)))

    return gs
