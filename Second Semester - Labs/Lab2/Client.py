#!/usr/bin/env python3

import csv
import pandas as pd


#col_names = ['city', 'lat', 'lng', 'continent']

def random_client(position):
    data_client = write_df(position)
    rnd_client = data_client.sample(n=1)
    latcl = rnd_client['lat']
    lngcl = rnd_client['lng']
    citycl = str(rnd_client['city'])
    return latcl, lngcl



def write_df(position):
    df = pd.read_csv('./Datasets/worldcities.csv', sep=';', keep_default_na=False)
    is_origin = df[df.continent == position]
    return is_origin


#THIS FUNCTION GETS CLIENT'S DATA
def get_data_clients():
    names_cl,countries_cl,lats_cl,lons_cl = [],[],[],[]
    with open('./Datasets/worldcities.csv') as csvfile:
        reader_cl = csv.DictReader(csvfile,delimiter=';')
        for data_cl in reader_cl:
            names_cl.append(str(data_cl['city']))
            countries_cl.append(str(data_cl['continent']))
            lats_cl.append(float(data_cl['lat']))
            lons_cl.append(float(data_cl['lng']))

    return names_cl, countries_cl, lats_cl, lons_cl
