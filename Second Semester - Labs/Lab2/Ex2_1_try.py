#!/usr/bin/env python3

import simpy
from pycountry_convert import country_alpha2_to_continent_code as a2ctc
import numpy as np
import random
from runstats import Statistics
import matplotlib.pyplot as pyplot
import map
import heapq
import csv
import pandas as pd

if __name__ == '__main__':

    # #HERE I GET THE CLIENTS ON THE MAP
    [latitudine_clients,longitudine_clients] = map.get_data_clients()
    map.get_map("Clients")
    #
    # #HERE I GET THE SERVERS ON THE MAP
    # [latitudine_servers,longitudine_servers] = map.get_data_servers()
    # map.get_map(latitudine_servers,longitudine_servers,"Servers")
    # #[random_lat, random_lon] = map.get_random_client()
    # #map.get_nearest_servers(random_lat,random_lon)
