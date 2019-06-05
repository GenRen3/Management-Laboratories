#!/usr/bin/env python3

import matplotlib.pyplot as pyplot
from runstats import Statistics
import Map_generator as map
import Client as C
import Server as S
import random
import simpy
import time



#-------------------------------------------------------------------------------
# CONSTANTS
#-------------------------------------------------------------------------------
RANDOM_SEED = 17
SIM_TIME = 10 #1440 è un giorno in minuti
LINK_CAPACITY = pow(10, 10) #Gb
MAX_REQ = 30
#SERVER_NUM = 3
lambda_NA = 10 #the higher it is, the higher the num of clients
lambda_SA = 8
lambda_EU = 10
lambda_AF = 10
lambda_AS = 10
lambda_OC = 7
#ORIGIN = 'SA' #(we can use NA,SA,EU,AF,AS,OC)
#00-08, 08-16, 16-00
#small, large, larger
#periodi riferiti all'Europa
first_period = SIM_TIME/3
second_period = 2*first_period
third_period = 3*first_period



#-------------------------------------------------------------------------------
# ARRIVAL
#-------------------------------------------------------------------------------
def arrival(environment,position):
    global i
    #i = 0 #tenendo una i diversa per ogni location, si vede che per NA, EU e AS abbiamo numeri molto alti, mentre AF,SA,OC arrivnao meno clienti
    timer = 0
    if position=='NA':
        arrival_rate1=lambda_NA #16-00
        arrival_rate2=lambda_NA*30/100 #00-08, 3
        arrival_rate3=lambda_NA*80/100 #08-16, 8
    if position=='SA':
        arrival_rate1=lambda_SA #16-00
        arrival_rate2=lambda_SA*30/100 #00-08, 2.4
        arrival_rate3=lambda_SA*80/100 #08-16, 6.4
    if position=='EU':
        arrival_rate1=lambda_EU*30/100 #00-08, 3
        arrival_rate2=lambda_EU*80/100 #08-16, 8
        arrival_rate3=lambda_EU #16-00
    if position=='AF':
        arrival_rate1=lambda_AF*30/100 #00-08, 1.2
        arrival_rate2=lambda_AF*80/100 #08-16, 3.2
        arrival_rate3=lambda_AF #16-00
    if position=='AS':
        arrival_rate1=lambda_AS*80/100 #08-16, 8
        arrival_rate2=lambda_AS #16-00
        arrival_rate3=lambda_AS*30/100 #00-08, 3
    if position=='OC':
        arrival_rate1=lambda_OC*80/100 #08-16, 5.6
        arrival_rate2=lambda_OC #16-00
        arrival_rate3=lambda_OC*30/100 #00-08, 2.1
    while timer <= SIM_TIME:
        if timer<=first_period:
            inter_arrival = random.expovariate(lambd=arrival_rate1)
        elif timer>first_period and timer<=second_period:
            inter_arrival = random.expovariate(lambd=arrival_rate2)
        elif timer>second_period and timer<=third_period:
            inter_arrival = random.expovariate(lambd=arrival_rate3)
        yield environment.timeout(inter_arrival)
        timer=environment.now
        i+=1
        Client(environment,i,position)



#-------------------------------------------------------------------------------
# CLIENTS
#-------------------------------------------------------------------------------
#il client è stupido è la funzione arrival che chiama il client in base a lambda
class Client(object):


    def __init__(self,environment,i,position):
        self.env = environment
        self.number = i
        self.position = position
        self.env.process(self.run())

    def run(self):
        time_arrival = self.env.now
        #random.seed(time.clock())
        #K = random.randint(1,3)
        K = 1
        print("Client ", self.number, "from ", self.position, "arrived at ",
        time_arrival, "with ", K, "requests")

        #with this line we get a random client:
        [lat_client,long_client] = C.random_client(self.position)


        #with this line we get the nearset servers to the chosen client:
        nearest_servers = S.nearest_servers(lat_client,long_client)

        count_req = 1

        while count_req <= K:

            self.size = random.randint(1000,1400)
            print("Client ", i, "size: ", self.size)
            ok = 0

            while ok == 0:
                for server in nearest_servers: #select the nearest servers
                    if all_servers[server[0]].count < MAX_REQ:
                        server_latency = random.uniform(1, 10)/(60)
                        RTT = (float(server[1])/(3*10^5))/(1000*60)
                        print("Client ", i, "first timeout: ", server_latency+RTT)
                        yield self.env.timeout(server_latency+RTT)
                        yield self.env.process(self.env.servers.arrived(server, self.size, self.number))
                        ok = 1
                        break

            count_req+=1
            #calculate response time
            #self.env.stats.push(self.env.now-time_arrival)

        self.tot_time = self.env.now-time_arrival
        print("Client ", self.number, "from ", self.position, "served in ",
        self.tot_time, "at ", self.env.now)



#-------------------------------------------------------------------------------
# SERVERS
#-------------------------------------------------------------------------------
class Server(object):
   def __init__(self, environment):
       self.env = environment
       self.old_time = 0
       self.new_arrival = self.env.event()
       self.new_departure = self.env.event()
       global i
       global all_servers

   def arrived(self,server,size, number):
       self.size = size
       self.current_number = number
       self.new_arrival = self.env.event()
       self.new_departure = self.env.event()
       with all_servers[server[0]].request() as request:
           self.new_arrival.succeed()
           yield request
           self.req = all_servers[server[0]].count
           print("Client ", self.current_number, "served by ", server[0], "with current req: ", self.req)
           yield self.env.process(self.serve(server,self.size))

   def serve(self,server,size):
       self.size = size
       self.current_requests = all_servers[server[0]].count
       print("First fraction: ", LINK_CAPACITY, "/", self.current_requests)
       self.available_capacity = LINK_CAPACITY/self.current_requests
       print("Fraction: ", self.size, "/", self.available_capacity)
       self.transfer_delay = (self.size/self.available_capacity)
       self.time_now = self.env.now
       yield (self.env.timeout(self.transfer_delay) or self.new_arrival or self.new_departure)
       if self.env.now - self.time_now >= self.transfer_delay:
           print("served by: ", server[0])
           self.new_departure.succeed()
       else:
           print("Gone in else")
           yield self.env.process(self.update_timeout(self.time_now, self.size, server, self.current_requests))

   def update_timeout(self, current_time, size, server, req):
       self.size = size
       self.start_time = current_time
       self.old_requests = req
       #self.new_requests = all_servers[server[0]].count
       self.elapsed_time = self.env.now - self.start_time
       self.size_done = self.elapsed_time*(LINK_CAPACITY/self.old_requests)
       self.size_to_do = self.size - self.size_done
       print(self.size_to_do)
       if self.size_to_do < 1:
           print("Served because of size, by: ", server[0])
           self.new_departure.succeed()
           self.new_departure = self.env.event()
       else:
           self.new_arrival = self.env.event()
           yield self.env.process(self.serve(server,self.size_to_do))








#-------------------------------------------------------------------------------
# MAIN
#-------------------------------------------------------------------------------
if __name__=='__main__':

    random.seed(RANDOM_SEED)

    #map.get_map_total("Clients")
    #map.get_map_total("Servers")

    #create simulation environment
    env = simpy.Environment()

    names_ser,countries_ser,lats_ser,lons_ser,costs_ser = S.get_data_servers()

    all_servers = {}
    for server in names_ser: #create dictionary of all servers
        all_servers[server]=simpy.Resource(env, capacity=MAX_REQ)
    #print(all_servers)

    server_request = {}
    for server in all_servers:
        server_request[server] = {}

    env.servers = Server(env)

    #save statistics
    env.stats_NA = Statistics()
    env.stats_SA = Statistics()
    env.stats_EU = Statistics()
    env.stats_AF = Statistics()
    env.stats_AS = Statistics()
    env.stats_OC = Statistics()
    env.stats = Statistics()

    #start the arrival process
    # env.process(arrival(env,'NA'))
    # env.process(arrival(env,'SA'))
    # env.process(arrival(env,'EU'))
    env.process(arrival(env,'AF'))
    # env.process(arrival(env,'AS'))
    # env.process(arrival(env,'OC'))

    # #simulate until SIM_TIME
    i = 0
    env.run(until=SIM_TIME)
