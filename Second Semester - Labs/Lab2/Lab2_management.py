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
MAX_REQ = 20
lambda_us = 25#the higher it is, the higher the num of clients
lambda_eu = 30
lambda_as = 40
mu_us = 1/25
mu_eu = 1/30
mu_as = 1/40
#--------------
#Arrival
#--------------
def arrival(environment,position):
    i=0
    if position=='us':
        arrival_rate=lambda_us
    if position=='eu':
        arrival_rate=lambda_eu
    if position=='as':
        arrival_rate=lambda_as
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
        [lat_client,long_client]=map.get_random_client() #with this line we get a random client
        #here we get the list of nearest servers.
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