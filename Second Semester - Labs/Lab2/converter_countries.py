#!/usr/bin/env python3
import pandas as pd
import numpy as np
import csv
import map
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import matplotlib.image as image

data, names_cl,countries_cl,lats_cl,lons_cl=[],[],[],[],[]


def get_data_clients():
    with open('./worldcities.csv') as csvfile:
        reader_cl = csv.DictReader(csvfile,delimiter=';')
        for data_cl in reader_cl:
            names_cl.append(str(data_cl['city']))
            countries_cl.append(str(data_cl['continent']))
            lats_cl.append(float(data_cl['lat']))
            lons_cl.append(float(data_cl['lng']))
    return reader_cl





def converter():
    data = get_data_clients()

    for i in range(len(names_cl)):
        if lats_cl[i] < 90 and lats_cl[i] > 36.536123 and lons_cl[i] < 192.831729 and lons_cl[i] > 41.74285837391827 and countries_cl[i]=="EU":
            countries_cl[i]="AS"
        if lats_cl[i] < 90 and lats_cl[i] > 36.536123 and lons_cl[i] > -180 and lons_cl[i] < -169:
            countries_cl[i]="AS"

    rows = zip(names_cl,lats_cl,lons_cl,countries_cl)

    with open("./export.csv", "w") as f:
        writer = csv.writer(f, delimiter=';')
        for row in rows:
            writer.writerow(row)

    return


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
    #m.bluemarble()
    m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)

    # Draw coastlines and fill continents and water with color
    #m.drawcoastlines()
    #m.fillcontinents(color='peru',lake_color='dodgerblue')

    # draw parallels, meridians, and color boundaries
    #m.drawparallels(np.arange(bbox[0],bbox[1],(bbox[1]-bbox[0])/5),labels=[1,0,0,0])
    #m.drawmeridians(np.arange(bbox[2],bbox[3],(bbox[3]-bbox[2])/5),labels=[0,0,0,1],rotation=45)
    #m.drawmapboundary(fill_color='dodgerblue')

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



if __name__ == '__main__':

    converter()
    get_map_total("Clients")
