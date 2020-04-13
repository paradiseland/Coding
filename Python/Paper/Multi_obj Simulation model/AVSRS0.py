import simpy
import random

class warehouse:
    def __init__(self, env, lift, vehicle):
        self.env = env
        self.lambda_s = 50
        self.proc = env.process(self.source(env, lift, vehicle))


    def source(self, env, lift, vehicle):
        ind = 0
        while True:
            ind += 1
            g = self.good(env, "good {}".format(ind), lift, vehicle)
            env.process(g)
            t_arrive = random.expovariate(1/(60/self.lambda_s))
            yield env.timeout(t_arrive)
    

    def good(self, env, name, lift, vehicle):
        """
        good arrives, is lifted and transported to the storage place.
        """
        timepoint_arrive = env.now
        print("{:6.3f}, \033[1;31m{}\33[0m arrives".format(timepoint_arrive, name))
        with vehicle.request() as req_veh:
            yield req_veh
            wait_vehicle = env.now - timepoint_arrive
            print("{:6.3f}, {} waits for vehicle for {:6.3f}s".format(env.now, name, wait_vehicle))
            with lift.request() as req:
                yield req
                wait_liftdown = env.now - timepoint_arrive
                print("{:6.3f}, {} waits for lift for {:6.3f}s".format(env.now, name, wait_liftdown))
                time_lifted1 = abs(random.gauss(2, 1))
                yield env.timeout(time_lifted1)
                print("{:6.3f}, {} gets lifted for {:6.3f}s".format(env.now, name, time_lifted1))

        trans_time = env.now - timepoint_arrive
        print("{:6.3f}, {} gets transported for {:6.3f} s\n\033[1;32m{} FINISHED \33[0m ".format(env.now, name, trans_time, name.upper()))
            


        # with lift.request() as req2:
        #     result_lift2 = yield req2
        #     wait = env.now - timepoint_arrive
        #     print("{:6.3f}, {} waits for vehicle for {}s".format(env.now, name, wait))
        #     time_lifted1 = yield env.timeout(random.gauss(5, 1))
        #     print("{:6.3f}, {} get lifted, takes {} s ".format(env.now, name, time_lifted1))








if __name__ == "__main__":
    env = simpy.Environment()
    lift = simpy.Resource(env, capacity= 1)
    vehicle = simpy.Resource(env, capacity=1)
    war = warehouse(env, lift, vehicle)
    env.run(until = 100)
