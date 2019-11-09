import re
input_prob = []
input_problem = dict()
file_name = "A-n6-k2.vrp"
with open(file_name) as f:
    for line in f.readlines():
        input_prob.append(line.strip('\n'))
for i in range(6):
    cur_str_list = input_prob[i].split()
    input_problem[cur_str_list[0]] = " ".join(cur_str_list[2:])
dim = int(input_problem['DIMENSION'])

type_of_vrp = input_prob[0].split()
type_of_vrp = type_of_vrp[2]
k_order_1 = re.search('-k',type_of_vrp).span()
K =int(list(type_of_vrp)[k_order_1[1]])

location = []
demand = []
for i in range(7, 7+dim):
    cur = input_prob[i].split()
    del cur[0]
    cur_location = (int(cur[0]),int(cur[1]))
    location.append(cur_location)

for i in range(14, 14+dim):
    cur_demand = input_prob[i].split()
    del cur_demand[0]
    cur_demand = int(cur_demand[0])
    demand.append(cur_demand)

