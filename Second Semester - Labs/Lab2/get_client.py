#!/usr/bin/env python3.7

import csv
import pandas as pd


def random_client(position):
    data_client = write_df(position)
    rnd_client = data_client.sample(n=1) #get a random dow from the dataframe obtained in write_df
    latcl = rnd_client['lat']
    lngcl = rnd_client['lng']
    return latcl, lngcl


def write_df(position):
    df = pd.read_csv('./worldcities.csv', sep=';', keep_default_na=False)
    is_origin = df[df.iso2 == position] #save rows where location column is equal to the desired position
    return is_origin
