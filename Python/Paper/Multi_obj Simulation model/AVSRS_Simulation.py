import simpy


class Warehouse():
    """
    Give some configuration of the warehouse, vehicles and lifts.
    """

    def __init__(self, aisle, bay, tier, acc_veh, acc_lift):
        self.aisle = aisle
        self.bay = bay
        self.tier = tier
        self.acc_vehicle = acc_veh
        self.dec_vehicle = acc_veh
        self.acc_lift = acc_lift
        self.dec_lift = acc_lift


class Fleet():
    """
    define a Fleet class to get state of fleet and get a available vehicle
    """

    def __init__(self, num):
        self.num = num
        self.coord = [[0, 0, 0, 0] for i in range(self.num)]
        self.vehicle = [Vehicle() for i in range(self.num)]

    def num_idle(self):
        state = [i.state for i in self.vehicle]
        return state.count(0)

    def get_closest(self):
        state = [i.state for i in self.vehicle]
        closest = 0
        tmp = [10000]*4
        for ind, st in enumerate(state):
            if st == 0:
                if sum(self.vehicle[ind].place) < sum(tmp):
                    tmp = self.vehicle[ind].place
                    closest = ind
        return closest

class Lifts():
    """
    record each lift state
    """
    def __init__(self, num):
        self.num = num
        self.tier = [0]*self.num
        self.lift = [Lift() for i in range(self.num)]
    




class Lift():
    """
    define a lift class to get available lift and save a queue of lift.
    """

    def __init__(self):
        self.state = 0
        self.tier = 0
        self.queue_length = 0
    
    def busy(self, destination):
        self.tier = destination[2]
        self.state = 0

    def release(self):
        self.state = 1

    def queue(self, veh):
        self.queue_length += 1


class Vehicle():
    """
    define a Vehicle class to get palce, availability and operation of each vehicle.
    """

    def __init__(self, env):

        self.place = []
        self.destination = [0, 0, 0, 0]
        self.state = 0
        self.drive_proc = env.process()

    def busy(self, chosen, dest, type_transaction):
        if type_transaction == 0:
            index_vehicle = chosen
            self.destination = dest
        else:
            self.destination = [0, 0, 0, 0]
        self.state = 0

    def release(self, index, place_coord):
        self.palce[index] = place_coord
        self.state = 1

    def drive(self, env):
        pass

    
class Storage():
    def __init__(self):
        self.time = 0

    def transaction_arrive(self):
        pass

    def get_available_place(self):
        # randomly storage
        # Zone, Aisle, Tier
        place = []
        self.place = place

    def update_storage(self):
        self.place = [0]*4


class Retrieval():
    def __init__(self):
        self.time = 0


def Store(place_store, place_vehicle):

    # transaction arrives

    # determine the place to store

    # get a avilable & closest vehicle
    # place[A_Z, T, B, oneside]

    # type of storage place & vehicle initial place :[0, 0]. [0, N], [N, N]
    journey_vehicle = 0
    journey_vehicle += place_vehicle[3]

    if place_vehicle[2] > 1:
        store1(place_vehicle)
    else:
        store2(place_vehicle)


def store1(place_vehicle):
    """
    seized vehicle_T > 1:
    """

    # queue in the lift queue

    # get downstairs


def store2():
    """
    storage in tier which gt 1
    """
    pass


def simulation():
    env = simpy.Environment()
    proc_arrive = simpy.Process(env, )
    proc_request_v = simpy.Process(env, )


if __name__ == "__main__":

    v = Vehicle()
    st = Storage()
    # main process:
    st.transaction_arrive()
    place = st.get_available_place()
    v_current = v.get_aviable()

    env = simpy.Environment()


