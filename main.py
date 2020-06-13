#!/usr/bin/env python3

from skyfield.api import Loader
import math

TLE_URL = 'https://celestrak.com/NORAD/elements/starlink.txt'
R_MEAN = 6378.1 #km

def load_sats():
    load = Loader('./tle_cache')
    sats = Loader.tle_file(TLE_URL)
    return sats

# Calculates the area of a Starlink satellite using the
# spherical earth model, a satellite (for altitude), and
# minimum terminal angle (elevation angle)
def calcAreaSpherical(altitude: float, term_angle:float) -> float:
    epsilon = to_rads(term_angle)

    eta_FOV = math.asin( (math.sin(epsilon + RIGHT_ANGLE) * R_MEAN) / (R_MEAN + altitude) )
    print(to_deg(eta_FOV))

    lambda_FOV = 2 * (math.pi - (epsilon + RIGHT_ANGLE + eta_FOV))

    area = 2 * math.pi * (R_MEAN ** 2) * ( 1 - math.cos(lambda_FOV / 2))

    return area

def to_deg(radians: float) -> float:
    return radians * (180 / math.pi)

def to_rads(degrees: float) -> float:
    return degrees * (math.pi / 180)

RIGHT_ANGLE = to_rads(90)

# sats = load_sats()
# sat1 = sats[0]
# print(sat1)
area = calcAreaSpherical(340, 35)
print(area)