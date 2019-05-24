#!/usr/bin/env python3.7

import simpy
import random
from runstats import Statistics
import matplotlib.pyplot as pyplot
import map

#in another file we build geography and routing table

#------------
# Constants
#------------
RANDOM_SEED = 17
SIM_TIME = 10
LINK_CAPACITY = 10 #Gb
SERVER_NUM = 3
#lambda_nort_us = #the higher it is, the higher the num of clients
#lambda_south_us =
#lambda_europe =
#lambda_africa =
#lambda_asia =
#lambda_austr =
mu_us = 1/25
mu_eu = 1/30
mu_as = 1/40
#mu_nort_us =
#mu_south_us =
#mu_europe =
#mu_africa =
#mu_asia =
#mu_austr =

ORIGIN = 'north_us' #(we can use north_us,south_us,europe,africa,asia,austr) 



#--------------
#Arrival
#--------------
def arrival(environment,position):
    i=0
    if position=='north_us':
        arrival_rate=lambda_nort_us
    if position=='south_us':
        arrival_rate=lambda_south_us
    if position=='europe':
        arrival_rate=lambda_europe
    if position=='africa':
        arrival_rate=lambda_africa
    if position=='asia':
        arrival_rate=lambda_asia
    if position=='austr':
        arrival_rate=lambda_austr
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
        tot_list_servers = map.get_list_servers()
        [lat_client,long_client] = map.get_random_client(ORIGIN) #with this line we get a random client
        nearest_servers = map.get_nearest_servers(random_lat,random_lon) #with this line we get the nearset servers to the chosen client
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

    #create simulation environment
    env = simpy.Environment()
    env.servers = Server(env,mu)
    #start the arrival process
    env.process(arrival(env, 'us'))
    env.process(arrival(env,'eu'))
    env.process(arrival(env,'as'))
    #simulate until SIM_TIME
    env.run(until=SIM_TIME)
