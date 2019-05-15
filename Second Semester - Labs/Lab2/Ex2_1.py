#!/usr/bin/env python3

import simpy
import numpy
import random
from runstats import Statistics
import matplotlib.pyplot as pyplot

#*******************************************************************************
# Constants
#*******************************************************************************
RANDOM_SEED = 42
NUM_SERVERS = 3
SIM_TIME    = 10000

#*******************************************************************************
# Arrival process
#*******************************************************************************
def arrival(environment, arrival_rate):

    # keep track of client number
    i = 0

    # arrival will continue forever
    while True:

        # sample the time to next arrival
        inter_arrival = random.expovariate(lambd=arrival_rate)

        # yield an event to the simulator
        yield environment.timeout(inter_arrival)

        # a new client arrived
        i += 1
        Client(environment, i)

#*******************************************************************************
# Client
#*******************************************************************************
class Client(object):

    def __init__(self, environment, i):
        self.env = environment
        self.number = i

        # the client is a "process"
        self.env.process(self.run())

    def run(self):
        # store the absolute arrival time
        time_arrival = self.env.now
        #print("client", self.number, "has arrived at", time_arrival)

        # The client goes to the first server to be served
        yield self.env.process(self.env.servers.serve())

        # calculate the response time
        #print("client", self.number, "response time", self.env.now - time_arrival)
        self.env.stats.push(self.env.now - time_arrival)

#*******************************************************************************
# Servers
#*******************************************************************************
class Servers(object):

    # constructor
    def __init__(self, environment, num_servers, service_rate):
        self.env = environment
        self.service_rate = service_rate
        self.servers = simpy.Resource(self.env, num_servers)

    def serve(self):
        # request a server
        with self.servers.request() as request:
            yield request

            # server is free, wait until service is finished
            service_time = random.expovariate(lambd=self.service_rate)

            # yield an event to the simulator
            yield self.env.timeout(service_time)


#*******************************************************************************
# main
#*******************************************************************************
if __name__ == '__main__':

    random.seed(RANDOM_SEED)

    mu = 1.0/20.0
    lambd = 1.0/25.0

    #*********************************
    # setup and perform the simulation
    #*********************************

    env = simpy.Environment()

    # save stats
    env.stats = Statistics()

    # servers
    env.servers = Servers(env, NUM_SERVERS, mu)

    # start the arrival process
    env.process(arrival(env, lambd))

    # simulate until SIM_TIME
    env.run(until=SIM_TIME)

    # print the mean response time
    print("%.3f %.3f %.2f" % (mu, lambd, env.stats.mean()))
