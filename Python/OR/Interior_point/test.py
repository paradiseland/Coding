file_path = 'prob.txt'
input_problem = []
with open(file_path,'r') as f:
        for line in f.readlines():
            input_problem.append(line.strip('\n'))
my_obj_type = input_problem[0]
my_obj_expr = input_problem[1]
my_obj_split = [i for i in input_problem[1].split(' ')]

while True:
    num_of_var = 0
    for i in range(1,20):
        if 'x%d'%i in my_obj_expr:
            num_of_var += 1
    break

print(my_obj_expr)
print(num_of_var)
