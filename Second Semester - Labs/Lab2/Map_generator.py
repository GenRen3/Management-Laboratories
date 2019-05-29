#!/usr/bin/env python3
from mpl_toolkits.basemap import Basemap
from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt
import csv


#THIS FUNCTION PRODUCES THE MAP
def get_map_total(Title):

    # How much to zoom from coordinates (in degrees)
    zoom_scale = 0

    # Setup of the bounding box for the zoom and bounds of the map
    if Title=="Clients":
        bbox = [np.min(lats_cl)-zoom_scale,np.max(lats_cl)+zoom_scale,\
                np.min(lons_cl)-zoom_scale,np.max(lons_cl)+zoom_scale]
    else:
        bbox = [np.min(lats_ser)-zoom_scale,np.max(lats_ser)+zoom_scale,\
                np.min(lons_ser)-zoom_scale,np.max(lons_ser)+zoom_scale]

    #Generates the base of the map by using arcgis map images
    fig = plt.figure(figsize=(12, 7), edgecolor='b')
    m = Basemap(projection='cyl',resolution=None,llcrnrlat=-90, urcrnrlat=90,
    llcrnrlon=-180, urcrnrlon=180)
    m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=1500, verbose=True)

    #Prits servers or clients and uses different colors for different continents
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

    #Adds titles and saves the figure
    plt.title(Title+" Distribution")
    plt.savefig(Title +'.pdf', format='pdf', dpi=1000)
    plt.show()


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
