#!/usr/bin/env python3

from skyfield import api
from skyfield.api import Loader

import math
import json 

from typing import List, Dict

import s2sphere

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import shapely.geometry
from shapely.geometry import Polygon
import geog
import h3

TLE_URL = 'https://celestrak.com/NORAD/elements/starlink.txt'
R_MEAN = 6378.1 #km
H3_RESOLUTION_LEVEL = 5

def to_deg(radians: float) -> float:
    return radians * (180 / math.pi)

def to_rads(degrees: float) -> float:
    return degrees * (math.pi / 180)

RIGHT_ANGLE = to_rads(90)

def load_sats() -> List:
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

# Returns the cap angle (lambda_FOV/2) in radians
def calcCapAngle(altitude: float, term_angle: float) -> float:
    epsilon = to_rads(term_angle)

    eta_FOV = math.asin( (math.sin(epsilon + RIGHT_ANGLE) * R_MEAN) / (R_MEAN + altitude) )

    lambda_FOV = 2 * (math.pi - (epsilon + RIGHT_ANGLE + eta_FOV))

    # area = 2 * math.pi * (R_MEAN ** 2) * ( 1 - math.cos(lambda_FOV / 2))

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

def plotFootprint(sat):
    angle = calcCapAngle(sat.elevation.km, 35)
    cells = get_cell_ids(sat.latitude.degrees, sat.longitude.degrees, angle)
    print(len(cells))

    proj = cimgt.Stamen('terrain-background')
    plt.figure(figsize=(8,8), dpi=400)
    ax = plt.axes(projection=proj.crs)
    ax.add_image(proj, 6)
    # ax.coastlines()
    ax.set_extent([sat.longitude.degrees-5., sat.longitude.degrees+5.,  sat.latitude.degrees-5,  sat.latitude.degrees+5.], crs=ccrs.Geodetic())
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
    ax.plot(sat.longitude.degrees, sat.latitude.degrees, marker='o', color='red', markersize=4,
                alpha=0.7, transform=ccrs.Geodetic())
    plt.savefig('test.png')

def get_cell_ids_h3(lat:float, lng:float, angle: float) -> List: 
    p = shapely.geometry.Point([lng, lat])
    # so to more accurately match projections maybe arc length of a sphere woulde be best?
    arc_length = R_MEAN * angle # in km

    n_points = 20
    #arc_length should be the radius in kilometers so convert to diameter in meters
    d = arc_length * 1000 # meters
    angles = np.linspace(0, 360, n_points)
    polygon = geog.propagate(p, angles, d)
    mapping = shapely.geometry.mapping(shapely.geometry.Polygon(polygon))
    # print(json.dumps(mapping, indent=2))

    cells = h3.polyfill(mapping, 5, True)
    
    return cells

def plotFootprintH3(sat):
    angle = calcCapAngle(sat.elevation.km, 35)
    cells = get_cell_ids_h3(sat.latitude.degrees, sat.longitude.degrees, angle)
    print(len(list(cells)))

sats = load_sats()
print(f"Loaded {len(sats)} satellites")

ts = api.load.timescale()
now = ts.now()
# print(now)
# now = ts.tt_jd(2459013.763217299)
subpoints = {sat.name : sat.at(now).subpoint() for sat in sats}

sat1 = subpoints['STARLINK-1439']
angle = calcCapAngle(sat1.elevation.km, 35)
print(f"center: {sat1.latitude.degrees}, {sat1.longitude.degrees} angle: {angle}")
#plotFootprint(sat1)
#plotFootprintH3(sat1)

#exit()

# Can I specify the whole sphere to S2? Docs say an angle >= 180 is the whole sphere
# region = s2sphere.Cap.from_axis_angle(s2sphere.LatLng.from_degrees(0,0).to_point(), s2sphere.Angle.from_degrees(181))
# print(region.area())
# prints 12.566370614359172 which is 4*pi, so yes
# cells = get_cell_ids(0.,0.,181.)
# print(len(cells)) # prints 1572864, so yes that should be the whole sphere

coverage: Dict[str,int] = {}
def readTokens():
    with open('cell_ids.txt', 'r') as fd:
        lines = fd.readlines()
        for line in lines:
            tok = line.strip()
            # cell_id = s2sphere.CellId.from_token(tok)
            coverage[tok] = 0

#readTokens()
for _, sat in subpoints.items():
    angle = calcCapAngle(sat.elevation.km, 35)
    cells = get_cell_ids_h3(sat.latitude.degrees, sat.longitude.degrees, angle)
    if len(cells) == 0:
        Exception("empty region returned")
    #print(len(cells))
    # for cellid in cells:
    #     coverage[cellid.to_token()] += 1
# print(coverage)