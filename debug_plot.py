from typing import List

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

import h3

import shapely.geometry
from shapely.geometry import Polygon

import s2sphere


def plotFootprintH3(lat: float, lon: float, h3_cells: List):
    """Uses cartopy to replot the footprint, mostly used for debugging and validating
    math and library usage
    """
    proj = cimgt.Stamen('terrain-background')
    plt.figure(figsize=(6, 6), dpi=400)
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
    ax.add_image(proj, 6)
    ax.set_extent([lon-10., lon+10., lat-10,  lat+10.], crs=ccrs.Geodetic())
    ax.background_patch.set_visible(False)

    geoms = []
    for cellid in h3_cells:
        vertices = []
        bounds = h3.h3_to_geo_boundary(cellid)  # arrays of [lat, lng]
        coords = [[lng, lat] for [lat, lng] in bounds]
        geo = Polygon(coords)
        geoms.append(geo)

    ax.add_geometries(geoms, crs=ccrs.Geodetic(), facecolor='red',
                      edgecolor='black', alpha=0.4)
    ax.plot(lon, lat, marker='o', color='red', markersize=4,
            alpha=0.7, transform=ccrs.Geodetic())
    plt.savefig('test_h3.png')


def plotFootprint(lat: float, lon: float, cells: List):
    """Uses cartopy to replot the footprint, mostly used for debugging and validating
    math and library usage"""

    proj = cimgt.Stamen('terrain-background')
    plt.figure(figsize=(6, 6), dpi=400)
    ax = plt.axes(projection=proj.crs)
    ax.add_image(proj, 6)
    ax.set_extent([lon-10., lon+10., lat-10,  lat+10.], crs=ccrs.Geodetic())
    ax.background_patch.set_visible(False)

    geoms = []
    for cellid in cells:
        new_cell = s2sphere.Cell(cellid)
        vertices = []
        for i in range(0, 4):
            vertex = new_cell.get_vertex(i)
            latlng = s2sphere.LatLng.from_point(vertex)
            vertices.append((latlng.lng().degrees,
                             latlng.lat().degrees))
        geo = Polygon(vertices)
        geoms.append(geo)

    ax.add_geometries(geoms, crs=ccrs.Geodetic(), facecolor='red',
                      edgecolor='black', alpha=0.4)
    ax.plot(lon, lat, marker='o', color='red', markersize=4,
            alpha=0.7, transform=ccrs.Geodetic())
    plt.savefig('test.png')
