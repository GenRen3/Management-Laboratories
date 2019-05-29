#!/usr/bin/env python3.7

import csv
import pandas as pd


#col_names = ['city', 'iso2', 'lat', 'lng']

def random_client(position):
    data_client = write_df(position)
    rnd_client = data_client.sample(n=1)
    latcl = rnd_client['lat']
    lngcl = rnd_client['lng']
    return latcl, lngcl



def write_df(position):
    df = pd.read_csv('./worldcities.csv', sep=';', keep_default_na=False)
    is_origin = df[df.continent == position]
    return is_origin
