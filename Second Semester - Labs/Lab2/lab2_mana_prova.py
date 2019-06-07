#!/usr/bin/env python3.7

import simpy
import random
from runstats import Statistics
import matplotlib.pyplot as pyplot
import time

#------------
# Constants
#------------
RANDOM_SEED = 17
SIM_TIME = 10
LINK_CAPACITY = pow(10,3) #Gb
MAX_REQ = 20

lam_us = 10
lam_eu = 12
lam_as = 8

mu_us = 30
mu_eu = 40
mu_as = 25

#ORIGIN = 'SA' #(we can use NA,SA,EU,AF,AS,OC)


#--------------
#Arrival
#--------------
def arrival(environment,position):
    global i
    if position=='us':
        arrival_rate=lam_us
    elif position=='eu':
        arrival_rate=lam_eu
    elif position=='as':
        arrival_rate=lam_as
    time=0
    while time <= SIM_TIME:
        inter_arrival = random.expovariate(lambd=arrival_rate)
        yield environment.timeout(inter_arrival)
        time = environment.now
        i+=1
        Client(environment,position)



#------------
# Clients
#------------
class Client(object):

    def __init__(self, environment, position):
        global all_servers
        global i
        global single_server
        self.env = environment
        self.pos = position
        self.number = i

        self.env.process(self.run())

    def run(self):
        time_arrival = self.env.now
        ok = 0
        self.size = random.randint(10,100)
        print("client", self.number, "from", self.pos, "has arrived at", time_arrival, "with size: ", self.size)
        self.nearest_server = self.get_nearest(self.pos)
        while ok == 0:
            for server in self.nearest_server:
                if all_servers[server].count < MAX_REQ:
                    yield self.env.process(self.env.servers.arrived(self.pos, server, self.size, self.number))
                    ok = 1
                    break
        print("client", self.number, "from", self.pos, "response time", self.env.now - time_arrival)
        print("Client ", self.number, "finished service at ", self.env.now)

    def get_nearest(self,pos):
        self.nearest = []
        if pos == 'eu':
            self.nearest= ['eu', 'as', 'us']
        elif pos == 'us':
            nearest = ['us', 'as', 'eu']
        elif pos == 'as':
            self.nearest = ['as', 'eu', 'us']
        return self.nearest


#prima new_arrival, poi "with server.request() as request, yield request"

class Servers(object):

    def __init__(self, environment):
        global i
        global single_server
        global server_names
        global all_servers
        self.new_arrival = {}
        for name_ser in server_names:
            self.new_arrival[name_ser] = environment.event()
        self.new_departure = {}
        for name_ser in server_names:
            self.new_departure[name_ser] = environment.event()
        # global server_request
        self.env = environment

    def arrived(self, position, server, size, number):
        self.new_arrival[server].succeed()
        self.new_arrival[server] = self.env.event()
        flag = 0
        with all_servers[server].request() as request:
            yield request
            while flag == 0:
                current_time = self.env.now
                current_requests = all_servers[server].count
                #yield self.env.process(self.env.servers.update_timeouts(server,size))
                transfer_delay = size/(LINK_CAPACITY/all_servers[server].count)
                print("Expected timeout for ", number, "is ", transfer_delay)
                yield self.env.timeout(transfer_delay) | self.new_arrival[server] | self.new_departure[server]
                elapsed_time = self.env.now - current_time
                print(elapsed_time, " & ", transfer_delay)
                print(transfer_delay - elapsed_time)
                if transfer_delay-elapsed_time > pow(10, -3): #current_requests != server.count:
                    print("Service interrupted for ", number, "at ", self.env.now)
                    size = size - (self.env.now - current_time)*(LINK_CAPACITY/current_requests)
                    print("Remaining size for ", number, "is: ", size)
                    if size < 0.1:
                        flag = 1
                        self.new_departure[server].succeed()
                        self.new_departure[server] = self.env.event()
                else:
                    flag = 1
                    print("Flag for ", number, "is ", flag)
                    self.new_departure[server].succeed()
                    self.new_departure[server] = self.env.event()


    def update_timeouts(self, server, size):
        pass





if __name__ == '__main__':

    random.seed(RANDOM_SEED)
    i=0

    env = simpy.Environment()

    server_names = ['eu', 'as', 'us']
    all_servers = {}
    for server in server_names:
        all_servers[server] = simpy.Resource(env, capacity=MAX_REQ)
    print(all_servers)

    server_request = {}
    for server in all_servers:
        server_request[server] = {}

    single_server = simpy.Resource(env, capacity=MAX_REQ)

    env.servers = Servers(env)

    env.process(arrival(env, 'as'))
    env.process(arrival(env, 'us'))
    env.process(arrival(env, 'eu'))

    env.run(until=SIM_TIME)
