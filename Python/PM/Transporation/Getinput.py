def get_parameters(file):
    """
    From text file, read the parameters into the integer programming model.
    """
    input_data = []
    with open(file, 'r') as f:
        for line in f.readlines():
            input_data.append(line.strip('\n'))
    supply_ind = input_data.index('SUPPLY')
    demand_ind = input_data.index('DEMAND')
    tech_ind = input_data.index('tech_coe')
    length = len(input_data)
    supply = []
    supply_name = []
    demand = []
    demand_name = []
    for i in range(supply_ind+1, demand_ind):
        tmp = [j for j in input_data[i].split(' ')]
        supply.append(float(tmp[1]))
        supply_name.append(tmp[0])
    for i in range(demand_ind+1, tech_ind):
        tmp = [j for j in input_data[i].split(' ')]
        demand.append(float(tmp[1]))
        demand_name.append(tmp[0])
    tech_coe = []
    for i in range(tech_ind+1, length):
        for j in input_data[i].split(' '):
            tech_coe.append(float(j))
    return supply, demand, tech_coe


if __name__ == "__main__":
    supply, demand, tech_coe = get_parameters('data.txt')
    print(supply, demand, tech_coe)
