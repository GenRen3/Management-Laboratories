import csv
import pandas as pd
import Server as S
import Client_prova as C


def get_RTT():

    names_ser,countries_ser,lats_ser,lons_ser,costs_ser = S.get_data_servers()
    names_cl, countries_cl, lats_cl, lons_cl = C.get_data_clients()

    RTT_table = pd.DataFrame(index=names_cl,columns=names_ser)
    for i in range(len(names_cl)):
        if not(names_cl[i] in RTT_table.index):
            for j in range(len(names_ser)):
                dist=S.compute_dist(lats_ser[j],lons_ser[j],lats_cl[i],lons_cl[i])
                RTT = (float(dist)/(3*pow(10,5)))
                RTT_table.loc[names_cl[i],names_ser[j]]=RTT
    return RTT_table
