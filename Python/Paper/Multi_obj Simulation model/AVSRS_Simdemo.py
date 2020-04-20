import simpy
import random

class warehouse:
    def __init__(self, env, lift, vehicle):
        self.env = env
        self.lambda_s = 50
        self.s = env.process(self.source_store(env, lift, vehicle))
        self.r = env.process(self.source_retrieval(env, lift, vehicle))


    def source_store(self, env, lift, vehicle):
        ind_s = 0
        while True:
            ind_s += 1
            g_s = self.good_store(env, "STORE {}".format(ind_s), lift, vehicle)
            env.process(g_s)
            t_arrive_storage = random.expovariate(1/(60/self.lambda_s))
            yield env.timeout(t_arrive_storage)
            
            

    def source_retrieval(self, env, lift, vehicle):
        ind_r = 0
        while True:
            ind_r += 1
            g_r = self.good_retrieval(env, "RETRIEVAL {}".format(ind_r), lift, vehicle)
            env.process(g_r)
            t_arrive_retrieval = random.expovariate(1/(60/self.lambda_s))
            yield env.timeout(t_arrive_retrieval)


    def good_store(self, env, name, lift, vehicle):
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

    def good_retrieval(self, env, name, lift, vehicle):
        """
        good arrives, is lifted and transported to the I/O.
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
