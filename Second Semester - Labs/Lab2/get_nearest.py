#!/usr/bin/env python3.7

import numpy as np
import csv
import map
from operator import itemgetter
from math import sin, cos, sqrt, atan2, radians

def get_servers():
    names_s = [] #initialize all to empty lists
    lats_s = []
    lons_s = []
    names_s, lats_s, lons_s = map.get_data_servers() #get the servers data from map
    return names_s, lats_s, lons_s

#compute the distance between the client and the server i
def compute_dist(lat1,lon1,lat2,lon2):
    R = 6373.0

    #convert geographical coordinates to radians
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
    all_dist = [] #initialize the list that will contain [name_server, distance] for all servers
    #iterate over all servers
    for i in range(len(names)):
        dist = compute_dist(lat_cl,lon_cl,lats[i],lons[i])
        all_dist.append([names[i], dist])
    ordered_dist = sorted(all_dist, key=itemgetter(1)) #order all_dist according to distance
    return ordered_dist
