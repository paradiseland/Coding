import random
from random import randint as rd
import simpy
import numpy as np
from read_config import *

"""
Only model one single area of the Warehouse
Including Storage and Retrieval.
"""


def rand_place_available(warehouse) -> list:
    """
    Randomly storaged,  generating a randomly available place to storage by considering shape of warehouse.
    """
    # 1: vacant; 0: occupied
    st_place = 0
    while st_place == 0:
        tmp = [rd(0, i-1) for i in warehouse.shape]
        st_place = warehouse.record[tuple(tmp)]
    return [i+1 for i in tmp]


def rand_place_loaded(warehouse) -> list:
    """
    Randomly retrieval,  generating a randomly loaded place to retrieve by considering shape of warehouse.
    """
    # i-dim
    record_1d = warehouse.record.reshape(warehouse.containers)
    loaded_index: tuple = np.where(record_1d == 0)
    choose = np.random.choice(loaded_index[0], 1)
    record_1d[choose[0]] = -1
    record_nd = record_1d.reshape(warehouse.shape)
    tmp = np.where(record_nd == -1)

    return [tmp[i][0]+1 for i in range(len(tmp))]


def get_available_closest(warehouse, lift, fleet) -> 'index of chosen':
    """
    Only called when there is more than 1 vehicles available.
    By considering the *Bay* place of each vehicle, get the closest place[last destination] to the lift.
    when system has same *Bay*, choose the lower tier vehicle.
    """
    # lift_place: [int((A_Z-1)/2+1),T, 0, 0]
    state = [i.state for i in fleet.vehicles]
    T_lift = lift.tier

    available = [i.state == 1 for i in fleet.vehicles]
    vehs_to_lift = [i.place[2]*warehouse.coe_length['bay'] +
                    abs(IO[0]-i.place[0])*warehouse.coe_length['width_of_aisle'] for i in fleet.vehicles]
    # ΔT between vehicle and Lift.
    veh_delta_tier = [abs(T_lift-i.place[1]) for i in fleet.vehicles]
    veh_tiers = [i.place[1] for i in fleet.vehicles]
    if T_lift in veh_tiers:
        # there is no less than 1 vehicle in the tier of lift.
        if sum([T_lift == i for i in veh_tiers]) > 1:
            # gt 1 vehicle is in the same tier of lift.
            same_tier = [ind for ind, st in enumerate(
                veh_tiers) if st == T_lift]
            vehs_to_lift = [fleet.vehicles[i].place[2]*warehouse.coe_length['bay'] +
                            abs(IO[0]-fleet.vehicles[i].place[0])*warehouse.coe_length['width_of_aisle'] for i in same_tier]
            if len(set(vehs_to_lift)) == 1:
                closest = state.index(1)
            else:
                closest = same_tier[vehs_to_lift.index(min(vehs_to_lift))]
        else:
            # only 1 available in the same tier of lift.
            closest = veh_tiers.index(T_lift)
    else:
        # all vehicles are in different tiers from that of lift.
        closest = veh_delta_tier.index(min(veh_delta_tier))

    return closest


class Warehouse:
    """
    Define a Warehouse class to get an available place and to save parameters of warehouse configuration.
    """

    def __init__(self, A_Z, T, B, sides):
       self.A_Z = A_Z
       self.T = T
       self.B = B
       self.sides = sides
       self.shape = (self.A_Z, self.T, self.B, self.sides)
       self.coe_length: (A, T, B) = dict(
           zip(['width_of_aisle', 'height_tier', 'bay'], [width_of_aisle, height_tier, bay]))
       self.containers = self.A_Z*self.T*self.B*self.sides
       self.record = np.ones(self.shape)
       self.num_of_transactions = 0
       self.EC = []

    @property
    def available_num(self):
        return sum(sum(self.record.reshape((1, -1)) == 1))

    def store(self, place: tuple):
        self.record[place] = 0
        self.num_of_transactions += 1

    def retrieve(self, place: tuple):
        self.record[place] = 1
        self.num_of_transactions += 1

    def record_consuption_tranaction(self, vehicle, lift):
        self.EC.append(vehicle.energy + lift.energy)


    def init_warehouse(self):
        tmp = np.ones(self.containers)
        ind = np.arange(self.containers)
        random_choose = np.random.choice(
            ind, int(self.containers/2), replace=False).tolist()
        for i in random_choose:
            tmp[i] = 0
        self.record = tmp.reshape(self.shape)
    
    @property
    def get_EC(self):
        return  self.EC/self.num_of_transactions

class Vehicle:
    """
    Define a Vehicle class to get place, availability and operation of each vehicle.
    """

    def __init__(self, vmax, acc):
        self.place = IO
        self.destination = IO
        # busy: 0 idle:1
        self.state = 1
        self.ACC = self.DEC = acc
        self.V_MAX = vmax
        self.weight = 100
        self.G = (weight+self.weight) * g
        self.this_consumption = 0
        self.consumption = []
        self.busytime = []

    def busy(self, dest):
        self.this_consumption = 0
        self.destination = dest
        self.state = 0

    def release(self, dest, work_time):
        self.place = dest
        self.state = 1
        self.busytime.append(work_time)

    @property
    def D_sign(self):
        return self.V_MAX**2/self.ACC

    def get_transport_time(self, Dis):
        t1, t2, vtop = self.get_transport_time_vtop(Dis)
        self.this_consumption += self.get_energy(Dis) - self.regenerate_energy(Dis)
        return 2*t1+t2

    def get_transport_time_vtop(self, Dis):
        # two scenario: place to lift; lift to place.
        # return t1 & t_2
        if Dis < self.D_sign:
            return (Dis/self.ACC)**.5, 0, (self.ACC*Dis)**.5
        else:
            return self.V_MAX/self.ACC, (Dis - self.V_MAX**2/self.ACC)/self.V_MAX, self.V_MAX

    def get_energy(self, Dis):
        """
        Compute work of a single journey.
        """
        t1, t2, v_top = self.get_transport_time_vtop(Dis)
        W_VA = ((self.G*c_r + self.G/g*self.ACC*f_r) * v_top / (1000*eta))*t1/3600
        W_VD = ((self.G/g*self.DEC*f_r - self.G*c_r) * v_top / (1000*eta))*t1/3600
        W_VC = self.G*c_r*v_top/(1000*eta)*t2/3600
        return W_VA + W_VD + W_VC

    def regenerate_energy(self, Dis):
        t1, t2, v_top = self.get_transport_time_vtop(Dis)
        RW_v = (self.G/g*self.DEC*f_r - self.G*c_r) * v_top**2/(2*self.DEC) * 2.78*1e-7
        return RW_v
    
    def record_consumption(self):
        self.consumption.append(self.this_consumption)


class Fleet:
    """
    Define a Fleet class to get state of fleet and get a available vehicle.
    """

    def __init__(self, num, vmax, acc):
        self.num = num
        self.vehicles = [Vehicle(vmax, acc) for i in range(self.num)]

    def num_idle(self):
        state = [i.state for i in self.vehicles]
        return state.count(1)

    @property
    def coord(self):
        return [self.vehicles[i].place for i in range(self.num)]


class Lift:
    """
    Define a lift class to get available lift and save a queue of lift.
    """

    def __init__(self, vmax, acc):
        # busy:0 idle:1
        self.state = 1
        self.tier = IO[1]
        self.ACC = self.DEC = acc
        self.V_MAX = vmax
        self.weight = 200
        self.G = (weight+self.weight) * g
        self.this_consumption = 0
        self.consumption = []
        self.busytime = []

    def busy(self):
        self.state = 0
        self.this_consumption = 0

    def release(self, dest, work_time):
        self.tier = dest[1]
        self.state = 1
        self.busytime.append(work_time)

    @property
    def D_sign(self):
        return self.V_MAX**2/self.ACC

    def get_transport_time(self, Dis):
        t1, t2, vtop = self.get_transport_time_vtop(Dis)
        self.this_consumption += self.get_energy(Dis) - self.regenerate_energy(Dis)
        return 2*t1+t2

    def get_transport_time_vtop(self, Dis):
        # two scenario: place to lift; lift to place.
        # return t1 & t_2
        if Dis < self.D_sign:
            return (Dis/self.ACC)**.5, 0, (self.ACC*Dis)**.5
        else:
            return self.V_MAX/self.ACC, (Dis - self.V_MAX**2/self.ACC)/self.V_MAX, self.V_MAX

    def get_energy(self, Dis):
        """
        Compute work of a single journey 
        """
        t1, t2, v_top = self.get_transport_time_vtop(Dis)
        W_VA = ((self.G + self.G/g*self.ACC*f_r) * v_top / (1000*eta))*t1/3600
        W_VD = ((self.G/g*self.DEC*f_r + self.G) * v_top / (1000*eta))*t1/3600
        W_VC = self.G*v_top/(1000*eta)*t2/3600
        return W_VA + W_VD + W_VC

    def regenerate_energy(self, Dis):
        t1, t2, v_top = self.get_transport_time_vtop(Dis)
        RW_l = (self.G/g*self.DEC*f_r + self.G) * v_top**2/(2*self.DEC) * 2.78*1e-7
        return RW_l
    
    def record_consumption(self):
        self.consumption.append(self.this_consumption)

class Simulation:
    def __init__(self, env, lift, fleet, lift_re, veh_re, warehouse):
        self.env = env
        self.S = env.process(self.source_storage(env, lift, fleet, lift_re, veh_re))
        self.R = env.process(self.source_retrieval(env, lift, fleet, lift_re, veh_re))

    
    @property
    def E_C(self):
        return (sum([sum(v.consumption) for v in fleet.vehicles])+sum(lift.consumption))/warehouse.num_of_transactions

    @property
    def U_V(self):
        return sum([sum(i.busytime) for i in fleet.vehicles])/(Simlation_time*fleet.num)
    @property
    def U_L(self):
        return sum(lift.busytime)/Simlation_time


    def source_storage(self, env, lift, fleet, lift_re, veh_re):
        """
        In simulation time, keeping register [Storage] process into the simulation environment.
        """
        ind_s = 0
        while True:
            ind_s += 1
            gs = self.good_store(
                env, f'STORAGE {ind_s}', lift, fleet, lift_re, veh_re, warehouse)
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
        print("{:10.2f}, \033[1;31m{}\33[0m  arrives.".format(
            timepoint_arrive, name))
        yield env.timeout(0)

        dest = rand_place_available(warehouse)
        print(
            f'            place of  \033[1;31m{name}\33[0m is at{dest}, state of chosen place: {int(warehouse.record[tuple([i-1 for i in dest])])} .')
        warehouse.store(tuple([i-1 for i in dest]))

        # [len(i.users) for i in veh_re]
        len_of_queue = [len(i.users) for i in veh_re]
        # num_of_idle = [i.state for i in fleet.vehicles]
        num_of_idle = [i==0 for i in len_of_queue]

        if sum(num_of_idle) > 1:
            # find the closest available vehicle of all idle vehicles.
            v = get_available_closest(warehouse, lift, fleet)

        elif sum(num_of_idle) == 1:
            v = num_of_idle.index(True)

        else:
            # for condition that each vehicle is in duty, we choose a vehicle which has a smaller queue length.
            v = len_of_queue.index(min(len_of_queue))

        with veh_re[v].request() as req_veh:
            yield req_veh

            label_v_start = env.now
            print("{:10.2f}, \033[1;31m{}\33[0m seized vehicle\033[1;36m {} \33[0m, and place of the vehicle is at {}.".format(env.now, name, v+1, fleet.vehicles[v].place))
            fleet.vehicles[v].busy(dest)

            if fleet.vehicles[v].place[1] > 1:
                # seized vehicle is on gt 1 tier.
                with lift_re.request() as req_lift:
                    yield req_lift
                    lift.busy()
                    label_l_start = env.now

                    # veh -> lift :{1.to [0]bay,2.->IO[Aisle]}
                    trans_length = fleet.vehicles[v].place[2] * warehouse.coe_length['bay'] + abs(fleet.vehicles[v].place[0]-IO[0]) * warehouse.coe_length['width_of_aisle']
                    travel_to_lift = fleet.vehicles[v].get_transport_time(
                        trans_length)

                    lift_height = abs(
                        lift.tier - fleet.vehicles[v].place[1]) * warehouse.coe_length['height_tier']
                    lift_to_vehicle_tier = lift.get_transport_time(lift_height)
                    meet_time = max(travel_to_lift, lift_to_vehicle_tier)
                    yield env.timeout(meet_time)
                    print(
                        "{:10.2f}, \033[1;31m lift \33[0m meets the vehicle.".format(env.now))

                    lift_height = (fleet.vehicles[v].place[0]-1) * warehouse.coe_length['height_tier']
                    travel_to_IO = lift.get_transport_time(lift_height)

                    yield env.timeout(travel_to_IO)
                    print(
                        "{:10.2f}, \033[1;33m lift\33[0m travels to I/O. ".format(env.now))

                    yield env.timeout(0)
                    print("{:10.2f}, vehicle\033[1;36m {} \33[0m charges the load.".format(env.now, v+1))

                    if dest[1] == 1:
                        pass
                    else:
                        lift_height = (dest[1]-IO[1]) * warehouse.coe_length['height_tier']
                        travel_to_storage_tier = lift.get_transport_time(lift_height)
                        yield env.timeout(travel_to_storage_tier)
                        print("{:10.2f}, \033[1;33m lift \33[0m travels to storage's tier {}. ".format(env.now, dest[1]))
                lift.record_consumption()
                lift.release(dest, env.now-label_l_start)
                # get out the 'with', release the RESOURCE lift.
                trans_length = dest[2] * warehouse.coe_length['bay']
                travel_to_storage = fleet.vehicles[v].get_transport_time(trans_length)
                yield env.timeout(travel_to_storage)
                print("{:10.2f}, \033[1;33m vehicle {} \33[0m travels to storage. ".format(env.now, v+1))

            else:
                # the seized vehicle is on the first floor.
                if fleet.vehicles[v].place[:2] == IO[:2]:
                    # vehicle is at IO place
                    if dest[1] == 1:
                        # destination tier is tier 1.
                        pass
                    else:
                        # destination tier is tier gt 1.
                        with lift_re.request() as lift_req:
                            yield lift_req
                            lift.busy()
                            label_l_start = env.now
                            
                            lift_height = (dest[1]-IO[1])* warehouse.coe_length['height_tier']
                            travel_to_storage_tier = lift.get_transport_time(lift_height)
                            yield env.timeout(travel_to_storage_tier)
                            print(
                                "{:10.2f}, \033[1;33m lift \33[0m travels to storage's tier. ".format(env.now))
                        lift.record_consumption()
                        lift.release(dest, env.now - label_l_start)

                    trans_length = dest[2] * warehouse.coe_length['bay'] + abs(dest[0]-IO[0])*warehouse.coe_length['width_of_aisle']
                    travel_to_storage = fleet.vehicles[v].get_transport_time(trans_length)
                    yield env.timeout(travel_to_storage)
                    print("{:10.2f}, \033[1;33m vehicle {} \33[0m travels to storage. ".format(
                        env.now, v+1))

                else:
                    # vehicle is in tier 1 other place.
                    travel_length = fleet.vehicles[v].place[2] * warehouse.coe_length['bay'] + abs(
                       fleet.vehicles[v].place[0] -IO[0])*warehouse.coe_length['width_of_aisle']
                    travel_to_IO = fleet.vehicles[v].get_transport_time(
                        travel_length)
                    yield env.timeout(travel_to_IO)
                    print(
                        "{:10.2f}, \033[1;35m vehicle {} \33[0m travels to I/O. ".format(env.now, v+1))

                    if dest[1] == 1:
                        pass

                    else:
                        with lift_re.request() as lift_req:
                            yield lift_req
                            lift.busy()
                            label_l_start = env.now
                            
                            lift_height = (dest[1]-IO[1]) * warehouse.coe_length['height_tier']
                            travel_to_storage_tier = lift.get_transport_time(lift_height)
                            yield env.timeout(travel_to_storage_tier)
                            print(
                                "{:10.2f}, \033[1;33m lift \33[0m travels to storage's tier. ".format(env.now))
                        lift.record_consumption()
                        lift.release(dest, env.now-label_l_start)
                        

                    trans_length = dest[2] * warehouse.coe_length['bay'] + abs(dest[0]-IO[0])*warehouse.coe_length['width_of_aisle']
                    travel_to_storage = fleet.vehicles[v].get_transport_time(
                        trans_length)
                    yield env.timeout(travel_to_storage)
                    print("{:10.2f}, \033[1;33m vehicle {} \33[0m travels to storage. ".format(
                        env.now, v+1))
        
        fleet.vehicles[v].record_consumption()
        fleet.vehicles[v].release(dest, env.now-label_v_start)

        print("{:10.2f}, \033[1;44m  {}  FINISHED, VEHICLE {} RELEASED \33[0m".format(
            env.now, name, v+1))

    def source_retrieval(self, env, lift, fleet, lift_re, veh_re):
        """
        In simulation time, keeping register [Retrieval] process into the sim env.
        """
        ind_s = 0
        while True:
            ind_s += 1
            gr = self.good_retrieve(
                env, f'RETRIEVAL {ind_s}', lift, fleet, lift_re, veh_re, warehouse)
            env.process(gr)
            t_arrive_retrieval = random.expovariate(lambda_ZR)
            yield env.timeout(t_arrive_retrieval)

    def good_retrieve(self, env, name, lift, fleet, lift_re, veh_re, warehouse):
        """
        demand arrives, is lifted and transported to I/O.
        Procedure:
        *****--------REQUEST: Vehicle --------********
        1.Arrived retrieval seizes an available vehicle.
        2.Vehicle travels to lift.[can be omitted]
        *****--------REQUEST: Lift------------********
        3.Lift travels to vehicle's tier. [can be omitted]
        4.Lift travels to load's tier with vehicle. [can be omitted]
        5.vehicle travels to retrieval and back to lift/(I/O). 
        6.Lift travels to IO.[can be omitted]
        *****--------RLEASE: Lift-------------********
        *****--------RELease: Vehicle -------*********
        """
        timepoint_arrive = env.now
        print("{:10.2f}, \033[1;32m{}\33[0m arrives".format(
            timepoint_arrive, name))
        yield env.timeout(0)

        load = rand_place_loaded(warehouse)
        print(
            f'            place of  \033[1;32m{name}\33[0m is at{load}, place chosen state: {int(warehouse.record[tuple([i-1 for i in load])])} .')

        len_of_queue = [len(i.users) for i in veh_re]
        num_of_busy = [i > 0 for i in len_of_queue]
        num_of_idle = [i==0 for i in len_of_queue]
        # num_of_idle = [i.state for i in fleet.vehicles]

        if sum(num_of_idle) > 1:
            # find the closest available vehicle
            v = get_available_closest(warehouse, lift, fleet)

        elif sum(num_of_idle) == 1:
            v = num_of_idle.index(True)

        else:
            v = len_of_queue.index(min(len_of_queue))

        with veh_re[v].request() as req_veh:
            yield req_veh

            label_v_start = env.now
            print("{:10.2f}, \033[1;31m{}\33[0m seized vehicle\033[1;36m {} \33[0m, vehicle place is at {}".format(
                env.now, name, v+1, fleet.vehicles[v].place))
            fleet.vehicles[v].busy(IO)

            if fleet.vehicles[v].place[1] == load[1]:
                # load is at the same tier of the chosen vehicle.
                """
                Vehcile and Lift how to realize SYNC?
                min(t_1, t_2)
                """
                trans_length1 = abs(fleet.vehicles[v].place[2]-load[2]) * warehouse.coe_length['bay'] + abs(
                    fleet.vehicles[v].place[0]-load[0]) * warehouse.coe_length['width_of_aisle']
                travel_to_retrieval = fleet.vehicles[v].get_transport_time(
                    trans_length1)

                travel_length2 = load[2] * warehouse. coe_length['bay'] + abs(load[0]-IO[0]) * warehouse.coe_length['width_of_aisle']
                travel_to_lift = fleet.vehicles[v].get_transport_time(
                    travel_length2)
                travel_horizon = travel_to_retrieval + travel_to_lift

                if load[1] == IO[1]:
                    yield env.timeout(travel_to_lift)

                else:
                    with lift_re.request() as lift_req:
                        yield lift_req
                        lift.busy()
                        label_l_start = env.now
                        lift_height = abs(lift.tier - load[1]) * warehouse.coe_length['height_tier']
                        travel_to_retrieval_tier = lift.get_transport_time(lift_height)
                        meet_time = max(travel_horizon, travel_to_retrieval_tier)
                        yield env.timeout(meet_time)

                        lift_height = (load[1]-IO[1]) * warehouse.coe_length['height_tier']
                        lift_to_IO = lift.get_transport_time(lift_height)
                        yield env.timeout(lift_to_IO)
                        lift.record_consumption()
                    lift.release(IO, env.now-label_l_start)
            else:
                # tier of seized vehicle is different from that of retrieval.
                # seized vehicle travels to lift.
                travel_length = fleet.vehicles[v].place[2] * warehouse. coe_length['bay'] + abs(fleet.vehicles[v].place[0]-IO[0]) * warehouse.coe_length['width_of_aisle']
                travel_to_lift = fleet.vehicles[v].get_transport_time(travel_length)
                with lift_re.request() as lift_req:
                    yield lift_req
                    lift.busy()
                    label_l_start = env.now


                    lift_height = abs(lift.tier - fleet.vehicles[v].place[1]) * warehouse.coe_length['height_tier']
                    travel_veh_tier = lift.get_transport_time(lift_height)

                    meet_time = max(travel_to_lift, travel_veh_tier)
                    yield env.timeout(meet_time)

                    travel_length = load[2] * warehouse.coe_length['bay'] + abs(load[0]-IO[0]) * warehouse.coe_length['width_of_aisle']
                    travel_to_retrieval = fleet.vehicles[v].get_transport_time(travel_length)
                    yield env.timeout(travel_to_retrieval)
                    print("{:10.2f},vehicle \033[1;34m {} \33[0m travels to retrieval.".format(env.now, v+1))
                    yield env.timeout(travel_to_retrieval)
                    print("{:10.2f},vehicle \033[1;34m {} \33[0m gets to lift with good.".format(env.now, v+1))

                    lift_height = (load[1]-IO[1]) * warehouse.coe_length['height_tier']
                    lift_to_IO = lift.get_transport_time(lift_height)
                    yield env.timeout(lift_to_IO)
                    lift.record_consumption()
                lift.release(IO, env.now-label_l_start)
        fleet.vehicles[v].record_consumption()
        fleet.vehicles[v].release(IO, env.now - label_v_start)

        print("{:10.2f}, \033[1;46m  {}  FINISHED, VEHICLE {} RELEASED \33[0m".format(env.now, name, v+1))
        warehouse.retrieve(tuple([i-1 for i in load]))


if __name__ == "__main__":
    # A = 4
    # A_Z = 3
    # T = 4
    # B = 6
    
    # lambda_all = 100/3600
    # lambda_Z = lambda_all / A   
    warehouse_file = 'Configuration.txt'
    va_file = 'Velocity_profile.txt'
    wareh = get_config('Configuration.txt')
    v_a = get_velcity_profile('Velocity_profile.txt')
    sim_config = get_simulation(wareh, v_a)
    Simlation_time = 3600*8*5
    for k_th, config in enumerate([sim_config[32]]):
        A, T, B, containers, A_Z, lambda_Z, v_v, v_a, l_v, l_a= config
        lambda_Z /= 3600
        sides = 2
        lambda_ZS = lambda_Z/2
        lambda_ZR = lambda_Z/2
        # IO = [int((A_Z-1)/2+1),1,1,1]
        IO = [(A_Z-1)/2+1, 1, 0, 1]

        num_of_vehicles_Z = 2
        bay, width_of_aisle, height_tier = 1, 3, 1.5
        weight = 250

        f_r = 1.15
        c_r = 0.01
        g = 10
        eta = .9

        env = simpy.Environment()
        warehouse = Warehouse(A_Z, T, B, sides)
        warehouse.init_warehouse()
        lift = Lift(l_v, l_a)
        fleet = Fleet(num_of_vehicles_Z, v_v, v_a)
        lift_re = simpy.Resource(env, 1)
        veh_re = [simpy.Resource(env, 1) for i in range(num_of_vehicles_Z)]
        sim = Simulation(env, lift, fleet, lift_re, veh_re, warehouse)
        env.run(until=Simlation_time)

        print(f'\n A={A}, B={B}, T={T}, V_v={v_v}, V_a={v_a}, L_v={l_v}, L_a={l_a}')
        print('\n\n\nUL:{:.3f}, UV:{:.3f}, EC:{:.3f}\n\n'.format(sim.U_L, sim.U_V, sim.E_C))
