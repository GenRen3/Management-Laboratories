#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7

import simpy
import numpy
import random
from runstats import Statistics
import matplotlib.pyplot as pyplot

# *******************************************************************************
# Constants
# *******************************************************************************
RANDOM_SEED = 42
SIM_TIME = 10000
POINTS = 100

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
        #print("client", self.number, "response time", self.env.now - time_arrival)
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
    x = []
    y = []

    # we want to test the system while changing lambda
    for l in range(1, POINTS, 1):

        lambd = 2.0 * SERVERS * QUEUES * mu * l / POINTS #service at most of arrival time

        env = simpy.Environment()

        # save stats
        env.stats = Statistics()

        # queues
        env.queues = [Servers(env, SERVERS, mu) for i in range(0, QUEUES)]

        # start the arrival process
        env.process(arrival(env, lambd))

        # simulate until SIM_TIME
        env.run(until=SIM_TIME)

        # print the mean response time
        #print("%.3f %.3f %.2f" % (mu, lambd, env.stats.mean()))

        x.append(lambd / (SERVERS * QUEUES * mu))
        y.append(env.stats.mean())

    return x, y


# *******************************************************************************
# main
# *******************************************************************************
if __name__ == '__main__':

    random.seed(RANDOM_SEED)

    mu = 0.05  # 20 s per customers, thus 0.05 customer/s

    # ***************************************************************************
    # First Case: 1 Queue, 3 servers
    # ***************************************************************************
    x, y = simulate(1, 3)

    # ***************************************************************************
    # Second Case: 3 Queue, 1 servers
    # ***************************************************************************
    x, z = simulate(3, 1)

    # plotting the response time
    f, ax = pyplot.subplots()
    ax.plot(x, y, color='green', linewidth=2, label="1 queue with 3 servers")
    ax.plot(x, z, color='red', linewidth=2, label="3 queues with 1 server")
    ax.set_xlabel("lambda/(3 * mu)")
    ax.set_ylabel("E[T] - response time")
    #ax.set_xbound(0, 1)
    #ax.set_ybound(0, 200)
    ax.grid(b=True, which='major', color='#CCCCCC', linestyle='-')
    pyplot.legend()
    pyplot.show()
    # pyplot.savefig("fig1.png")
