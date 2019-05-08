#!/usr/bin/env python3

from queue import Queue, PriorityQueue


class Slient(object):
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.departure_time = de
        pass


class Server(object):
    def __init__(self):
        pass


# function arrival
def arrival(cur_time, FES, server):
    inter_arrival = 10
    FES.put((cur_time + inter_arrival, "arrival"))
    client = client(cur_time)
    server.waiting_line.put(client)

    if server.is_iddle():
        server.make_busy()
        service_time = 10
        FES.put((cur_time + service_time, "departure"))

# function departure


def departure():
    pass


# the time control
cur_time = 0

# list of events to simulate
FES = PriorityQueue()

# initialize
FES.put((0.0, "arrival"))

# move time
while cur_time < 1000:
    (time, event_type) = FES.get()
    cur_time = time
    if event_type == "arrival":
        arrival()

    elif event_type == "departure":
        departure()
