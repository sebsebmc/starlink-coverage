#!/usr/bin/env python3

from skyfield import api
from skyfield.api import Loader

import math
import typing

import s2sphere

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from shapely.geometry import Polygon


TLE_URL = 'https://celestrak.com/NORAD/elements/starlink.txt'
R_MEAN = 6378.1 #km

def load_sats():
    load = Loader('./tle_cache')
    sats = load.tle_file(url=TLE_URL)
    return sats

# Calculates the area of a Starlink satellite using the
# spherical earth model, a satellite (for altitude), and
# minimum terminal angle (elevation angle)
def calcAreaSpherical(altitude: float, term_angle:float) -> float:
    epsilon = to_rads(term_angle)

    eta_FOV = math.asin( (math.sin(epsilon + RIGHT_ANGLE) * R_MEAN) / (R_MEAN + altitude) )

    lambda_FOV = 2 * (math.pi - (epsilon + RIGHT_ANGLE + eta_FOV))

    area = 2 * math.pi * (R_MEAN ** 2) * ( 1 - math.cos(lambda_FOV / 2))

    return area

def calcCapAngle(altitude: float, term_angle: float) -> float:
    epsilon = to_rads(term_angle)

    eta_FOV = math.asin( (math.sin(epsilon + RIGHT_ANGLE) * R_MEAN) / (R_MEAN + altitude) )

    lambda_FOV = 2 * (math.pi - (epsilon + RIGHT_ANGLE + eta_FOV))

    area = 2 * math.pi * (R_MEAN ** 2) * ( 1 - math.cos(lambda_FOV / 2))

    return (lambda_FOV / 2)

# angle in degrees, is theta (the cap opening angle)
def get_cell_ids(lat, lng, angle):
    region = s2sphere.Cap.from_axis_angle(s2sphere.LatLng.from_degrees(lat, lng).to_point(), s2sphere.Angle.from_radians(angle))
    coverer = s2sphere.RegionCoverer()
    coverer.min_level = 9
    coverer.max_level = 9
    cells = coverer.get_covering(region)
    return cells
    # return sorted([x.id() for x in cells]) 

def to_deg(radians: float) -> float:
    return radians * (180 / math.pi)

def to_rads(degrees: float) -> float:
    return degrees * (math.pi / 180)

RIGHT_ANGLE = to_rads(90)

area = calcAreaSpherical(340, 35)

sats = load_sats()
print(f"Loaded {len(sats)} satellites")

ts = api.load.timescale()
now = ts.now()
# print(now)
# now = ts.tt_jd(2459013.763217299)
subpoints = {sat.name : sat.at(now).subpoint() for sat in sats}

# for name, topos in subpoints.items():
#     print(f"{name}: current elevation {topos.elevation.km}")

sat1 = subpoints['STARLINK-1439']
angle = calcCapAngle(sat1.elevation.km, 35)

print(f"center: {sat1.latitude.degrees}, {sat1.longitude.degrees} angle: {angle}")

cells = get_cell_ids(sat1.latitude.degrees, sat1.longitude.degrees, angle)

proj = cimgt.Stamen('terrain-background')
plt.figure(figsize=(8,8), dpi=400)
ax = plt.axes(projection=proj.crs)
ax.add_image(proj, 6)
# ax.coastlines()
ax.set_extent([sat1.longitude.degrees-5., sat1.longitude.degrees+5.,  sat1.latitude.degrees-5,  sat1.latitude.degrees+5.], crs=ccrs.Geodetic())
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
ax.plot(sat1.longitude.degrees, sat1.latitude.degrees, marker='o', color='red', markersize=4,
            alpha=0.7, transform=ccrs.Geodetic())
plt.savefig('test.png')