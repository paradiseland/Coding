"""
open the file get the problem.
"""
input_problem = []

with open('input.txt', 'r') as f:
    for line in f.readlines():
        input_problem.append(line.strip('\n'))

my_obj_type = input_problem[0]
my_obj_coe = [int(i) for i in input_problem[1].split(' ')]
my_lower_bounds = [float(i) for i in input_problem[2].split(' ')]
my_upper_bounds = [float(i) for i in input_problem[3].split(' ')]
type_of_variable = [i for i in input_problem[4].split(' ')]
name_of_variable = [i for i in input_problem[5].split(' ')]
tech_coe = [j.split(' ')
            for j in [coes for coes in input_problem[6].split(',')]]
for i in range(len(tech_coe)):
    for j in range(len(tech_coe[i])):
        tech_coe[i][j] = int(tech_coe[i][j])
sign_of_cons = [i for i in input_problem[7].split(' ')]
right_of_cons = [float(i) for i in input_problem[8].split(' ')]
print(my_obj_type)
print(my_obj_coe)
print(my_lower_bounds)
print(my_upper_bounds)
print(type_of_variable)
print(name_of_variable)
print(tech_coe)
print(sign_of_cons)
print(right_of_cons)
rows = [[name_of_variable, tech_coe[i]]for i in range(len(tech_coe))]
print(rows)
pass
