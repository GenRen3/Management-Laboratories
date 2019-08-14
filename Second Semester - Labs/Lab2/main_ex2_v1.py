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
RANDOM_SEED = 13
SIM_TIME = 24*60*60
#LINK_CAPACITY = 1.25*pow(10, 9) #10Gbps = 1250000kB/s = 1.25*10^6kB/s = 1.25*10^9 B/s
LINK_CAPACITY = 1.25*pow(10, 6) #10Mbps
#LINK_CAPACITY = 1.25*pow(10, 3) #10kbps
MAX_REQ = 10
lambda_NA = 3 #the higher it is, the higher the number of clients per second
lambda_SA = 2
lambda_EU = 2.5
lambda_AF = 1
lambda_AS = 4
lambda_OC = 0.67

#divide day in 3 periods
first_period = SIM_TIME/3 #00-08 in Europe
second_period = 2*first_period #08-16 in Europe
third_period = 3*first_period #16-24 in Europe



#-------------------------------------------------------------------------------
# ARRIVAL
#-------------------------------------------------------------------------------
def arrival(environment,position):
    global i
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

#print server status every 3600 seconds of simulation
def print_cose(environment):
    global server_status
    timer = 0
    while timer <= SIM_TIME:
        print("Servers status: ")
        for server in server_status.items():
            print(server[0], ": ", server[1][0])
        yield environment.timeout(3600)
        timer = environment.now

#compute the average number of servers on and the average cost per hour
def compute_cost(environment):
    global server_status
    timer = 0
    while timer <= SIM_TIME:
        cost_on = sum(server_status[server][2] for server in server_status if server_status[server][0]==1)
        tot_number_on = sum(server_status[server][0] for server in server_status)
        self.env.stats_number.push(tot_number_on)
        self.env.stats_cost.push(cost_on)
        yield environment.timeout(3600)
        timer = environment.now




#-------------------------------------------------------------------------------
# CLIENTS
#-------------------------------------------------------------------------------
class Client(object):


    def __init__(self,environment,i,position):
        global server_status
        global switch
        self.env = environment
        self.number = i
        self.position = position
        self.env.process(self.run())

    def run(self):
        time_arrival = self.env.now
        #random.seed(time.clock())
        K = random.randint(1,10) #random number of requests between 1 and 10

        #get a random client from chosen zone:
        [lat_client,long_client] = C.random_client(self.position)

        #list of servers ordedered by ditance from chosen client:
        nearest_servers = S.nearest_servers(lat_client,long_client)

        count_req = 1

        while count_req <= K: #loop until all client's requests have been served

            self.size = random.randint(1000,2000) #size of a request in Bytes
            ok = 0 #flag for the single request

            while ok == 0: #loop until request as been served
                for server in nearest_servers: #select the nearest servers
                    if server_status[server[0]][0] == 1 and all_servers[server[0]].count < MAX_REQ: #check if selected server is available (on and not full), if not go to the next one
                        server_latency = random.uniform(1, 10)/(1000) #latency of the server, random between 1 and 10 ms
                        RTT = (float(server[1])/(3*pow(10,5))) #Round Trip Time, depending on server-client distance
                        self.env.stats_RTT.push(RTT)
                        yield self.env.timeout(server_latency+RTT) #first timeout interval (it doesn't depend on number of requests at server)
                        yield self.env.process(self.env.servers.arrived(server, self.size, self.number)) #yield to server
                        yield self.env.timeout(RTT) #RTT for the server's response
                        ok = 1 #set flag to break from inner while (request has been served)
                        break #break from for (we do not need to look for another server)
                if ok == 0: #if request has not been served (so all servers on are full), we check if we can switch on one of the other servers
                    for server in nearest_servers: #if we can, we switch on the server nearest to the client
                        if server_status[server[0]][0] == 0 and self.env.now-switch[server[0]]>=60*60: #we switch a server on only if it has not been switched off in the previous hour (because switching on a server has a cost)
                            server_status[server[0]][0] = 1 #set status of the server to 1 (on)
                            switch[server[0]]=self.env.now #save time of the status switching in order to not change the status again before 1 hour has elapsed
                            break #break from for

            count_req+=1

        self.tot_time = self.env.now-time_arrival #service time
        self.env.stats_service_time.push(self.tot_time)
        #print("Client ", self.number, "from ", self.position, "served in ",
        #self.tot_time, "at ", self.env.now)



#-------------------------------------------------------------------------------
# SERVERS
#-------------------------------------------------------------------------------
class Server(object):
   def __init__(self, environment):
       global all_servers
       global names_ser
       global server_status
       global switch
       self.env = environment
       self.new_arrival = {} #create dictionary to store simpy event of arrival for each server
       self.new_departure = {} #create dictionary to store simpy event of departure for each server
       for server_name in names_ser:
           self.new_arrival[server_name] = environment.event()
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
               transfer_delay = size/(LINK_CAPACITY/current_requests) #time to serve the request according to current number of requests at server
               a = self.new_arrival[server[0]] #assign event to variable
               d = self.new_departure[server[0]] #assign event to variable
               r = yield self.env.timeout(transfer_delay) | a | d #whichever happens first, it stops all clients in server[0]
               elapsed_time = self.env.now - current_time
               if a in r or d in r: #if a or d happened
                   #print("Service interrupted for ", number, "at ", self.env.now, "during service in ", server[0])
                   size = size - (self.env.now - current_time)*(LINK_CAPACITY/current_requests) #compute remaining size to do according to elapsed time and requests at server[0] before interruption of service
                   if size < 0.1: #if remaining size is smaller than 0.1 Byte, we consider the request as served
                       request_successful = 1
                       self.new_departure[server[0]].succeed() #set departure event as successful to stop other clients in service and recompute times
                       self.new_departure[server[0]] = self.env.event() #re-initialize event
               else: #if transfer_delay time elapsed (request was served fully)
                   request_successful = 1  #set flag to 1 in order to exit inner while loop
                   self.new_departure[server[0]].succeed() #request was served, client leaves server[0], set departure event as successful to stop other clients in service and recompute times
                   self.new_departure[server[0]] = self.env.event() #re-initialize event
           if all_servers[server[0]].count <= 1 and self.env.now-switch[server[0]]>=60*60: #if the server has too few requests and it has been on for more than 1 hour, we switch it off
               server_status[server[0]][0] = 0 #set server status to 0 (off)
               switch[server[0]] = self.env.now #save time of the status switching in order to not change the status again before 1 hour has elapsed




#-------------------------------------------------------------------------------
# MAIN
#-------------------------------------------------------------------------------
if __name__=='__main__':

    random.seed(RANDOM_SEED)
    locations = ['NA', 'SA', 'EU', 'AF', 'AS', 'OC']

    #map.get_map_total("Clients") #get clients map
    #map.get_map_total("Servers2") #get servers map

    #create simulation environment
    env = simpy.Environment()

    #get data of the servers
    names_ser,countries_ser,lats_ser,lons_ser,costs_ser = S.get_data_servers()

    all_servers = {}
    server_status = {}
    switch = {}
    index_ser = 0
    #create dictionary of all servers, dictionary of server status and dictionary of switching times
    for server in names_ser:
        all_servers[server] = simpy.Resource(env, capacity=MAX_REQ)
        switch[server] = 0
        server_status[server] = [0, countries_ser[index_ser], costs_ser[index_ser]]
        index_ser+=1
    #set the servers that are on at the beginning
    server_status['CHICAGO'][0] = 1
    server_status['SAN PAOLO'][0] = 1
    server_status['NEW DELHI'][0] = 1
    print(server_status)

    #cost of servers at the beginning
    total_cost = sum(server_status[server][2] for server in server_status if server_status[server][0]==1)
    print("With some server off, the total cost per hour is: ", total_cost)

    env.servers = Server(env)

    #save statistics
    env.stats_pos = {}
    for loc in locations:
        env.stats_pos[loc] = Statistics()
    env.stats_day_night = {}
    for h in ['first', 'second', 'third']:
        env.stats_day_night[h] = Statistics()
    env.stats_RTT = Statistics()
    env.stats_service_time = Statistics()
    env.stats_number = Statistics()
    env.stats_cost = Statistics()

    #start printing status process
    env.process(print_cose(env))
    env.process(compute_cost(env))

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

    print("With some servers on, the average round trip time over 24 hours is: ", env.stats_RTT.mean())
    print("With some servers on, the average service time over 24 hours is: ", env.stats_service_time.mean())
    print("The average number of servers on is: ", env.stats_number.mean())
    print("With some servers on, the average cost per hour is: ", env.stats_cost.mean())
    # print("Average RTT for NA: ", env.stats_clients['NA'].mean())
    # print("Average RTT for SA: ", env.stats_clients['SA'].mean())
    # print("Average RTT for EU: ", env.stats_clients['EU'].mean())
    # print("Average RTT for AF: ", env.stats_clients['AF'].mean())
    # print("Average RTT for AS: ", env.stats_clients['AS'].mean())
    # print("Average RTT for OC: ", env.stats_clients['OC'].mean())
    # print("Average service time in the first period: ", env.stats_clients['first'].mean())
    # print("Average service time in the second period: ", env.stats_clients['second'].mean())
    # print("Average service time in the third period: ", env.stats_clients['third'].mean())
