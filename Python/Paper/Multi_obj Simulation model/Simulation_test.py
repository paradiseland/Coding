# import random
import simpy
from random import randint
# # -find available v, **queue**

# # back to I/O **lift queue**

# # go to storage place  **lift queue**


# def storage_arrive(env, sim_time, lambda_s):
#     while env.now < sim_time:
#         generate_time = 60 / lambda_s
#         category = random.sample(range(1, 5), 1)
#         print('env.now: {:.1f}\nstorage C{} arrived at {:.1f}s'.format(env.now, category, env.now + generate_time))
#         yield env.timeout(generate_time)

# # def good(env):




# if __name__ == "__main__":
#     env = simpy.Environment()
#     lambda_s = 50
#     sim_time = 60
#     env.process(storage_arrive(env,sim_time ,lambda_s))
#     env.run()

# class School:
#     """
#     queue: 8 .
#     """
#     def __init__(self, env):
#         self.env = env
#         self.class_ends = env.event()
#         # queue: SimTime, EventPriority, int, Event
#         self.pupil_procs = [env.process(self.pupil()) for i in range(3)]
#         self.bell_proc = env.process(self.bell())
#     def bell(self):
#         for i in range(2):
#             yield self.env.timeout(45)
#             self.class_ends.succeed()
#             self.class_ends = self.env.event()
#             print('bell')
#     def pupil(self):
#         for i in range(2):
#             print(r' \o/', end='')
#             yield self.class_ends

# env = simpy.Environment()
# school = School(env)
# env.run()

# class EV:
#     def __init__(self, env):
#         self.env = env
#         self.drive_proc = env.process(self.drive(env))
#         self.bat_ctrl_proc = env.process(self.bat_ctrl(env))
#         self.bat_ctrl_reactivate = env.event()


#     def drive(self, env):
#         while True:
#         # Drive for 20-40 min
#             yield env.timeout(randint(20, 40))
#             # Park for 1-6 hours
#             print('Start parking at', env.now)
#             self.bat_ctrl_reactivate.succeed() # "reactivate"
#             self.bat_ctrl_reactivate = env.event()
#             yield env.timeout(randint(60, 360))
#             print('Stop parking at', env.now)

#     def bat_ctrl(self, env):
#         while True:
#             print('Bat. ctrl. passivating at', env.now)
#             yield self.bat_ctrl_reactivate # "passivate"
#             print('Bat. ctrl. reactivated at', env.now)
#             yield env.timeout(randint(30, 90))

# env = simpy.Environment()
# ev = EV(env)
# env.run(until=500)


# class EV:
#     def __init__(self, env):
#         self.env = env
#         self.drive_proc = env.process(self.drive(env))

#     def drive(self, env):
#         while True:
#         # Drive for 20-40 min
#             yield env.timeout(randint(20, 40))

#     # Park for 1 hour
#             print('Start parking at', env.now)
#             charging = env.process(self.bat_ctrl(env))
#             parking = env.timeout(60)
#             yield charging | parking
#             if not charging.triggered:
#             # Interrupt charging if not already done.
#                 charging.interrupt('Need to go!')
#             print('Stop parking at', env.now)

#     def bat_ctrl(self, env):
#         print('Bat. ctrl. started at', env.now)
#         try:
#             yield env.timeout(randint(60, 90))
#             print('Bat. ctrl. done at', env.now)
#         except simpy.Interrupt as i:
#     # Onoes! Got interrupted before the charging was done.
#             print('Bat. ctrl. interrupted at', env.now, 'msg:',
#     i.cause)

# env = simpy.Environment()
# ev = EV(env)
# env.run(until=100)


# - Condition events
# Scenario:
# A counter with a random service time and customers who renege. Based on the
# program bank08.py from TheBank tutorial of SimPy 2. (KGM)

import random
import simpy

RANDOM_SEED = 42
NEW_CUSTOMERS = 5 # Total number of customers
INTERVAL_CUSTOMERS = 10.0 # Generate new customers roughly every x seconds
MIN_PATIENCE = 1 # Min. customer patience
MAX_PATIENCE = 3 # Max. customer patience


def source(env, number, interval, counter):
    """Source generates customers randomly"""
    for i in range(number):
        c = customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)


def customer(env, name, counter, time_in_bank):

    """Customer arrives, is served and leaves."""
    arrive = env.now
    print('%7.4f %s: Here I am' % (arrive, name))
    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(patience)
        wait = env.now - arrive
        if req in results:
            # We got to the counter
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))
            tib = random.expovariate(1.0 / time_in_bank)
            yield env.timeout(tib)
            print('%7.4f %s: Finished' % (env.now, name))
        else:
            # We reneged
            print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))
# Setup and start the simulation
print('Bank renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()
counter = simpy.Resource(env, capacity=1)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()
