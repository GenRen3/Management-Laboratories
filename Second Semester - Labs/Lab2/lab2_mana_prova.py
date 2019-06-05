#!/usr/bin/env python3

import simpy
import random
from runstats import Statistics
import matplotlib.pyplot as pyplot
import time

#------------
# Constants
#------------
RANDOM_SEED = 17
SIM_TIME = 5
LINK_CAPACITY = 40 #Gb
MAX_REQ = 20

lam_us = 3
lam_eu = 4
lam_as = 2.5

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
        self.env = environment
        self.pos = position

        self.env.process(self.run())

    def run(self):
        time_arrival = self.env.now
        ok = 0
        print("client", i, "from", self.pos, "has arrived at", time_arrival)
        self.nearest_server = self.get_nearest(self.pos)
        self.size = 1000
        while ok == 0:
            for server in self.nearest_server:
                if all_servers[server].count < MAX_REQ:
                    yield self.env.process(self.env.servers.serve(self.pos, server, self.size))
                    ok = 1
        print("client", i, "from", self.pos, "response time", self.env.now - time_arrival)

    def get_nearest(self,pos):
        self.nearest = []
        if pos == 'eu':
            self.nearest= ['eu', 'as', 'us']
        elif pos == 'us':
            nearest = ['us', 'as', 'eu']
        elif pos == 'as':
            self.nearest = ['as', 'eu', 'us']
        return self.nearest


class Servers(object):

    def __init__(self, environment):
        global i
        global server_request
        global all_servers
        self.old_time = 0
        self.env = environment

    def serve(self, position, server, size):
        self.position = position
        with all_servers[server].request() as request:
            yield request
            yield self.env.process(self.env.servers.update_timeouts(server,size))


    def update_timeouts(self, server, size):
        self.list_timeouts = []
        self.available_capacity = LINK_CAPACITY/all_servers[server].count
        self.elapsed_time = self.env.now - self.old_time
        for k,v in server_request[server].items():
            v[1] = v[1] - self.available_capacity/self.elapsed_time
            v[0] = v[1]/self.available_capacity
            self.list_timeouts.append(self.env.timeout(v[1]))
        server_request[server][str(i)] = [size, size/self.available_capacity]
        self.list_timeouts.append(self.env.timeout(server_request[server][str(i)][1]))
        print(server_request)
        yield simpy.AnyOf(self.env,self.list_timeouts)




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

    env.servers = Servers(env)

    env.process(arrival(env, 'as'))
    env.process(arrival(env, 'us'))
    env.process(arrival(env, 'eu'))

    env.run(until=SIM_TIME)
