#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7

import simpy
import numpy as np
import random

from runstats import Statistics

from scipy.stats import t, sem  # standard error of the mean
import math

import matplotlib.pyplot as pyplot

# *******************************************************************************
# Constants
# *******************************************************************************
RANDOM_SEED = 42
SIM_TIME = 1000
SAMPLES = 30

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
        self.env.process(self.run())

    def run(self):
        # store the absolute arrival time
        time_arrival = self.env.now
        #print("client", self.number, "has arrived at", time_arrival)

        # The client goes to the first server to be served
        yield self.env.process(random.choice(self.env.queues).serve())

        # calculate the response time
        self.env.stats.push(self.env.now - time_arrival)

# *******************************************************************************
# Servers
# *******************************************************************************


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

# *******************************************************************************
# setup and perform a simulation
# *******************************************************************************


def simulate(QUEUES, SERVERS):
    y = []

    for i in range(0, SAMPLES):

        env = simpy.Environment()

        # save stats
        env.stats = Statistics()

        # queues
        env.queues = [Servers(env, SERVERS, mu) for i in range(0, QUEUES)]

        # start the arrival process
        env.process(arrival(env, lambd))

        # simulate until SIM_TIME
        env.run(until=SIM_TIME)

        y.append(env.stats.mean())

    return y


# *******************************************************************************
# main
# *******************************************************************************
if __name__ == '__main__':

    random.seed(RANDOM_SEED)

    # For a fix pair of parameters we will repeat the simulation many times

    mu = 0.05  # 20 s per customers, thus 0.05 customer/s
    lambd = 1.5 * mu

    # ***************************************************************************
    # First Case: 1 Queue, 3 servers
    # ***************************************************************************
    y1 = simulate(1, 3)

    print(t.interval(0.99, SAMPLES-1, np.mean(y1), sem(y1)))

    # ***************************************************************************
    # Second Case: 3 Queue, 1 servers
    # ***************************************************************************
    y2 = simulate(3, 1)

    print(t.interval(0.99, SAMPLES-1, np.mean(y2), sem(y2)))

    f1, ax1 = pyplot.subplots()
    ax1.plot(y1, 'ro', color='green')
    ax1.plot(y2, 'ro', color='red')
    ax1.set_xlabel("Simulation round")
    ax1.set_ylabel("E[T] - response time")
    ax1.grid(b=True, which='major', color='#CCCCCC', linestyle='-')
    pyplot.show()

    # plotting the response time
    f, ax = pyplot.subplots()
    ax.hist(y1, color='green', bins=10, histtype='step', linewidth=10, density=True, cumulative=False)
    ax.hist(y2, color='red', bins=10, histtype='step', linewidth=10, density=True, cumulative=False)
    ax.set_xlabel("E[T] - response time")
    ax.set_ylabel("PDF")
    ax.set_xbound(14, 76)
    ax.set_ybound(0, 0.2)
    ax.grid(b=True, which='major', color='#CCCCCC', linestyle='-')
    pyplot.show()
    # pyplot.savefig("fig1.png")
