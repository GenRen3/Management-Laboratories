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
name_ser=[]
names_cl=[]
countries_cl = []
distances=[]
min_servers = []
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

    return distance

#THIS FUNCTION GETS CLIENT'S DATA
def get_data_clients():
    # the Clients can be found here:
    with open('./worldcities.csv') as csvfile:
        reader_cl = csv.DictReader(csvfile,delimiter=';')
        for data_cl in reader_cl:
            names_cl.append(str(data_cl['city']))
            countries_cl.append(str(data_cl['iso2']))
            lats_cl.append(float(data_cl['lat']))
            lons_cl.append(float(data_cl['lng']))
    # return lats_cl,lons_cl
    return

#THIS FUNCTION GETS SERVERS' DATA
def get_data_servers():
    # the Servers can be found here:
    with open('./Amazon_servers_stations.csv') as csvfile:
        reader_ser = csv.DictReader(csvfile,delimiter=';')
        for data_ser in reader_ser:
            names_ser.append(data_ser['NAME'])
            lats_ser.append(float(data_ser['LAT']))
            lons_ser.append(float(data_ser['LON']))
    # return lats_ser,lons_ser
    return

def get_list_servers():

    return names_ser


#THIS FUNCTION PRODUCESE THE MAP
def get_map(Title):

    # How much to zoom from coordinates (in degrees)
    zoom_scale = 0

    # Setup the bounding box for the zoom and bounds of the map
    if Title=="Clients":
        bbox = [np.min(lats_cl)-zoom_scale,np.max(lats_cl)+zoom_scale,\
                np.min(lons_cl)-zoom_scale,np.max(lons_cl)+zoom_scale]
    else:
        bbox = [np.min(lats_ser)-zoom_scale,np.max(lats_ser)+zoom_scale,\
                np.min(lons_ser)-zoom_scale,np.max(lons_ser)+zoom_scale]

    fig = plt.figure(figsize=(12, 7), edgecolor='b')
    m = Basemap(projection='cyl', resolution=None,llcrnrlat=-90, urcrnrlat=90,llcrnrlon=-180, urcrnrlon=180,)
    #m.bluemarble()
    m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)

    # Draw coastlines and fill continents and water with color
    #m.drawcoastlines()
    #m.fillcontinents(color='peru',lake_color='dodgerblue')

    # draw parallels, meridians, and color boundaries
    #m.drawparallels(np.arange(bbox[0],bbox[1],(bbox[1]-bbox[0])/5),labels=[1,0,0,0])
    #m.drawmeridians(np.arange(bbox[2],bbox[3],(bbox[3]-bbox[2])/5),labels=[0,0,0,1],rotation=45)
    #m.drawmapboundary(fill_color='dodgerblue')

    # # build and plot coordinates onto map
    # x,y = m(lons,lats)
    #
    # if Title=="Clients":
    #     m.plot(x,y,'r*',markersize=1)
    # else:
    #     m.plot(x,y,'r*',markersize=5)

    if Title=="Clients":
        for i in range(len(lats_cl)):
            country = countries_cl[i]
            x,y = m(lons_cl[i],lats_cl[i])

            if country=="NA":
                m.plot(x,y,'r*',markersize=1)
            if country=="SA":
                m.plot(x,y,'y*',markersize=1)
            if country=="EU":
                m.plot(x,y,'c*',markersize=1)
            if country=="AS":
                m.plot(x,y,'b*',markersize=1)
            if country=="OC":
                m.plot(x,y,'w*',markersize=1)
            if country=="AF":
                m.plot(x,y,'m*',markersize=1)

    else:
        x,y = m(lons_ser,lats_ser)
        m.plot(x,y,'r*',markersize=5)


    plt.title(Title+" Distribution")
    plt.savefig(Title +'.pdf', format='pdf', dpi=1000)
    plt.show()


#THIS FUNCTION RETURNS A RANDOM CLIENT
def get_random_client(ORIGIN):
    flag=0
    while flag!=1:
        k = random.randint(0,len(lats_cl))
        print(k)
        if countries_cl[k]==ORIGIN:
            flag=1
    print(names_cl[k])
    
    return lats_cl[k], lons_cl[k]

#THIS FUNCTION IS USED FOR THE SORTING IN get_nearest_servers()
def takeFirst(elem):
    return elem[0]

#THIS FUNCTION RETURNS THE N NEAREST SERVERS
def get_nearest_servers(lat_r_cl,lon_r_cl):
    # [lats_ser, lons_ser] = get_data_servers()

    for i in range(len(lats_ser)):
        distances.append([calculate_dist(lat_r_cl,lon_r_cl,lats_ser[i],lons_ser[i]) , names_ser[i]])

    distances.sort(key = takeFirst)
    return np.asarray(distances[:N])[:N,1]
