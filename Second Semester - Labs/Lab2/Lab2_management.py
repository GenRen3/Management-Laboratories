#!/usr/bin/env python3

import simpy
import random
from runstats import Statistics
import matplotlib.pyplot as pyplot
import map
import time


#in another file we build geography and routing table

#------------
# Constants
#------------
RANDOM_SEED = 17
SIM_TIME = 10
LINK_CAPACITY = 10 #Gb
SERVER_NUM = 3
#lambda_NA = #the higher it is, the higher the num of clients
#lambda_SA =
#lambda_EU =
#lambda_AF =
#lambda_AS =
#lambda_OC =
mu_us = 1/25
mu_eu = 1/30
mu_as = 1/40
#mu_NA =
#mu_SA =
#mu_EU =
#mu_AF =
#mu_AS =
#mu_OC =

ORIGIN = 'SA' #(we can use NA,SA,EU,AF,AS,OC)



#--------------
#Arrival
#--------------
def arrival(environment,position):
    i=0
    if position=='NA':
        arrival_rate=lambda_NA
    if position=='SA':
        arrival_rate=lambda_SA
    if position=='EU':
        arrival_rate=lambda_EU
    if position=='AF':
        arrival_rate=lambda_AF
    if position=='AS':
        arrival_rate=lambda_AS
    if position=='OC':
        arrival_rate=lambda_OC
    time=0
    while time <= SIM_TIME:
        time+=1
        inter_arrival = random.expovariate(lambd=arrival_rate)
        yield environment.timeout(inter_arrival)
        i+=1
        Client(environment,i,position)

#------------
# Clients
#------------
#il client è stupido, è la funzione arrival che chiama il client in base a lambda
class Client(object):
    def __init__(self,environment,i,position):
        self.env = environment
        self.number = i
        self.position = position
        self.env.process(self.run())


    def run(self):
        time_arrival = self.env.now
        map.get_data_clients()
        map.get_data_servers()
        tot_list_servers = map.get_list_servers()
        [lat_client,long_client] = map.get_random_client(ORIGIN) #with this line we get a random client
        nearest_servers = map.get_nearest_servers(lat_client,long_client) #with this line we get the nearset servers to the chosen client
        random.seed(time.clock())
        K = random.randint(10,100)
        count_req = 1
        while count_req <= K:
            size = 1000 #size = random.randint(1000,1400)
            routing_table = 'US1'
            ok=0
            while ok==0:
                for server_code in routing_table:
                    yield self.env.process(self.env.servers.serve(server_code,size))
                    if ok==1:
                        break #set timeout??
            count_req+=1
            #calculate response time
            self.env.stats.push(self.env.now-time_arrival)
        self.tot_time = self.env.now-time_arrival
#nella funzione mappa fai classe che genera posizione nella zona designata e calcola distanza e routing table


class Server(object):
    # we drop requests if everything is full
   def __init__(self, environment, service_rate):
       self.env = environment
       self.list_server = ['US1', 'EU1', 'AS1']
       self.service_rate = service_rate
       #self.list_server = simpy.Resource(self.env, capacity=MAX_REQ)
       #self.list_server='funzione.mappa.list_server'
       for server in self.list_server:
           server=simpy.Resource(self.env, capacity=MAX_REQ)


   def serve(self,server_code,size):
       if server_code.count==MAX_REQ:
           ok=0
           return ok
       else:
           with self.server_code.request() as request:#bisogna associare il codice a una risorsa(server)
                yield request
                service_time = random.expovariate(lambd=self.service_rate)
                yield self.env.timeout(service_time)
                ok =1
           return ok
       # if ok==0: return 0 #rejected
       # else:
       #     print('ok')
       #     return 1 #accepted


if __name__=='__main__':
    random.seed(RANDOM_SEED)
    mu = 1.0/20.0

    # map.get_data_clients()
    # map.get_data_servers()
    # #map.get_map("Clients")
    # tot_list_servers = map.get_list_servers()
    # [lat_client,long_client] = map.get_random_client(ORIGIN) #with this line we get a random client
    # nearest_servers = map.get_nearest_servers(lat_client,long_client) #with this line we get the nearset servers to the chosen client
    # print(nearest_servers)

    # #create simulation environment
    env = simpy.Environment()
    env.servers = Server(env,mu)
    # #start the arrival process
    env.process(arrival(env, 'NA'))
    env.process(arrival(env,'SA'))
    env.process(arrival(env,'EU'))
    env.process(arrival(env, 'AF'))
    env.process(arrival(env,'AS'))
    env.process(arrival(env,'OC'))
    # #simulate until SIM_TIME
    env.run(until=SIM_TIME)
