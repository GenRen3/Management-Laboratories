#!/usr/bin/env python3

from math import sin, cos, sqrt, atan2, radians
from operator import itemgetter
import csv



#This function gets the servers' info
def get_data_servers():
    names_ser, countries_ser,lats_ser, lons_ser, costs_ser = [],[],[],[],[]
    with open('./Datasets/Amazon_servers_stations.csv') as csvfile:
        reader_ser = csv.DictReader(csvfile,delimiter=';')
        for data_ser in reader_ser:
            names_ser.append(data_ser['NAME'])
            countries_ser.append(data_ser['COUNTRY'])
            lats_ser.append(float(data_ser['LAT']))
            lons_ser.append(float(data_ser['LON']))
            costs_ser.append(float(data_ser['COST']))

    return names_ser, countries_ser,lats_ser, lons_ser, costs_ser




#This function gets the distance between 2 points
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



#This function gets the nearest servers
def nearest_servers(lat_cl,lon_cl):
    names,countries ,lats, lons, cost = get_data_servers()
    all_dist = []
    for i in range(len(names)):
        dist = compute_dist(lat_cl,lon_cl,lats[i],lons[i])
        all_dist.append([names[i], dist])
    ordered_dist = sorted(all_dist, key=itemgetter(1))

    return ordered_dist
