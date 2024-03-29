#!/usr/bin/env python3.7
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import matplotlib.image as image
import numpy as np
import csv
import heapq
import random
import time
from operator import itemgetter

from math import sin, cos, sqrt, atan2, radians

lats_ser,lons_ser = [],[]
names_ser,country_ser = [],[]
lats_cl,lons_cl,names_cl,country_cl = [],[],[],[]
name_ser=[]
names_cl=[]
countries_cl = []
min_servers = []
N=10

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
    with open('./worldcities.csv') as csvfile:
        reader_cl = csv.DictReader(csvfile,delimiter=';')
        for data_cl in reader_cl:
            names_cl.append(str(data_cl['city']))
            countries_cl.append(str(data_cl['continent']))
            lats_cl.append(float(data_cl['lat']))
            lons_cl.append(float(data_cl['lng']))
    return

#THIS FUNCTION GETS SERVERS' DATA
def get_data_servers():
    global names_ser
    global lats_ser
    global lons_ser
    names_ser = []
    lats_ser = []
    lons_ser = []
    with open('./Amazon_servers_stations3.csv') as csvfile:
        reader_ser = csv.DictReader(csvfile,delimiter=';')
        for data_ser in reader_ser:
            names_ser.append(data_ser['NAME'])
            lats_ser.append(float(data_ser['LAT']))
            lons_ser.append(float(data_ser['LON']))
    return names_ser, lats_ser, lons_ser

def get_list_servers():
    return names_ser


#THIS FUNCTION PRODUCES THE MAP
def get_map_total(Title):

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
    m = Basemap(projection='cyl', resolution=None,llcrnrlat=-90, urcrnrlat=90,llcrnrlon=-180, urcrnrlon=180)
    m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)


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


#THIS FUNCTION PRODUCES THE MAP WITH THE LINKS
def get_map_links(nearest_servers,lat_r_cl,lon_r_cl):

    # How much to zoom from coordinates (in degrees)
    zoom_scale = 0
    lat,lon = [],[]

    plt.figure(figsize=(12,6))
    # Define the projection, scale, the corners of the map, and the resolution.
    m = Basemap(projection='merc',resolution=None,llcrnrlat=-90, urcrnrlat=90,llcrnrlon=-180, urcrnrlon=180)

    lat.append(lat_r_cl)
    lon.append(lon_r_cl)

    for i in range(len(nearest_servers)):

        if i!=0:
            lat.pop()
            lon.pop()

        lat.append(float(nearest_servers[i][2]))
        lon.append(float(nearest_servers[i][3]))
        print(lat,lon)

        # Draw the lines
        x, y = m(lon[:], lat[:])
        m.plot(x, y, 'o-', markersize=5, linewidth=1)

    # draw parallels, meridians, and color boundaries
    #m.drawparallels(np.arange(bbox[0],bbox[1],(bbox[1]-bbox[0])/5),labels=[1,0,0,0])
    #m.drawmeridians(np.arange(bbox[2],bbox[3],(bbox[3]-bbox[2])/5),labels=[0,0,0,1],rotation=45)
    #m.drawmapboundary(fill_color='white')
    #m.drawstates(color='black')
    #m.drawcountries(color='black')

    # build and plot coordinates onto map
    #x,y = m(lons,lats)
    #m.plot(x,y,'r*',markersize=5)
    plt.title("ASOS Station Distribution")
    #plt.savefig('asos_station_plot.png', format='png', dpi=500)
    plt.show()


#THIS FUNCTION RETURNS A RANDOM CLIENT
def get_random_client(ORIGIN):

    flag=0

    while flag!=1:
        random.seed(time.clock())
        k = random.randint(0,len(lats_cl))
        if countries_cl[k]==ORIGIN:
            flag=1
    print(names_cl[k])
    return lats_cl[k], lons_cl[k]

#THIS FUNCTION IS USED FOR THE SORTING IN get_nearest_servers()
def takeFirst(elem):
    return elem[1]

#THIS FUNCTION RETURNS THE N NEAREST SERVERS
def get_nearest_servers(lat_r_cl,lon_r_cl):
    lats_ser, lons_ser] = get_data_servers()
    distances = []

    for i in range(len(lats_ser)):
        distances.append([names_ser[i], calculate_dist(lat_r_cl,lon_r_cl,lats_ser[i],lons_ser[i]), lats_ser[i],lons_ser[i]])

    #print(lat_r_cl,lon_r_cl)
    #print(distances)
    #distances.sort(key = takeFirst)
    sorted_dist = sorted(distances, key = itemgetter(1))
    #return np.asarray(distances[:N])[:N]
    return np.asarray(sorted_dist[:N])[:N]
