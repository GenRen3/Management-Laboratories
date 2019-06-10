#!/usr/bin/env python3.7

import matplotlib.pyplot as pyplot
from runstats import Statistics
import Map_generator as map
import Client as C
import Server as S
import random
import simpy
import time
from decimal import Decimal

#per visualizzare delle print con servizio interrotto, simulare con:
#arrivi solo dall'Africa
#LINK_CAPACITY = pow(10, 2)
#MAX_REQ = 10
#SIM_TIME = 5
#lambda_AF = 9
#K = 1


#-------------------------------------------------------------------------------
# CONSTANTS
#-------------------------------------------------------------------------------
RANDOM_SEED = 13
SIM_TIME = 1440 #1440 è un giorno in minuti
LINK_CAPACITY = 1.25*pow(10, 9) # 10Gbps = 1250000kB/s = 1.25*10^6kB/s = 1.25*10^9 B/s
#LINK_CAPACITY = pow(10, 2) #il valore corretto è pow(10, 10)
MAX_REQ = 1250 #dovremmo basare MAX_REQ su un valore minimo di capacità
#meno di 1kB/s non ha senso, forse neanche meno di 1MB/s ha senso
#capacità minima per richiesta = 1MB/s allora MAX_REQ = 1250
#lambda = number of clients per minute (moltiplicare tutti per 10?)
lambda_NA = 41 #4173 (75%) - 2782 (50%)
lambda_SA = 5 #527 (50%) - 369 (35%)
lambda_EU = 11 #1174 (70%) - 783 (40%)
lambda_AF = 4 #445 (30%) - 297 (20%)
lambda_AS = 10 #1009 (40%) - 631 (25%)
lambda_OC = 1 #156 (45%) - 87 (25%)
#lambda da sistemare
#Se SIM_TIME è in minuti, qual è un numero sensato di clienti al minuto in arrivo?
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
        K = random.randint(1,10) #number of requests of the client
        #K = 1
        print("Client ", self.number, "from ", self.position, "arrived at ",
        time_arrival, "with ", K, "requests")


        #with this line we get a random client:
        [lat_client,long_client] = C.random_client(self.position)


        #with this line we get the nearset servers to the chosen client:
        nearest_servers = S.nearest_servers(lat_client,long_client)

        count_req = 1

        while count_req <= K: #loop until all requests have been served

            self.size = random.randint(1000,1400) #size of a request in Bytes
            #print("Client ", self.number, "size: ", self.size)
            ok = 0

            while ok == 0: #loop until request as been served
                for server in nearest_servers: #select the nearest servers
                    if all_servers[server[0]].count < MAX_REQ: #check if server is available
                        server_latency = random.uniform(1, 10)/(1000*60) #latency of the server, random
                        RTT = (float(server[1])/(3*10^5))/(1000*60) #Round Trip Time, depending on server-client distance
                        self.env.stats_RTT.push(RTT)
                        self.env.stats_clients[self.position].push(RTT)
                        #print("Client ", i, "first timeout: ", server_latency+RTT)
                        yield self.env.timeout(server_latency+RTT) #first timeout interval (it doesn't depend on number of requests at server)
                        yield self.env.process(self.env.servers.arrived(server, self.size, self.number)) #yield to server
                        ok = 1 #set flag to break from inner while
                        break #break from for

            count_req+=1
            #calculate response time
            #self.env.stats.push(self.env.now-time_arrival)

        self.tot_time = self.env.now-time_arrival
        self.env.stats_service_time.push(self.tot_time)
        print("Client ", self.number, "from ", self.position, "served in ",
        self.tot_time, "at ", self.env.now)



#-------------------------------------------------------------------------------
# SERVERS
#-------------------------------------------------------------------------------
class Server(object):
   def __init__(self, environment):
       #global i
       global all_servers
       global names_ser
       self.env = environment
       self.new_arrival = {} #create dictionary to store simpy event of arrival for each server
       for server_name in names_ser:
           self.new_arrival[server_name] = environment.event()
       self.new_departure = {} #create dictionary to store simpy event of departure for each server
       for server_name in names_ser:
           self.new_departure[server_name] = environment.event()

   #affinché non sovrascriva i vari server o clienti, le variabili non devono aver self. davanti (tranne new_arrival e new_departure e env)
   def arrived(self,server,size, number):
       self.new_arrival[server[0]].succeed() #a client has arrived at server[0]
       self.new_arrival[server[0]] = self.env.event() #re-initialize event
       request_successful = 0 #set flag to check the state of the request
       with all_servers[server[0]].request() as request:
           yield request
           #print("client ", number, "arrived in ", server[0], "server at ", self.env.now)
           while request_successful == 0: #loop until request has been served
               current_time = self.env.now
               current_requests = all_servers[server[0]].count #number of requests currently in service at server[0]
               transfer_delay = size/(LINK_CAPACITY*60/all_servers[server[0]].count) #time to serve the request according to current number od requests at server
               #moltiplicato per 60 perché noi simuliamo in minuti e invece LINK_CAPACITY è in GB/s
               #print("Expected timeout for ", number, "is ", transfer_delay)
               yield self.env.timeout(transfer_delay) | self.new_arrival[server[0]] | self.new_departure[server[0]] #whichever happens first, it stops all clients in server[0]
               elapsed_time = self.env.now - current_time
               #print("Client ", number, "times: ", elapsed_time, " & ", transfer_delay)
               # print("Client ", number, "times difference: ", transfer_delay - elapsed_time) #difference between expected timeout and actual elapsed time
               if transfer_delay-elapsed_time > pow(10, -4): #sarebbe più corretto mettere l'if sulla size invece che sul time elapsed, ma alla fine dovrebbe essere uguale
                   #print("Service interrupted for ", number, "at ", self.env.now, "during service in ", server[0])
                   size = size - (self.env.now - current_time)*(LINK_CAPACITY*60/current_requests) #compute remaining size to do according to elapsed time and requests at server[0] before interruption of service
                   # *60 vedi sopra
                   #print("Remaining size for ", number, "is: ", size)
                   if size < 0.1: #in caso rimanesse meno di 0.1 Byte da fare, ma non dovrebbe mai succedere perché prima c'è l'if sulla differenza tra timeout ed elapsed
                       request_successful = 1
                       self.new_departure[server[0]].succeed()
                       self.new_departure[server[0]] = self.env.event()
               else:
                   request_successful = 1 #set flag to 1 in order to break from while loop
                   #print("Flag for ", number, "is ", request_successful)
                   self.new_departure[server[0]].succeed() #request was served, client leaves server[0]
                   self.new_departure[server[0]] = self.env.event()
                   #print("Client ", number, "left server in ", server[0])



#-------------------------------------------------------------------------------
# MAIN
#-------------------------------------------------------------------------------
if __name__=='__main__':

    random.seed(RANDOM_SEED)
    locations = ['NA', 'SA', 'EU', 'AF', 'AS', 'OC']

    #map.get_map_total("Clients")
    #map.get_map_total("Servers")

    #create simulation environment
    env = simpy.Environment()

    names_ser,countries_ser,lats_ser,lons_ser,costs_ser = S.get_data_servers()

    all_servers = {}
    for server in names_ser: #create dictionary of all servers
        all_servers[server]=simpy.Resource(env, capacity=MAX_REQ)
    #print(all_servers)

    total_cost = sum(costs_ser)
    print("With all servers on, the total cost per hour is: ", total_cost, "$")
    print("In 24 hours the total cost is: ", total_cost*24, "$")

    env.servers = Server(env)

    #save statistics
    env.stats_clients = {}
    for loc in locations:
        env.stats_clients[loc] = Statistics()
    # env.stats_NA = Statistics()
    # env.stats_SA = Statistics()
    # env.stats_EU = Statistics()
    # env.stats_AF = Statistics()
    # env.stats_AS = Statistics()
    # env.stats_OC = Statistics()
    env.stats_RTT = Statistics()
    env.stats_service_time = Statistics()

    #start the arrival process
    env.process(arrival(env,'NA'))
    env.process(arrival(env,'SA'))
    env.process(arrival(env,'EU'))
    env.process(arrival(env,'AF'))
    env.process(arrival(env,'AS'))
    env.process(arrival(env,'OC'))

    # #simulate until SIM_TIME
    i = 0
    env.run(until=SIM_TIME)

    print("With all servers on, the average round trip time over 24 hours is: ", env.stats_RTT.mean()) #0.0014016330907470288 (simulazione con parametri scritti in cima)
    print("With all servers on, the average service time over 24 hours is: ", env.stats_service_time.mean())
    print("Average RTT for NA: ", env.stats_clients['NA'].mean())
    print("Average RTT for SA: ", env.stats_clients['SA'].mean())
    print("Average RTT for EU: ", env.stats_clients['EU'].mean())
    print("Average RTT for AF: ", env.stats_clients['AF'].mean())
    print("Average RTT for AS: ", env.stats_clients['AS'].mean())
    print("Average RTT for OC: ", env.stats_clients['OC'].mean())
