def get_config(file_name):
    """
    From txt.file, read the configuration of warehouses into the environment.
    """
    input_data = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            input_data.append(line.strip('\n'))
    configuration = [[] for i in range(len(input_data)-1)]

    for i in range(len(input_data)-1):
        configuration[i] = [int(j)for j in input_data[i+1].split(' ')]
    return configuration


def get_velcity_profile(file_name):
    """
    From txt.file, read the velocity profile of vehicle and lift into the environment.
    """
    input_data = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            input_data.append(line.strip('\n'))
    v_a_profile = [[] for i in range(len(input_data)-1)]

    for i in range(len(input_data)-1):
        v_a_profile[i] = [int(j)for j in input_data[i+1].split(' ')]
    return v_a_profile*2


def get_simulation(warehouse, va):
    """
    From two input, generate 2*2*3*3 different simulation environment.
    """
    sim = []
    for i in warehouse:
        for vv in va[:2]:
            for vl in va[2:4]:
                sim.append(i+vv+vl)
    return sim


if __name__ == "__main__":
    wareh = get_config('Configuration.txt')
    v_a = get_velcity_profile('Velocity_profile.txt')
    print(get_simulation(wareh, v_a)[0])    
