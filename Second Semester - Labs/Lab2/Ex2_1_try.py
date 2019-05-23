#!/usr/bin/env python3
import simpy
import numpy
import random
from runstats import Statistics
import matplotlib.pyplot as pyplot
import map.py


if __name__ == '__main__':


    #HERE I GET THE CLIENTS ON THE MAP
    [latitudine_clients,longitudine_clients] = map.get_data_clients()
    get_map(latitudine_clients,longitudine_clients,"Clients")

    #HERE I GET THE SERVERS ON THE MAP
    [latitudine_servers,longitudine_servers] = map.get_data_servers()
