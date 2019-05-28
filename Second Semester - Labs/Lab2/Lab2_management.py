#!/usr/bin/env python3.7

import simpy
import random
from runstats import Statistics
import matplotlib.pyplot as pyplot
import map
import time
import get_client
import get_nearest



#in another file we build geography and routing table

#------------
# Constants
#------------
RANDOM_SEED = 17
SIM_TIME = 10
LINK_CAPACITY = 10 #Gb
MAX_REQ = 10
#SERVER_NUM = 3
lambda_NA = 2#the higher it is, the higher the num of clients
lambda_SA = 1
lambda_EU = 2
lambda_AF = 1
lambda_AS = 1.5
lambda_OC = 1.5
#ORIGIN = 'SA' #(we can use NA,SA,EU,AF,AS,OC)



#--------------
#Arrival
#--------------
def arrival(environment,position):
    i=0
    time=0
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
    while time <= SIM_TIME:
        time+=1
        inter_arrival = random.expovariate(lambd=arrival_rate)
        yield environment.timeout(inter_arrival)
        i+=1
        Client(environment,i,position)
    print("End time for ", position, "= ", time)


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
        random.seed(time.clock())
        K = random.randint(1,3)
        print("Client ", self.number, "from ", self.position, "arrived at ", time_arrival, "with ", K, "requests")
        [lat_client,long_client] = map.get_random_client(self.position) #with this line we get a random client
        #[lat_client,long_client] = get_client.random_client(self.position)
        nearest_servers = map.get_nearest_servers(lat_client,long_client) #with this line we get the nearset servers to the chosen client
        #nearest_servers = get_nearest.nearest_serv(lat_client, long_client)
        #print(nearest_servers[0:5])
        #map.get_map_links(nearest_servers,lat_client,long_client)
        count_req = 1
        while count_req <= K:
            ok = 0
            while ok == 0:
                yield self.env.process(self.env.servers.serve(nearest_servers))
                ok = self.env.servers.success_req()
            # size = 1000 #size = random.randint(1000,1400)
            count_req+=1
            #calculate response time
            #self.env.stats.push(self.env.now-time_arrival)
        self.tot_time = self.env.now-time_arrival
        print("Client ", self.number, "from ", self.position, "served in ", self.tot_time)


class Server(object):
    # we drop requests if everything is full
   def __init__(self, environment, all_servers):
       self.env = environment
       self.server_resources = all_servers

   def serve(self,list_nearest):
       self.flag = 0
       for server in list_nearest: #select the nearest servers
           if self.server_resources[server[0]].count < MAX_REQ:
               #print(server[0], self.server_resources[server[0]].count)
               with self.server_resources[server[0]].request() as request:
                   yield request
                   server_latency = random.uniform(1, 10)
                   RTT = float(server[1])/(3*10^5)
                   # print(RTT)
                   transfer_delay = random.randint(1, 5)
                   service_time = server_latency + transfer_delay + RTT
                   # print(service_time)
                   yield self.env.timeout(service_time) #the timeout must be server_latency+RTT(depending on distance)+transfer_delay (depending on available capacity and packet size)
               self.flag = 1 #if request is solved by the server, set ok flag to 1, break from cycle and go back to client for next rquest
               #print(ok)
               break

   def success_req(self):
       if self.flag == 1:
           return 1
       else:
           return 0



if __name__=='__main__':
    random.seed(RANDOM_SEED)

    map.get_data_clients()
    map.get_data_servers()
    #map.get_map_total("Clients")
    # tot_list_servers = map.get_list_servers()
    # [lat_client,long_client] = map.get_random_client(position) #with this line we get a random client
    # nearest_servers = map.get_nearest_servers(lat_client,long_client) #with this line we get the nearset servers to the chosen client
    # print(nearest_servers)

    # #create simulation environment
    env = simpy.Environment()

    tot_list_servers = map.get_list_servers()
    #print(tot_list_servers)
    all_servers = {}
    for server in tot_list_servers: #create dictionary of all servers
        all_servers[server]=simpy.Resource(env, capacity=MAX_REQ)
    #print(all_servers)

    env.servers = Server(env, all_servers)
    # #start the arrival process
    env.process(arrival(env,'NA'))
    env.process(arrival(env,'SA'))
    env.process(arrival(env,'EU'))
    env.process(arrival(env,'AF'))
    env.process(arrival(env,'AS'))
    env.process(arrival(env,'OC'))
    # #simulate until SIM_TIME
    env.run(until=SIM_TIME)
