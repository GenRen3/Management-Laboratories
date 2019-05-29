#!/usr/bin/env python3

from operator import itemgetter
import csv



#This function gets the servers' info
def get_data_servers():
    global names_ser
    global lats_ser
    global lons_ser
    names_ser = []
    lats_ser = []
    lons_ser = []
    with open('./Datasets/Amazon_servers_stations.csv') as csvfile:
        reader_ser = csv.DictReader(csvfile,delimiter=';')
        for data_ser in reader_ser:
            names_ser.append(data_ser['NAME'])
            lats_ser.append(float(data_ser['LAT']))
            lons_ser.append(float(data_ser['LON']))

    return names_ser, lats_ser, lons_ser




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
    names, lats, lons = get_data_servers()
    print(len(names))
    all_dist = []
    for i in range(len(names)):
        dist = compute_dist(lat_cl,lon_cl,lats[i],lons[i])
        all_dist.append([names[i], dist])
    print(len(all_dist))
    ordered_dist = sorted(all_dist, key=itemgetter(1))

    return ordered_dist
