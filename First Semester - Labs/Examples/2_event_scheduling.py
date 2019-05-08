#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7

from queue import Queue, PriorityQueue
from runstats import Statistics
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

        # Statistics of the waiting time
        self.response_time = Statistics()

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

    # get the first element from the queue
    client = server.waiting_line.get()

    # save statistics of the waiting time
    server.response_time.push(time - client.arrival_time)

    # see whether there are more clients to in the line
    if not server.waiting_line.empty():

        # TODO: sample the service time
        service_time = 5

        # schedule when the client will finish the server
        FES.put((time + service_time, "departure"))

    else:
        server.idle = True

# ******************************************************************************
# the "main" of the simulation - this is the ``Event Scheduling'' approach
# ******************************************************************************


if __name__ == '__main__':

    # initialize the entities
    server = Server()

    # the time control
    time = 0

    # list of events to simulate
    FES = PriorityQueue()

    # initialize the FES
    FES.put((0.0, "arrival"))

    # simulate until the simulated time reaches a stop condition
    while time < 1000:

        (time, event_type) = FES.get()

        if event_type == "arrival":
            arrival(time, FES, server)

        elif event_type == "departure":
            departure(time, FES, server)

    # print global statistics
    print("Average response time: \t %.3f" % server.response_time.mean())
    print("Stddev response time:  \t %.3f" % server.response_time.stddev())
