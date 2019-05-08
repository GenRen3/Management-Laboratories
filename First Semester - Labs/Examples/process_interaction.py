#!//Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7

import simpy  # it useful for the simulations
import numpy
import random
import matplotlib.pyplot as pyplot

# *******************************************************************************
# Constants
# *******************************************************************************
RANDOM_SEED = 42
NUM_SERVERS = 1
SIM_TIME = 1000

# *******************************************************************************
# Arrival process
# *******************************************************************************


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


# *******************************************************************************
# Client
# *******************************************************************************
class Client(object):

    def __init__(self, environment, i):
        self.env = environment
        self.number = i

        # the client is a "process"
        env.process(self.run())

    def run(self):
        # store the absolute arrival time
        time_arrival = self.env.now
        print("client", self.number, "has arrived at", time_arrival)

        # The client goes to the first server to be served
        yield env.process(env.servers.serve())

        # calculate the response time
        print("client", self.number, "response time",
              self.env.now - time_arrival)

# *******************************************************************************
# Servers
# *******************************************************************************


class Servers(object):

    # constructor
    def __init__(self, environment, num_servers, service_rate):
        self.env = environment
        self.service_rate = service_rate
        self.servers = simpy.Resource(env, num_servers)

    def serve(self):
        # request a server
        with self.servers.request() as request:
            yield request

            # server is free, wait until service is finished
            service_time = random.expovariate(lambd=self.service_rate)

            # yield an event to the simulator
            yield self.env.timeout(service_time)


# *******************************************************************************
# main
# *******************************************************************************
if __name__ == '__main__':

    random.seed(RANDOM_SEED)  # this will give me the same sequence of numbers

    # we suppose it is an exponential distribution, then we'll be able to change it
    mu = 2.0  # mean of the time that the cients stay
    lambd = 1.0  # time required to arrive in line for a client

    # *********************************
    # setup and perform the simulation
    # *********************************

    env = simpy.Environment()

    # servers
    env.servers = Servers(env, NUM_SERVERS, mu)

    # start the arrival process
    env.process(arrival(env, lambd))

    # simulate until SIM_TIME
    env.run(until=SIM_TIME)
