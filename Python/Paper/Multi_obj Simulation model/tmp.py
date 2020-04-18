import random 
from random import randint as rd
import simpy 
import numpy as np


"""
only model one single area of the Warehouse
Including Storage and Retrieval.
"""

def rand_place_available(warehouse) ->list: 
    """
    Randomly storaged,  generating a randomly available place to storage by considering shape of warehouse.
    """
    st_place = 0
    while st_place == 0:
        tmp = [rd(0, i-1) for i in [warehouse.A_Z, warehouse
        .T, warehouse.B, warehouse.sides]]
        st_place = warehouse.record[tuple(tmp)]
    return [i+1 for i in tmp]

def rand_place_loaded(warehouse)->list:
    """
    Randomly retrieval,  generating a randomly loaded place to storage by considering shape of warehouse.
    """
    # i-dim
    record_1d = warehouse.record.reshape(warehouse.containers)
    loaded_index :tuple = np.where(record_1d==0)
    choose = np.random.choice(loaded_index[0], 1)
    record_1d[choose[0]] = -1
    record_nd = record_1d.reshape(warehouse.shape)
    tmp = np.where(record_nd ==-1)
    return [tmp[i][0]+1 for i in range(len(tmp))]

def get_available_closest(departure, destination, lift, fleet) -> 'index of chosen':
    """
    Only called when there is more than 1 vehicles available.
    By considering the *Bay* place of each vehicle, get the closest place[last destination] to the lift.
    when system has same *Bay*, choosee the lower vehicle.
    """
    # lift_place: [int((A_Z-1)/2+1),T, 0, 0]
    # closest: B+delta(T)
    
    state = [i.state for i in fleet.vehicles]
    T_lift = lift.tier
    
    available = [i.state == 1 for i in fleet.vehicles]
    vehs_bay = [i.place[2] for i in fleet.vehicles]
    # ΔT between vehicle and Lift.
    veh_delta_tier = [abs(T_lift-i.place[1]) for i in fleet.vehicles]

    if len(set(vehs_bay)) == 1:
        if sum(available) > 1:
            closest = veh_delta_tier.index(min(veh_delta_tier))
        else:
            assert('there is no more than 1 vehicle available')
    else:
        closest = vehs_bay.index(min(vehs_bay))

    return closest

class Warehouse:
    """
    define a Warehouse class to get available place and save parameters.
    """
    def __init__(self, A_Z, T, B, sides):
       self.A_Z = A_Z
       self.T = T
       self.B = B
       self.sides = sides
       self.shape = (self.A_Z, self.T, self.B, self.sides)
       self.coe_length :(A, T, B)= dict(zip(['width_of_asile', 'height_tier', 'bay'], [width_of_asile, height_tier, bay]))
       self.containers = self.A_Z*self.T*self.B*self.sides
       self.record = np.ones(self.shape)

    @property
    def available_num(self):
        return sum(sum(self.record.reshape((1, -1)) == 1))
        
    def store(self, place:tuple):
        self.record[place] == 0
    
    def retrieve(self, place:tuple):
        self.record[place] == 1

    def init_warehouse(self):
        tmp = np.ones(self.containers)
        ind = np.arange(self.containers)
        random_choose = np.random.choice(ind, int(len(ind)/2), replace = False).tolist()
        for i in random_choose:
            tmp[i] = 0
        self.record = tmp.reshape(self.shape)


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
        self.G = weight[0] * g


    def busy(self, chosen, dest, type_transaction):
        # STORE:type_transaction = 0 ; RETRIEVAL:type_transaction = 1
        if type_transaction == 0:
            index_vehicle = chosen
            self.destination = dest
        else:
            self.destination = [0, 0, 0, 0]
        self.state = 0

    def release(self, dest):
        self.palce = dest
        self.state = 1
    
    @property
    def D_sign(self):
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


class Fleet:
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




class Lift:
    """
    define a lift class to get available lift and save a queue of lift.
    """

    def __init__(self, acc, vmax):
        # busy:0 idle:1
        self.state = 1
        self.tier = 0
        self.ACC = self.DEC = acc
        self.V_MAX = vmax

    
    def busy(self, dest):
        self.tier = dest
        
        self.state = 0

    def release(self, dest):
        self.state = 1
        self.tier = dest[1]

    @property
    def D_sign(self):
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


class Simulation:
    def __init__(self, env, lift, fleet, lift_re, veh_re, warehouse):

        self.env = env

        self.S = env.process(self.source_storage(env, lift, fleet, lift_re, veh_re))

        self.R = env.process(self.source_retrieval(env, lift, fleet, lift_re, veh_re))
    

    def source_storage(self, env, lift, fleet, lift_re, veh_re):
        """
        In simulation time, keeping register [Storage] process into the simulation environment.
        """
        ind_s = 0
        while True:
            ind_s += 1
            gs = self.good_store(env, f'STORAGE {ind_s}', lift, fleet, lift_re, veh_re,warehouse)
            env.process(gs)
            t_arrive_storage = random.expovariate(lambda_ZS)
            yield env.timeout(t_arrive_storage)


    def good_store(self, env, name, lift, fleet, lift_re, veh_re, warehouse):
        """
        good arrives, is lifted and transported to the storage place.
        Procedure:
        *****--------REQUEST: Vehicle --------********
        1. Arrived storage seizes an available vehicle.
        2. Vehicle travels to lift. [can be omitted]  
        *****--------REQUEST: Lift------------********
        3. Lift travels to vehicle's tier [can be omitted]  
        4. Lift travels to I/O. [can be omitted] 
        5. Lift travels to tier of storage. [can be omitted]
        *****--------RLEASE: Lift-------------********
        6. Vehicle travels to storage.
        *****--------RELease: Vehicle -------*********
        """
        
        timepoint_arrive = env.now
        print("{:6.3f}, \033[1;31m{}\33[0m arrives".format(timepoint_arrive, name))
        yield env.timeout(0)

        dest = rand_place_available(warehouse)
        warehouse.store(dest)
        print(f'Place of  {name} is at{dest}')


        # 解决方案：
        # 设置一个列表来表示资源， 对资源的 Veh.users长进行判断  len(Veh.users) 返回队长列表： [len(i.users) for i in veh_re]
        len_of_queue = [len(i.users) for i in veh_re]
        num_of_busy = [i>0 for i in len_of_queue]
        num_of_idle = [i==0 for i in len_of_queue]

        if sum(num_of_idle) > 1:
            # find the closest available vehicle
            v = get_available_closest(IO, dest, lift, fleet)

        elif sum(num_of_idle) == 1:
            v = num_of_idle.index(True)

        else:
            # 对多个车建一个排队队列
            v = len_of_queue.index(min(len_of_queue))
            # *******同时在下一个事件来临时，更新掉这个队列，即撤回需求，重新判断再添加需
        with veh_re[v].request() as req_veh:
            yield req_veh
            print("{:6.3f}, \033[1;31m{}\33[0m seized vehicle {}, vehicle place is at {}".format(env.now, name, v+1, fleet.vehicles[v].place))
            fleet.vehicles[v].busy(v, dest, 0)

            if fleet.vehicles[v].place[1] > 1:
                travel_to_lift = fleet.vehicles[v].get_transport_time(fleet.vehicles[v].place[2])
                yield env.timeout(travel_to_lift)
                print("{:6.3f}, \033[1;35m vehicle {} \33[0m travels to lift. ".format(env.now, v+1))
                
                with lift_re.request() as req_lift:
                    yield req_lift

                    lift_to_vehicle_tier = lift.get_transport_time(abs(lift.tier - fleet.vehicles[v].place[1]))
                    lift.busy(fleet.vehicles[v].place[1])

                    yield env.timeout(lift_to_vehicle_tier)
                    print("{:6.3f}, \033[1;31m lift \33[0m travels to vehicle's tier".format(env.now))

                    travel_to_IO = lift.get_transport_time(fleet.vehicles[v].place[1])
                    yield env.timeout(travel_to_IO)
                    print("{:6.3f}, \033[1;33m lift  \33[0m travels to I/O. ".format(env.now))
                    
                    yield env.timeout(0)
                    print("{:6.3f}, \033[1;33m vehicle{}  \33[0m charges the load.".format(env.now, v+1))
                    
                    if dest[1] == 1:
                        lift.release(dest)

                    else:
                        travel_to_storage_tier = lift.get_transport_time(dest[1])
                        yield env.timeout(travel_to_storage_tier)
                        print("{:6.3f}, \033[1;33m lift \33[0m travels to storage's tier {}. ".format(env.now, dest[1]))
                        lift.release(dest)


                    travel_to_storage = fleet.vehicles[v].get_transport_time(dest[2])
                    yield env.timeout(travel_to_storage)
                    print("{:6.3f}, \033[1;33m vehicle {} \33[0m travels to storage. ".format(env.now, v+1))
            else:
                # the seized vehicle is on the first floor.
                if fleet.vehicles[v].place[1:3] == IO[1:3]:
                    if dest[1] == 1:
                        lift.release(dest)
                        travel_to_storage = fleet.vehicles[v].get_transport_time(dest[2])
                        yield env.timeout(travel_to_storage)
                        print("{:6.3f}, \033[1;33m vehicle {} \33[0m travels to storage. ".format(env.now, v+1))
                    else:
                        travel_to_storage_tier = lift.get_transport_time(dest[1])
                        yield env.timeout(travel_to_storage_tier)
                        print("{:6.3f}, \033[1;33m lift \33[0m travels to storage's tier. ".format(env.now))
                        lift.release(dest)

                        travel_to_storage = fleet.vehicles[v].get_transport_time(dest[2])
                        yield env.timeout(travel_to_storage)
                        print("{:6.3f}, \033[1;33m vehicle {} \33[0m travels to storage. ".format(env.now, v+1))
                else:
                    travel_to_IO = fleet.vehicles[v].get_transport_time(fleet.vehicles[v].place[2])
                    yield env.timeout(travel_to_IO)
                    print("{:6.3f}, \033[1;35m vehicle {} \33[0m travels to I/O. ".format(env.now, v+1))
                    if dest[1] == 1:
                        lift.release(dest)
                        travel_to_storage = fleet.vehicles[v].get_transport_time(dest[2])
                        yield env.timeout(travel_to_storage)
                        print("{:6.3f}, \033[1;33m vehicle {} \33[0m travels to storage. ".format(env.now, v+1))
                        fleet.vehicles[v].release(dest)
                    else:
                        with lift_re.request() as lift_req:
                            travel_to_storage_tier = lift.get_transport_time(dest[1])
                            yield env.timeout(travel_to_storage_tier)
                            print("{:6.3f}, \033[1;33m lift \33[0m travels to storage's tier. ".format(env.now))
                            lift.release(dest)

                        travel_to_storage = fleet.vehicles[v].get_transport_time(dest[2])
                        yield env.timeout(travel_to_storage)
                        print("{:6.3f}, \033[1;33m vehicle {} \33[0m travels to storage. ".format(env.now, v+1))
                        fleet.vehicles[v].release(dest)
                        print("{:6.3f}, \033[1;33m  {}  FINISHED \33[0m ".format(env.now,name))


    def source_retrieval(self, env, lift, fleet, lift_re, veh_re):
        """
        In simulation time, keeping register [Retrieval] process into the sim env.
        """
        ind_s = 0
        while True:
            ind_s += 1
            gr = self.good_retrieve(env, f'RETRIEVAL {ind_s}', lift, fleet, lift_re, veh_re,warehouse)
            env.process(gr)
            t_arrive_retrieval = random.expovariate(lambda_ZR)
            yield env.timeout(t_arrive_retrieval)


    def good_retrieve(self, env, name, lift, fleet, lift_re, veh_re, warehouse):
        """
        demand arrives, is lifted and transported to I/O.
        """
        timepoint_arrive = env.now
        print("{:6.3f}, \033[1;31m{}\33[0m arrives".format(timepoint_arrive, name))
        yield env.timeout(0)

        load = rand_place_loaded(warehouse)
        print(f'Place of  {name} is at{load}')


        # 解决方案：
        # 设置一个列表来表示资源， 对资源的 Veh.users长进行判断  len(Veh.users) 返回队长列表： [len(i.users) for i in veh_re]


        
        len_of_queue = [len(i.users) for i in veh_re]
        num_of_busy = [i>0 for i in len_of_queue]
        num_of_idle = [i==0 for i in len_of_queue]

        # if sum(num_of_idle) > 1:
        #     # find the closest available vehicle
        #     v = get_available_closest(IO, dest, lift, fleet)

        # elif sum(num_of_idle) == 1:
        #     v = num_of_idle.index(True)

        # else:
        #     # 对多个车建一个排队队列
        #     v = len_of_queue.index(min(len_of_queue))
        #     # *******同时在下一个事件来临时，更新掉这个队列，即撤回需求，重新判断再添加需
        # with veh_re[v].request() as req_veh:
        #     yield req_veh
        #     print("{:6.3f}, \033[1;31m{}\33[0m seized vehicle {}, vehicle place is at {}".format(env.now, name, v+1, fleet.vehicles[v].place))
        #     fleet.vehicles[v].busy(v, dest, 0)

        #     if fleet.vehicles[v].place[1] > 1:
        #         travel_to_lift = fleet.vehicles[v].get_transport_time(fleet.vehicles[v].place[2])
        #         yield env.timeout(travel_to_lift)
        #         print("{:6.3f}, \033[1;35m vehicle {} \33[0m travels to lift. ".format(env.now, v+1))
                
        #         with lift_re.request() as req_lift:
        #             yield req_lift

        #             lift_to_vehicle_tier = lift.get_transport_time(abs(lift.tier - fleet.vehicles[v].place[1]))
        #             lift.busy(fleet.vehicles[v].place[1])

        #             yield env.timeout(lift_to_vehicle_tier)
        #             print("{:6.3f}, \033[1;31m lift \33[0m travels to vehicle's tier".format(env.now))

        #             travel_to_IO = lift.get_transport_time(fleet.vehicles[v].place[1])
        #             yield env.timeout(travel_to_IO)
        #             print("{:6.3f}, \033[1;33m lift  \33[0m travels to I/O. ".format(env.now))
                    
        #             yield env.timeout(0)
        #             print("{:6.3f}, \033[1;33m vehicle{}  \33[0m charges the load.".format(env.now, v+1))
                    
        #             if dest[1] == 1:
        #                 lift.release(dest)

        #             else:
        #                 travel_to_storage_tier = lift.get_transport_time(dest[1])
        #                 yield env.timeout(travel_to_storage_tier)
        #                 print("{:6.3f}, \033[1;33m lift \33[0m travels to storage's tier {}. ".format(env.now, dest[1]))
        #                 lift.release(dest)


        #             travel_to_storage = fleet.vehicles[v].get_transport_time(dest[2])
        #             yield env.timeout(travel_to_storage)
        #             print("{:6.3f}, \033[1;33m vehicle {} \33[0m travels to storage. ".format(env.now, v+1))
        #     else:
        #         # the seized vehicle is on the first floor.
        #         if fleet.vehicles[v].place[1:3] == IO[1:3]:
        #             if dest[1] == 1:
        #                 lift.release(dest)
        #                 travel_to_storage = fleet.vehicles[v].get_transport_time(dest[2])
        #                 yield env.timeout(travel_to_storage)
        #                 print("{:6.3f}, \033[1;33m vehicle {} \33[0m travels to storage. ".format(env.now, v+1))
        #             else:
        #                 travel_to_storage_tier = lift.get_transport_time(dest[1])
        #                 yield env.timeout(travel_to_storage_tier)
        #                 print("{:6.3f}, \033[1;33m lift \33[0m travels to storage's tier. ".format(env.now))
        #                 lift.release(dest)

        #                 travel_to_storage = fleet.vehicles[v].get_transport_time(dest[2])
        #                 yield env.timeout(travel_to_storage)
        #                 print("{:6.3f}, \033[1;33m vehicle {} \33[0m travels to storage. ".format(env.now, v+1))
        #         else:
        #             travel_to_IO = fleet.vehicles[v].get_transport_time(fleet.vehicles[v].place[2])
        #             yield env.timeout(travel_to_IO)
        #             print("{:6.3f}, \033[1;35m vehicle {} \33[0m travels to I/O. ".format(env.now, v+1))
        #             if dest[1] == 1:
        #                 lift.release(dest)
        #                 travel_to_storage = fleet.vehicles[v].get_transport_time(dest[2])
        #                 yield env.timeout(travel_to_storage)
        #                 print("{:6.3f}, \033[1;33m vehicle {} \33[0m travels to storage. ".format(env.now, v+1))
        #                 fleet.vehicles[v].release(dest)
        #             else:
        #                 with lift_re.request() as lift_req:
        #                     travel_to_storage_tier = lift.get_transport_time(dest[1])
        #                     yield env.timeout(travel_to_storage_tier)
        #                     print("{:6.3f}, \033[1;33m lift \33[0m travels to storage's tier. ".format(env.now))
        #                     lift.release(dest)

        #                 travel_to_storage = fleet.vehicles[v].get_transport_time(dest[2])
        #                 yield env.timeout(travel_to_storage)
        #                 print("{:6.3f}, \033[1;33m vehicle {} \33[0m travels to storage. ".format(env.now, v+1))
        #                 fleet.vehicles[v].release(dest)
        #                 print("{:6.3f}, \033[1;33m  {}  FINISHED \33[0m ".format(env.now,name))









if __name__ == "__main__":
    A_Z = 3
    T = 4
    B = 6
    sides = 2
    lambda_all = 100/3600
    lambda_Z = lambda_all / 4
    lambda_ZS = lambda_Z/2
    lambda_ZR = lambda_Z/2
    # IO = [int((A_Z-1)/2+1),1,1,1]
    IO = [(A_Z-1)/2+1, 1, 0, 1]

    num_of_vehicles_Z = 2
    bay, width_of_asile, height_tier = 1, 3, 1.5
    weight = [100, 200, 250]

    f_r = 1.15
    c_r = 0.01
    g = 10
    eta = .9

    env = simpy.Environment()
    warehouse = Warehouse(A_Z, T, B, sides)
    warehouse.init_warehouse()
    lift =  Lift(1,1)
    fleet = Fleet(num_of_vehicles_Z, 1,1)
    lift_re = simpy.Resource(env, 1)
    veh_re = [simpy.Resource(env, 1) for i in range(num_of_vehicles_Z)]
    sim = Simulation(env, lift, fleet, lift_re, veh_re, warehouse)
    env.run(until=3600)
