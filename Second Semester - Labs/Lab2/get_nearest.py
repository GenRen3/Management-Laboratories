#!/usr/bin/env python3.7

import numpy as np
import csv
import map
from operator import itemgetter
from math import sin, cos, sqrt, atan2, radians

def get_servers():
    names_s = []
    lats_s = []
    lons_s = []
    names_s, lats_s, lons_s = map.get_data_servers()
    return names_s, lats_s, lons_s

def compute_dist(lat1,lon1,lat2,lon2):
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def nearest_serv(lat_cl,lon_cl):
    names, lats, lons = get_servers()
    print(len(names))
    all_dist = []
    for i in range(len(names)):
        dist = compute_dist(lat_cl,lon_cl,lats[i],lons[i])
        all_dist.append([names[i], dist])
    print(len(all_dist))
    ordered_dist = sorted(all_dist, key=itemgetter(1))
    return ordered_dist
