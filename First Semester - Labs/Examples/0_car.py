#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7

import simpy


class Car(object):
    def __init__(self, env):
        self.env = env
        env.process(self.run())

    def run(self):
        while True:
            print('Parked at %d' % self.env.now)
            parking_time = 5

            # process() returns to wait for parking_time
            yield self.env.timeout(parking_time)

            # after the timeout the code return here
            print('Start driving at %d' % self.env.now)

            trip_duration = 2
            yield self.env.timeout(trip_duration)
            # after driving the code will return here


env = simpy.Environment(initial_time=2)
Car(env)
env.run(until=15)


# -------------------------------------------------------------------------------

exit(0)
# Behind the scenes
coroutine


class Environment(BaseEnvironment):

    def __init__(self, initial_time=0):
        self._now = initial_time
        self._queue = []  # The list of all currently scheduled events.
        self._eid = count()  # Counter for event IDs
        self._active_proc = None

    def step(self):
        """Process the next event.

        Raise an :exc:`EmptySchedule` if no further events are available.

        """
        try:
            self._now, _, _, event = heappop(self._queue)
        except IndexError:
            raise EmptySchedule()
