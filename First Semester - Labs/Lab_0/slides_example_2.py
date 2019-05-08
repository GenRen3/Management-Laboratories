#!/usr/bin/env python3

import simpy
import numpy
import random

from matplotlib import pyplot

# ******************************************************************************
# Constants
# ******************************************************************************
RANDOM_SEED = 42
CAR_ARRIVAL = 2
TRUCK_ARRIVAL = 4

SIM_TIME = 10000

# ******************************************************************************
# Car arrival process
# ******************************************************************************


class VehicleArrival(object):

    # constructor
    def __init__(self, environ, vehicle, arrival_time):

        # hold samples of inter-arrival time
        self.inter_arrival = []

        self.arrival_time = arrival_time
        self.env = environ
        self.vehicle = vehicle

    # execute the process
    def arrival_process(self):
        while True:
            # sample the time to next arrival
            inter_arrival = random.expovariate(lambd=1.0/self.arrival_time)

            # yield an event to the simulator
            yield self.env.timeout(inter_arrival)

            # the car has arrived
            # save samples of the inter_arrival to calculate statistics later on
            self.inter_arrival.append(inter_arrival)

            print("The event has occurred: a", self.vehicle, "has arrived at", self.env.now)


# ******************************************************************************
# the "main" of the simulation
# ******************************************************************************
if __name__ == '__main__':

    random.seed(RANDOM_SEED)

    # ********************************
    # setup and perform the simulation
    # ********************************

    env = simpy.Environment()

    # car arrival
    car = VehicleArrival(env, "CAR", CAR_ARRIVAL)
    truck = VehicleArrival(env, "TRUCK", TRUCK_ARRIVAL)

    # start the arrival process
    env.process(car.arrival_process())
    env.process(truck.arrival_process())

    # simulate until SIM_TIME
    env.run(until=SIM_TIME)

    # *************************
    # calculate some statistics
    # *************************
    print("Average inter-arrival time for cars: ",
          numpy.mean(car.inter_arrival))
    print("Average inter-arrival time for trucks: ",
          numpy.mean(truck.inter_arrival))

    # ****************
    # plot some stuff
    # ****************

    fig, (series, pdf, cdf) = pyplot.subplots(3, 1)

    series.plot(car.inter_arrival)
    series.set_xlabel("Sample")
    series.set_ylabel("Inter-arrival")

    pdf.hist(car.inter_arrival, bins=100, normed=True)
    pdf.set_xlabel("Time")
    pdf.set_ylabel("Density")
    pdf.set_xbound(0, 15)

    cdf.hist(car.inter_arrival, bins=100, cumulative=True, normed=True)
    cdf.set_xlabel("Time")
    cdf.set_ylabel("P(Arrival time <= x)")
    cdf.set_ybound(0, 1)
    cdf.set_xbound(0, 15)

    pyplot.show()
