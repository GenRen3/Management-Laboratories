#!/usr/bin/env python3.7

import matplotlib.pyplot as pyplot
from runstats import Statistics
import Map_generator as map
import Client as C
import Server as S
import random
import simpy
import time

#per visualizzare delle print con servizio interrotto, simulare con:
#arrivi solo dall'Africa
#LINK_CAPACITY = pow(10, 2)
#SIM_TIME = 5
#lambda_AF = 9
#K = 1


#-------------------------------------------------------------------------------
# CONSTANTS
#-------------------------------------------------------------------------------
RANDOM_SEED = 17
SIM_TIME = 1440 #1440 è un giorno in minuti
#LINK_CAPACITY = 1.25*pow(10, 9) # 10Gbps = 1250000kB/s = 1.25*10^6kB/s = 1.25*10^9 B/s
LINK_CAPACITY = 1.25*pow(10,6) #Gb/s #il valore corretto è pow(10, 10)
MAX_REQ = 125
lambda_NA = 400 #the higher it is, the higher the num of clients
lambda_SA = 300
lambda_EU = 350
lambda_AF = 120
lambda_AS = 500
lambda_OC = 80
#ORIGIN = 'SA' #(we can use NA,SA,EU,AF,AS,OC)
#00-08 (40%), 08-16 (60%), 16-00 (70%)
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
        arrival_rate2=lambda_NA*30/100 #00-08
        arrival_rate3=lambda_NA*80/100 #08-16
    if position=='SA':
        arrival_rate1=lambda_SA #16-00
        arrival_rate2=lambda_SA*30/100 #00-08
        arrival_rate3=lambda_SA*80/100 #08-16
    if position=='EU':
        arrival_rate1=lambda_EU*30/100 #00-08
        arrival_rate2=lambda_EU*80/100 #08-16
        arrival_rate3=lambda_EU #16-00
    if position=='AF':
        arrival_rate1=lambda_AF*30/100 #00-08
        arrival_rate2=lambda_AF*80/100 #08-16
        arrival_rate3=lambda_AF #16-00
    if position=='AS':
        arrival_rate1=lambda_AS*80/100 #08-16
        arrival_rate2=lambda_AS #16-00
        arrival_rate3=lambda_AS*30/100 #00-08
    if position=='OC':
        arrival_rate1=lambda_OC*80/100 #08-16
        arrival_rate2=lambda_OC #16-00
        arrival_rate3=lambda_OC*30/100 #00-08
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

def print_cose(environment):
    global server_status
    timer = 0
    while timer <= SIM_TIME:
        print("Servers status: ")
        for server in server_status.items():
            print(server[0], ": ", server[1][0])
        yield environment.timeout(180)
        timer = environment.now




#-------------------------------------------------------------------------------
# CLIENTS
#-------------------------------------------------------------------------------
#il client è stupido è la funzione arrival che chiama il client in base a lambda
class Client(object):


    def __init__(self,environment,i,position):
        global server_status
        self.env = environment
        self.number = i
        self.position = position
        self.env.process(self.run())

    def run(self):
        time_arrival = self.env.now
        #random.seed(time.clock())
        K = random.randint(1,10)
        #K = 1
        #print("Client ", self.number, "from ", self.position, "arrived at ",
        #time_arrival, "with ", K, "requests")

        #with this line we get a random client:
        [lat_client,long_client] = C.random_client(self.position)


        #with this line we get the nearset servers to the chosen client:
        nearest_servers = S.nearest_servers(lat_client,long_client)

        count_req = 1

        while count_req <= K:

            self.size = random.randint(1000,2000) #size of a request in Bytes
            #print("Client ", self.number, "size: ", self.size)
            ok = 0

            while ok == 0:
                for server in nearest_servers: #select the nearest servers
                    if all_servers[server[0]].count < MAX_REQ and server_status[server[0]][0] == 1:
                        server_latency = random.uniform(1, 10)/(1000*60)
                        RTT = (float(server[1])/(3*10^5))/(60)
                        self.env.stats_RTT.push(RTT)
                        #fare statistica di RTT
                        #self.env.stats.push(RTT)
                        #print("Client ", i, "first timeout: ", server_latency+RTT)
                        yield self.env.timeout(server_latency+RTT) #first timeout interval (it doesn't depend on number of requests at server)
                        yield self.env.process(self.env.servers.arrived(server, self.size, self.number)) #yield to server
                        yield self.env.timeout(RTT)
                        ok = 1 #set flag to break from inner while
                        break #break from for
                if ok == 0:
                    for server in nearest_servers:
                        if server_status[server[0]][0] == 0:
                            server_status[server[0]][0] = 1
                            break

            count_req+=1
            #calculate response time

        self.tot_time = self.env.now-time_arrival
        #print("Client ", self.number, "from ", self.position, "served in ",
        #self.tot_time, "at ", self.env.now)



#-------------------------------------------------------------------------------
# SERVERS
#-------------------------------------------------------------------------------
class Server(object):
   def __init__(self, environment):
       #global i
       global all_servers
       global names_ser
       global server_status
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
               transfer_delay = size/(LINK_CAPACITY*60/current_requests) #time to serve the request according to current number od requests at server
               #moltiplicato per 60 perché noi simuliamo in minuti e invece LINK_CAPACITY è in GB/s
               #print("Expected timeout for ", number, "is ", transfer_delay)
               a = self.new_arrival[server[0]]
               d = self.new_departure[server[0]]
               r = yield self.env.timeout(transfer_delay) | a | d #whichever happens first, it stops all clients in server[0]
               elapsed_time = self.env.now - current_time
               #print("Client ", number, "times: ", elapsed_time, " & ", transfer_delay)
               #print("Client ", number, "times difference: ", transfer_delay - elapsed_time) #difference between expected timeout and actual elapsed time
               if a in r or d in r: #sarebbe più corretto mettere l'if sulla size invece che sul time elapsed, ma alla fine dovrebbe essere uguale
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
           #print(all_servers[server[0]].count)
           if all_servers[server[0]].count <= 2 and self.env.now >= 10:
               print('Current req: ', current_requests)
               server_status[server[0]][0] = 0




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
    print(costs_ser) #forse c'è uno 0.16 dove dovrebbe esserci uno 0.32; in Oceania 0.35 forse è tanto

    all_servers = {}
    for server in names_ser: #create dictionary of all servers
        all_servers[server]=simpy.Resource(env, capacity=MAX_REQ)
    #print(all_servers)

    index_ser = 0
    server_status = {}
    for server in names_ser:
        server_status[server] = [0, countries_ser[index_ser], costs_ser[index_ser]]
        index_ser+=1
    server_status['DENVER'][0] = 1
    server_status['MONACO'][0] = 1
    server_status['HONG KONG'][0] = 1
    print(server_status)

    total_cost = sum(server_status[server][2] for server in server_status if server_status[server][0]==1)
    print("With some server off, the total cost per hour is: ", total_cost)

    env.servers = Server(env)

    #save statistics
    #save statistics
    env.stats_pos = {}
    for loc in locations:
        env.stats_pos[loc] = Statistics()
    env.stats_day_night = {}
    for h in ['first', 'second', 'third']:
        env.stats_day_night[h] = Statistics()
    env.stats_RTT = Statistics()
    env.stats_service_time = Statistics()

    #start the arrival process
    env.process(print_cose(env))

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
    print("Average service time in the first period: ", env.stats_clients['OC'].mean())
    print("Average service time in the second period: ", env.stats_clients['OC'].mean())
    print("Average service time in the third period: ", env.stats_clients['OC'].mean())



    #trovare modo furbo per spegnere i server.
    #In base a cosa li spegnamo? Il numero dei server spenti e quali sono spenti deve essere diverso nei tre intervalli di tempo

    # NA,SA
    #fascia 1: da -42.419415 (Rio de Janeiro) a -86.250007 (South Bend)
    #fascia 2: da South Bend a -104.984703 (Denver)
    #fascia 3: da Denver a -124.367277 (Capetown, NA)

    # EU, AF
    #fascia 1: da 28.049722 (Johannesburg) a 4.897976 (Amsterdam)
    #fascia 2: da Amsterdam a -15.295431 (Saint Louis)

    # AS, OC
    #fascia 1: da 151.216454 (Sidney) a 115.86048 (Perth)
    #fascia 2: da Perth a 72.8335238 (Mumbai)
