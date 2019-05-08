#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7

import simpy
import numpy
import random

from runstats import Statistics

import matplotlib.pyplot as pyplot

# *******************************************************************************
# Constants
# *******************************************************************************
RANDOM_SEED = 43
SIM_TIME = 10000

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
        self.env.stats.append((self.env.now, self.env.now - time_arrival))

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

    env = simpy.Environment()

    # save stats
    env.stats = []

    # queues
    env.queues = [Servers(env, SERVERS, mu) for i in range(0, QUEUES)]

    # start the arrival process
    env.process(arrival(env, lambd))

    # simulate until SIM_TIME
    env.run(until=SIM_TIME)

    return env.stats


# *******************************************************************************
# main
# *******************************************************************************
if __name__ == '__main__':

    random.seed(RANDOM_SEED)

    # here we are simulating for a fix pair of parameters
    mu = 0.05  # 20 s per customers, thus 0.05 customer/s
    lambd = 1.5 * mu

    # ***************************************************************************
    # First Case: 1 Queue, 3 servers
    # ***************************************************************************
    x1, y1 = zip(*simulate(1, 3))

    # ***************************************************************************
    # Second Case: 3 Queue, 1 servers
    # ***************************************************************************
    x2, y2 = zip(*simulate(3, 1))

    f1, ax1 = pyplot.subplots()
    ax1.plot(x1, y1, 'ro', color='green')
    ax1.plot(x2, y2, 'ro', color='red')
    ax1.set_xlabel("Simulated time")
    ax1.set_ylabel("Response time")
    ax1.grid(b=True, which='major', color='#CCCCCC', linestyle='-')
    pyplot.show()

    # plotting the response time
    f, ax = pyplot.subplots()
    ax.hist(y1, bins=1000, histtype='step', density=True, cumulative=True)
    ax.hist(y2, bins=1000, histtype='step', density=True, cumulative=True)
    ax.set_xlabel("Response time")
    ax.set_ylabel("CDF")
    ax.set_xbound(0, 150)
    ax.set_ybound(0, 1)
    ax.grid(b=True, which='major', color='#CCCCCC', linestyle='-')
    pyplot.show()
    # pyplot.savefig("fig1.png")
