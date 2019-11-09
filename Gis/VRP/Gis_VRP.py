"""
model the SCVRP & solve the problem
problem:
K = 2
Capacity 100
N = 5
demand 0 20 30 40 50 50

"""
import numpy as np
import cplex
from cplex.exceptions import CplexError
from Variable import Variable
from Constraint import Constraint
from Objective import Objective
from Result import Result
import copy

def get_data(file_path):
    return 

def get_problem(location, cus_depot):

    return dist_1dim,cus_depot,K,num_of_customers
location = [(50, 50),(0, 50),(0, 0),(50, 0),(50, 100),(100,100)]
num_of_customers=5
cus_depot = 6
K = 2 
distance = np.zeros((6,6),dtype=np.int16)
# # manhatten distance 
# for i in range(len(location)):
#     for j in range(len(location)):
#         distance[i,j] = abs(location[i][0]-location[j][0])+abs(location[i][1]-location[j][1])

# euclidean distance
for i in range(len(location)):
    for j in range(len(location)):
        distance[i,j] = ((location[i][0]-location[j][0])**2+(location[i][1]-location[j][1])**2)**0.5

# init the decision variables 
decision_variables = []
for i in range(num_of_customers+1):
    decision_variables.append([])
    for j in range(num_of_customers+1):
        decision_variables[i].append(Variable('I',[0,1],'x%d%d'%(i,j)))
for i in range(num_of_customers+1):
    decision_variables[0][i]['upper_bound']=2.0

variables_1dim = []
rel = np.zeros((cus_depot,cus_depot),dtype=np.int16)
x = 0
dist_1dim = []
mapping = dict() # get a dict like : mapping = {'01':0,'02':1,'03':2 ...} 
ind1=[] # ind1 each customer has remain decision_variables
list_customer = list(range(cus_depot))
for i in range(cus_depot):
    ind1.append(num_of_customers-i)

for i in range(cus_depot):
    for j in range(ind1[i]):
        variables_1dim.append(decision_variables[i][i+j+1])
        dist_1dim.append(float(distance[i][i+j+1]))
        rel[i][i+j+1] = x
        mapping['%d%d'%(i,i+j+1)] = x
        x+=1

# for customer i
# m<i,give x_mi
# m>i give x_im m\in {0,1,...,5}
rows1 = []
for i in range(num_of_customers):
    rows1.append([])
    for j in range(2):
        rows1[i].append([])
for i in range(1,cus_depot):
    list_cur = copy.deepcopy(list_customer)
    list_cur.remove(i)
    for j in list_cur:
        if j < i:
            rows1[i-1][0].append(mapping['%d%d'%(j,i)])
            rows1[i-1][1].append(1)
        else:
            rows1[i-1][0].append(mapping['%d%d'%(i,j)])
            rows1[i-1][1].append(1)
'''
[[['x01', 'x12', 'x13', 'x14', 'x15'], [1, 1, 1, 1, 1]],
 [['x02', 'x12', 'x23', 'x24', 'x25'], [1, 1, 1, 1, 1]],
 [['x03', 'x13', 'x23', 'x34', 'x35'], [1, 1, 1, 1, 1]],
 [['x04', 'x14', 'x24', 'x34', 'x45'], [1, 1, 1, 1, 1]],
 [['x05', 'x15', 'x25', 'x35', 'x45'], [1, 1, 1, 1, 1]]]
 transfer to variables_1dim and get:
[['x0', 'x5', 'x6', 'x7', 'x8'], [1, 1, 1, 1, 1]]
[['x1', 'x5', 'x9', 'x10', 'x11'], [1, 1, 1, 1, 1]]
[['x2', 'x6', 'x9', 'x12', 'x13'], [1, 1, 1, 1, 1]]
[['x3', 'x7', 'x10', 'x12', 'x14'], [1, 1, 1, 1, 1]]
[['x4', 'x8', 'x11', 'x13', 'x14'], [1, 1, 1, 1, 1]]
[['x0', 'x1', 'x2', 'x3', 'x4'], [1, 1, 1, 1, 1]]

'''
# for depot0 : 
row2 = [[]]
for i in range(2):
    row2[0].append([])
for i in range(num_of_customers):
    row2[0][0].append(i)
    row2[0][1].append(1)
'''
[['x01', 'x02', 'x03', 'x04', 'x05'], [1, 1, 1, 1, 1]]
'''
rows = rows1+row2

my_obj = Objective('min',dist_1dim)

right_side = [2.0]*num_of_customers
right_side.append(2.0*K)
constraints = [Constraint('c%d'%(i+1), rows[i], 'E', right_side[i]) for i in range(len(rows))]
relation = ['E']*len(constraints)
var_names = ['x%d'%(i+1) for i in range(int(cus_depot*(cus_depot-1)/2))]
row_names = ['c%d'%(i+1) for i in range(cus_depot)]
lowerbounds = []
upperbounds = []
var_types = []
for i in range(len(variables_1dim)):
    # lowerbounds.append(float(variables_1dim[i].lower_bound))
    # upperbounds.append(float(variables_1dim[i].upper_bound))
    lowerbounds.append(variables_1dim[i].lower_bound)
    upperbounds.append(variables_1dim[i].upper_bound)
    var_types.append(variables_1dim[i].type)
lin_expression = [cplex.SparsePair(ind = rows[i][0], val = rows[i][1]) for i in range(len(rows))]

def generate_problem(prob):
    if my_obj.preference == 'min':
        prob.objective.set_sense(prob.objective.sense.minimize)
    elif my_obj.preference == 'max':
        prob.objective.set_sense(prob.objective.sense.maximize)
    else:
        print('You had input the wrong objective preference!')
    # !!! all obj&ub&lb need be float.
    prob.variables.add(obj=my_obj.coefficient,lb=lowerbounds,ub=upperbounds,names=var_names,types=var_types)
    prob.linear_constraints.add(lin_expr=lin_expression,senses=relation,rhs=right_side,names=row_names)
    pass

def calculate():
    try:
        my_prob = cplex.Cplex()
        generate_problem(my_prob)
        my_prob.solve()
    except CplexError as exc:
        print(exc)
    num_rows = my_prob.linear_constraints.get_num()
    num_cols = my_prob.variables.get_num()
    print("Solution status = ", my_prob.solution.get_status(), ":", end=' ')
    print(my_prob.solution.status[my_prob.solution.get_status()])
    print("Solution value  = ", my_prob.solution.get_objective_value())
    x = my_prob.solution.get_values()
    for j in range(num_cols):
        print("Column %d:  Value = %10f " % (j, x[j]))
    res = Result(is_solved=my_prob.solution.get_status(),
                 objective_value=my_prob.solution.get_objective_value(),
                 x_value=x, status=my_prob.solution.status[my_prob.solution.get_status()])
    print("Problem:{0}\nOptimal Value:{1}\nSolution:{2}".format(my_prob.solution.status[res.is_solved], res.obj_value, res.x_value))
    my_prob.write("vrp.lp")

if __name__ == '__main__':

    calculate()

