#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7

from queue import Queue, PriorityQueue
import random

# ******************************************************************************
# Classes representing the entities of our model
# ******************************************************************************

# Client


class Client(object):

    # constructor
    def __init__(self, at):

        # the arrival time
        self.arrival_time = at

# Server


class Server(object):

    # constructor
    def __init__(self):

        # variables of our model: the queue of "clients"
        self.waiting_line = Queue()

        # whether the server is idle or not
        self.idle = True

# ******************************************************************************
# Function implementing our events
# ******************************************************************************

# function arrival


def arrival(time, FES, server):

    # TODO: sample the time until the next event
    inter_arrival = 10

    # schedule the next arrival
    FES.put((time + inter_arrival, "arrival"))

    # create a record for the client
    client = Client(time)

    # insert the record in the queue
    server.waiting_line.put(client)

    # if the server is idle start the service
    if server.idle:
        server.idle = False

        # TODO: sample the service time
        service_time = 5

        # schedule when the client will finish the server
        FES.put((time + service_time, "departure"))

# function departure


def departure(time, FES, server):

    # TODO: Complete this function
    pass


# ******************************************************************************
# the "main" of the simulation - this is the ``Event Scheduling'' approach
# ******************************************************************************

if __name__ == '__main__':

    # the time control
    time = 0

    # list of events to simulate
    FES = PriorityQueue()

    # initialize the FES
    FES.put((0.0, "arrival"))

    # initialize the entities
    server = Server()

    # simulate until the simulated time reaches a stop condition
    while time < 1000:

        (time, event_type) = FES.get()

        if event_type == "arrival":
            arrival(time, FES, server)

        elif event_type == "departure":
            departure(time, FES, server)
