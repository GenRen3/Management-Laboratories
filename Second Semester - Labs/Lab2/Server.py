#!/usr/bin/env python3

import numpy as np
import csv
import map
from operator import itemgetter
import Map_generator as map




#This function gets the servers' info
def get_data_servers():
    global names_ser
    global lats_ser
    global lons_ser
    names_ser = []
    lats_ser = []
    lons_ser = []
    with open('./Amazon_servers_stations.csv') as csvfile:
        reader_ser = csv.DictReader(csvfile,delimiter=';')
        for data_ser in reader_ser:
            names_ser.append(data_ser['NAME'])
            lats_ser.append(float(data_ser['LAT']))
            lons_ser.append(float(data_ser['LON']))

    return names_ser, lats_ser, lons_ser




#This function gets the nearest servers
def nearest_servers(lat_cl,lon_cl):
    names, lats, lons = get_data_servers()
    print(len(names))
    all_dist = []
    for i in range(len(names)):
        dist = map.compute_dist(lat_cl,lon_cl,lats[i],lons[i])
        all_dist.append([names[i], dist])
    print(len(all_dist))
    ordered_dist = sorted(all_dist, key=itemgetter(1))

    return ordered_dist
