#!/usr/bin/env python3
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import matplotlib.image as image
import numpy as np
import csv
import random
import heapq

from math import sin, cos, sqrt, atan2, radians

lats_ser,lons_ser,names_ser,country_ser = [],[],[],[]
lats_cl,lons_cl,names_cl,country_cl = [],[],[],[]
name_ser=[], names_cl[]
N=5


#THIS FUNCTION CALCULATES THE DISTANCE BETWEEN TWO POINTS WITH LATITUDE AND LONGITUDINE
def calculate_dist(lat1,lon1,lat2,lon2):
    # approximate radius of earth in km
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

    return print(distance)

#THIS FUNCTION GETS CLIENT'S DATA
def get_data_clients():
    # the Clients can be found here:
    with open('./worldcities.csv') as csvfile:
        reader_cl = csv.DictReader(csvfile,delimiter=',')
        for data_cl in reader_cl:
            names_cl.append(data_cl['city'])
            lats_cl.append(float(data_cl['lat']))
            lons_cl.append(float(data_cl['lng']))
    return lats_cl,lons_cl

#THIS FUNCTION GETS SERVERS' DATA
def get_data_servers():
    # the Servers can be found here:
    with open('./Amazon_servers_stations.csv') as csvfile:
        reader_ser = csv.DictReader(csvfile,delimiter=';')
        for data_ser in reader_ser:
            names_ser.append(data_ser['NAME'])
            lats_ser.append(float(data_ser['LAT']))
            lons_ser.append(float(data_ser['LON']))
    return lats_ser,lons_ser

#THIS FUNCTION PRODUCESE THE MAP
def get_map(lats,lons,Title):

    # How much to zoom from coordinates (in degrees)
    zoom_scale = 0

    # Setup the bounding box for the zoom and bounds of the map
    bbox = [np.min(lats)-zoom_scale,np.max(lats)+zoom_scale,\
            np.min(lons)-zoom_scale,np.max(lons)+zoom_scale]

    fig = plt.figure(figsize=(12, 7), edgecolor='b')
    m = Basemap(projection='cyl', resolution=None,llcrnrlat=-90, urcrnrlat=90,llcrnrlon=-180, urcrnrlon=180,)
    #m.bluemarble()
    m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)

    # Draw coastlines and fill continents and water with color
    #m.drawcoastlines()
    #m.fillcontinents(color='peru',lake_color='dodgerblue')

    # draw parallels, meridians, and color boundaries
    m.drawparallels(np.arange(bbox[0],bbox[1],(bbox[1]-bbox[0])/5),labels=[1,0,0,0])
    m.drawmeridians(np.arange(bbox[2],bbox[3],(bbox[3]-bbox[2])/5),labels=[0,0,0,1],rotation=45)
    #m.drawmapboundary(fill_color='dodgerblue')

    # build and plot coordinates onto map
    x,y = m(lons,lats)

    if Title=="Clients":
        m.plot(x,y,'r*',markersize=1)
    else:
        m.plot(x,y,'r*',markersize=5)

    plt.title(Title+" Distribution")
    plt.savefig(Title +'.pdf', format='pdf', dpi=1000)
    plt.show()

#THIS FUNCTION RETURNS A RANDOM CLIENT
def get_random_client():
    [lats_cl,lons_cl]= get_data_clients()
    k = random.randint(0,int(len(lats_cl)))
    return lats_cl[k], lons_cl[k]

#THIS FUNCTION RETURNS A RANDOM CLIENT
def get_nearest_servers(lat_r_cl,lon_r_cl):
    [lats_ser,lons_ser]=get_data_servers()

    for i in range(len(lats_cl)):
        distances[i] = calculate_dist(lat_r_cl,lon_r_cl,lats_ser[i],lons_ser[i])

    return heapq.nsmallest(5,enumerate(distances),key=lambda x: x[1])
