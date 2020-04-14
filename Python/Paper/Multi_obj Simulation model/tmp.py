import simpy 
import random 
from random import randint as rd

"""
only model one single area of the Warehouse
Including Storage and Retrieval.
"""

def rand_place(): 
    return [rd(1, i) for i in [A_Z, T, B, sides]]


def get_available_closest(departure, destination, lift, fleet):
    # lift_place: [int((A_Z-1)/2+1),T, 0, 0]
    # closest: B+delta(T)
    state = [i.state for i in fleet.vehicles]
    T_lift = lift.tier
    closest = 0
    tmp = [10000]*4
    for ind, st in enumerate(state):
        if st == 1:
            # distance between lift and vehicle: B + ΔT

            if fleet.vehicles[ind].place[1]-T_lift + fleet.vehicles[ind].place[2] < tmp[1]-T_lift+tmp[2]:
                tmp = fleet.vehicles[ind].place
                closest = ind
    return closest

class Vehicle:
    """
    define a Vehicle class to get place, availability and operation of each vehicle.
    """

    def __init__(self, acc, vmax):
        self.place = [0, 0, 0, 0]
        # A, B, T, one side
        self.destination = [0, 0, 0, 0]
        # busy: 0 idle:1
        self.state = 1
        self.ACC = self.DEC = acc
        self.V_MAX = vmax
        self.D_sign = self.get_Dsign()
        self.G = weight[0] * g

    def __enter__(self):
        self.state = 0
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.state = 1



    def busy(self, chosen, dest, type_transaction):
        # STORE:type_transaction = 0 ; RETRIEVAL:type_transaction = 1
        if type_transaction == 0:
            index_vehicle = chosen
            self.destination = dest
        else:
            self.destination = [0, 0, 0, 0]
        self.state = 0

    def release(self):
        self.palce = self.destination
        self.state = 1

    def get_Dsign(self):
        return self.V_MAX**2/self.ACC

    def get_transport_time(self, Dis):
        t1, t2, vtop = self.get_transport_time_vtop(Dis)
        return 2*t1+t2

    def get_transport_time_vtop(self, Dis):
        # two scenario: place to lift; lift to place.
        # return t1 & t_2
        if Dis < self.D_sign:
            return (Dis/self.ACC)**.5, 0, (self.ACC*Dis)**.5
        else:
            return self.V_MAX/self.ACC, (Dis - self.V_MAX**2/self.ACC)/self.V_MAX, self.V_MAX

    def get_energy(self):
        """
        Compute work of a single journey 
        """
        t1, t2, v_top = self.get_transport_time_vtop()
        W_VA = ((self.G*c_r + self.G/g*self.ACC*f_r) * v_top / (1000*eta))*t1
        W_VD = ((self.G/g*self.DEC*f_r - self.G*c_r) * v_top / (1000*eta))*t1
        W_VC = self.G*c_r*v_top/(1000*eta)*t2
        return W_VA, W_VD, W_VC

    def regenerate_energy(self):
        t1, t2, v_top = self.get_transport_time_vtop()
        RW_v = (self.G/g*self.DEC*f_r - self.G*c_r)*v_top**2/(2*self.DEC) *2.78*1e-7
        return RW_v


class Fleet():
    """
    define a Fleet class to get state of fleet and get a available vehicle
    """

    def __init__(self, num, acc, vmax):
        self.num = num
        self.coord = [[0, 0, 0, 0] for i in range(self.num)]
        self.vehicles = [Vehicle(acc, vmax) for i in range(self.num)]

    def num_idle(self):
        state = [i.state for i in self.vehicles]
        return state.count(1)




class Lift():
    """
    define a lift class to get available lift and save a queue of lift.
    """

    def __init__(self, acc, vmax):
        # busy:0 idle:1
        self.state = 1
        self.tier = 0
        self.ACC = self.DEC = acc
        self.V_MAX = vmax
        self.D_sign = self.get_Dsign()
    
    def busy(self):
        
        self.state = 0

    def release(self, dest):
        self.state = 1
        self.tier = dest[1]

    def get_Dsign(self):
        return self.V_MAX**2/self.ACC

    def get_transport_time(self, Dis):
        t1, t2, vtop = self.get_transport_time_vtop(Dis)
        return 2*t1+t2
    def get_transport_time_vtop(self, Dis):
        # two scenario: place to lift; lift to place.
        # return t1 & t_2
        if Dis < self.D_sign:
            return (Dis/self.ACC)**.5, 0, (self.ACC*Dis)**.5
        else:
            return self.V_MAX/self.ACC, (Dis - self.V_MAX**2/self.ACC)/self.V_MAX, self.V_MAX

    def get_energy(self):
        """
        Compute work of a single journey 
        """
        t1, t2, v_top = self.get_transport_time_vtop()
        W_VA = ((self.G + self.G/g*self.ACC*f_r) * v_top / (1000*eta))*t1
        W_VD = ((self.G/g*self.DEC*f_r + self.G) * v_top / (1000*eta))*t1
        W_VC = self.G*v_top/(1000*eta)*t2
        return W_VA, W_VD, W_VC

    def regenerate_energy(self):
        t1, t2, v_top = self.get_transport_time_vtop()
        RW_v = (self.G/g*self.DEC*f_r + self.G)*v_top**2/(2*self.DEC) *2.78*1e-7
        return RW_v





class Simulation():
    def __init__(self, env, lift, fleet, lift_re, veh_re):
        self.env = env
        self.S = env.process(self.source_storage(env, lift, fleet, lift_re, veh_re))
        # self.R = env.process()
    

    def source_storage(self, env, lift, fleet, lift_re, veh_re):
        ind_s = 0
        while True:
            ind_s += 1
            gs = self.good_store(env, f'STORAGE {ind_s}', lift, fleet, lift_re, veh_re)
            env.process(gs)
            t_arrive_storage = random.expovariate(lambda_ZS)
            yield env.timeout(t_arrive_storage)


    def good_store(self, env, name, lift, fleet, lift_re, veh_re):
        """
        good arrives, is lifted and transported to the storage place.
        """
        timepoint_arrive = env.now
        print("{:6.3f}, \033[1;31m{}\33[0m arrives".format(timepoint_arrive, name))
        
        dest = rand_place()

        if sum([v.queue == [] for v in veh_re]) >= 1:
            pass
            print('into the condition')
            v = get_available_closest(rand_place, dest, lift, fleet)

        elif sum([v.queue == [] for v in veh_re]) == 1:
            
            v = [v.queue == [] for v in veh_re].index(True)

        elif sum([v.queue == [] for v in veh_re]) == 0:
            pass


        # with veh_re[v].request as req:






        
        if fleet.num_idle() > 0:
            # yield env.event()
            v = get_available_closest(IO, dest, lift, fleet)
            print("{:6.3f}, \033[1;31m{}\33[0m seized vehicle {}".format(env.now, name, v+1))
            fleet.vehicles[v].busy(v, dest, 0)
            if fleet.vehicles[v].place[1] > 1:
                travel_to_lift = fleet.vehicles[v].get_transport_time(fleet.vehicles[v].place[2])
                yield env.timeout(travel_to_lift)
                print("{:6.3f}, \033[1;35m vehicle {} \33[0m travels to lift. ".format(env.now, v+1))
                if lift.state == 1:
                    lift.busy(IO)
                    lift_to_vehicle_tier = lift.get_transport_time(abs(lift.tier - fleet.vehicles[v].place[2]))
                    yield env.timeout(lift_to_vehicle_tier)
                    print("{:6.3f}, \033[1;31m lift \33[0m travels to vehicle's tier".format(env.now))


                    travel_to_IO = lift.get_transport_time(fleet.vehicles[v].place[1])
                    yield env.timeout(travel_to_IO)
                    print("{:6.3f}, \033[1;33m lift  \33[0m travels to I/O. ".format(env.now))
            elif fleet.vehicles[v].place == IO:
                if lift.state == 1:
                    lift.busy()
            
            else:
                travel_to_lift = fleet.vehicles[v].get_transport_time(fleet.vehicles[v].place[2])
                yield env.timeout(travel_to_lift)
                print("{:6.3f}, \033[1;33m vehicle {} \33[0m travels to I/O. ".format(env.now, v+1))


            if dest[1] == 1:
                lift.release(dest)
                travel_to_storage = fleet.vehicles[v].get_transport_time(dest[2])
                yield env.timeout(travel_to_storage)
                print("{:6.3f}, \033[1;33m vehicle {} \33[0m travels to storage. ".format(env.now, v+1))
                fleet.vehicles[v].release()
            else:
                
                travel_to_storage_tier = lift.get_transport_time(dest[1])
                yield env.timeout(travel_to_storage_tier)
                lift.release(dest)
                travel_to_storage = fleet.vehicles[v].get_transport_time(dest[2])
                yield env.timeout(travel_to_storage)
                print("{:6.3f}, \033[1;33m vehicle {} \33[0m travels to storage. ".format(env.now, v+1))
                fleet.vehicles[v].release()


        # with fleet.request() as req_veh:
        #     yield req_veh
        #     wait_vehicle = env.now - timepoint_arrive
        #     print("{:6.3f}, {} waits for vehicle for {:6.3f}s".format(env.now, name, wait_vehicle))
        #     with lift.request() as req:
        #         yield req
        #         wait_liftdown = env.now - timepoint_arrive
        #         print("{:6.3f}, {} waits for lift for {:6.3f}s".format(env.now, name, wait_liftdown))
        #         time_lifted1 = abs(random.gauss(2, 1))
        #         yield env.timeout(time_lifted1)
        #         print("{:6.3f}, {} gets lifted for {:6.3f}s".format(env.now, name, time_lifted1))

        # trans_time = env.now - timepoint_arrive
        # print("{:6.3f}, {} gets transported for {:6.3f} s\n\033[1;32m{} FINISHED \33[0m ".format(env.now, name, trans_time, name.upper()))











if __name__ == "__main__":
    A_Z = 3
    T = 4
    B = 6
    sides = 2
    lambda_all = 100/3600
    lambda_Z = lambda_all / 4
    lambda_ZS = lambda_Z/2
    lambda_ZR = lambda_Z/2
    IO = [int((A_Z-1)/2+1),0,0,0]
    num_of_vehicles_Z = 2
    bay, width_of_asile, height_tier = 1, 3, 1.5
    weight = [100, 200, 250]

    f_r = 1.15
    c_r = 0.01
    g = 10
    eta = .9

    env = simpy.Environment()
    lift =  Lift(1,1)
    fleet = Fleet(num_of_vehicles_Z, 1,1)
    lift_re = simpy.Resource(env, 1)
    veh_re = [simpy.Resource(env, 1) for i in range(num_of_vehicles_Z)]
    sim = Simulation(env, lift, fleet, lift_re, veh_re)
    env.run(until=3600)
