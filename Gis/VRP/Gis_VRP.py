"""
using Cplex-Python API to call Cplex to solve VRP problem.
"""
import re
import copy
import math
import numpy as np
import cplex
from cplex.exceptions import CplexError
from cplex.callbacks import UserCutCallback, LazyConstraintCallback


import matplotlib.pyplot as plt
from Variable import Variable
from Constraint import Constraint
from Objective import Objective
from Result import Result

eps = 1e-6

def get_S(mapping,cur_solution):
    """
    from current solution get the S which may be a subtour.
    """
    # need to def num_of_customers & eps in advance.
    # demovalues:
    # [0.2, 0.2, 0, 0, 0, 0.8, 0, 0, 0, 0, 0, 0, 0.7, 0.8, 0.9]
    # mapping = {(0, 1):0, (0, 2):1, (0, 3):2, (0, 4):3, (0, 5):4, (1, 2):5, (1, 3):6, (1, 4):7, (1, 5):8, (2, 3):9, (2, 4):10, (2, 5):11, (3, 4):12, (3, 5):13, (4, 5):14}
    supernode = []
    dict_of_conn = dict(zip(mapping, cur_solution))
    # generate the list of supernodes.
    no_conn_depot = [] # def a list of some customers who are not diirectly connected to depot.

    for k, v in mapping.items():
        if v <= num_of_customers - 1:
            if dict_of_conn[k] < eps:
                no_conn_depot.append(k)

    no_conn_depot_conn = [] 
    # get a list of dict like:
    # [{(1, 3): 0, (2, 3): 0, (3, 4): 0.7, (3, 5): 0.8},
    #  {(1, 4): 0, (2, 4): 0, (3, 4): 0.7, (4, 5): 0.9},
    #  {(1, 5): 0, (2, 5): 0, (3, 5): 0.8, (4, 5): 0.9}]
    for i in range(len(no_conn_depot)):
        if no_conn_depot[i][0] == 0:
            cur_j_conn = dict()
            for q in range(1,num_of_customers+1):
                if no_conn_depot[i][1] == q:
                    pass
                elif no_conn_depot[i][1] < q:
                    cur_j_conn[(no_conn_depot[i][1], q)] = dict_of_conn[(no_conn_depot[i][1],q)]
                else:
                    cur_j_conn[(q, no_conn_depot[i][1])] = dict_of_conn[(q,no_conn_depot[i][1])]
            no_conn_depot_conn.append(cur_j_conn)
    cur_supernode = [[no_conn_depot[x][1]] for x in range(len(no_conn_depot))]
    for i in range(len(no_conn_depot)):
        cur_node = no_conn_depot[i][1]
        for k,v in no_conn_depot_conn[i].items():
            if v > eps:
                if k[0] == cur_node:
                    cur_supernode[i].append(k[1])
                else:
                    cur_supernode[i].append(k[0])
    list_of_set = []
    for i in range(len(no_conn_depot)):
        list_of_set.append(set(cur_supernode[i]))
    unique_set_supernode = []
    for item in list_of_set:
        if not item in unique_set_supernode:
            unique_set_supernode.append(item)
    num_of_S = len(unique_set_supernode)
    S = []
    for i in range(num_of_S):
        S.append(list(unique_set_supernode[i]))
    return S


def make_cuts(S, Q):
    """
    from the S which may be a set of subtour, get a constraintor a cut.
    the cut: X(δ(S)) ≥ 2γ(S)  
    γ(S) is replaced by [q(s)/Q]
    """
    q_S = []
    for i in range(len(S)):
        temp = 0
        for j in S[i]:
            temp += demand[j]
        # generate a list of q(S)
        q_S.append(temp)
    gamma_S = [math.ceil(i/Q)  for i in q_S]
    # gamma_S = [i/Q  for i in q_S]


    var_deltaS = []
    cus_dep = set(range(cus_depot))
    # for a S, will get a (num_of_customers+depot - no_conn) * no_conn vars
    for i in range(len(S)):
        var_deltaS.append([])
        for j in cus_dep-set(S[i]):
            for k in set(S[i]):
                if j < k:
                    var_deltaS[i].append(mapping[(j,k)])
                else:
                    var_deltaS[i].append(mapping[(k,j)])
    return var_deltaS, gamma_S


class LazyCallback(LazyConstraintCallback):
    """
    This callback will be used within the cut loop that CPLEX calls 
    at each node of the branch and cut algorithm.
    It will be called once after CPLEX has ended its own cut generation loop 
    so that the user can specify additional cuts to be added to the cut pool.
    """

    def __init__(self, env):
        LazyConstraintCallback.__init__(self, env)
        self.mapping = mapping

    def __call__(self):
        for i in range(4):
            print('*'*30)
        print("我成功了吗>>>????")
        cur_solution = self.get_values()
        connect = get_connect(cur_solution)
        plot_result(connect)
        S = get_S(mapping=mapping, cur_solution=cur_solution)
        print(S)
        var_order, gamma_S = make_cuts(S, Q)
        vars = []
        for i in range(len(var_order)):
            vars.append([])
            for j in var_order[i]:
                vars[i].append('x%d'%(j+1))
        add_con_expression = [cplex.SparsePair(
        ind=vars[i], val=[1]*len(vars[i])) for i in range(len(vars))]
        sense = 'G'*len(vars)
        rh = [2*i for i in gamma_S]
        for i in range(len(vars)):
            self.add(constraint=add_con_expression[i], sense='G', rhs=rh[i])
            print("add a LazyConstraint:",add_con_expression[i])


class MyCutCallback(UserCutCallback):
    """
    This callback will be used when CPLEX finds a new integer feasible solution 
    and when CPLEX finds that the LP relaxation at the current node is unbounded.
    """

    def __init__(self, env):
        UserCutCallback.__init__(self, env)

    def __call__(self):
        cur_solution = self.get_values()
        S = get_S(mapping=mapping, cur_solution=cur_solution)
        print(S)
        var_order, gamma_S = make_cuts(S, Q)
        vars = []
        for i in range(len(var_order)):
            vars.append([])
            for j in var_order[i]:
                vars[i].append('x%d'%(j+1))
        add_con_expression = [cplex.SparsePair(
        ind=vars[i], val=[1]*len(vars[i])) for i in range(len(vars))]
        sense = 'G'*len(vars)
        rh = 2 * gamma_S
        for i in range(len(vars)):
            self.add(cut=add_con_expression[i], sense='G', rhs=rh[i])
            print("add a LazyConstraint:",add_con_expression[i])



def get_parameter(file_name):
    """
    get the parameters of VRP problem from the .txt file.
    """
    input_prob = []
    input_problem = dict()
    with open(file_name) as f:
        for line in f.readlines():
            input_prob.append(line.strip('\n'))
    for j in range(6):
        cur_str_list = input_prob[j].split()
        input_problem[cur_str_list[0]] = " ".join(cur_str_list[2:])
    dim = int(input_problem['DIMENSION'])

    type_of_vrp = input_prob[0].split()
    type_of_vrp = type_of_vrp[2]
    Q = int(input_prob[5].split()[2])
    k_order_1 = re.search('-k', type_of_vrp).span()
    K = int(list(type_of_vrp)[k_order_1[1]])
    location = []
    demand = []
    for j in range(7, 7+dim):
        cur = input_prob[j].split()
        del cur[0]
        cur_location = (int(cur[0]), int(cur[1]))
        location.append(cur_location)
    for j in range(8+dim, 8+2*dim):
        cur_demand = input_prob[j].split()
        del cur_demand[0]
        cur_demand = int(cur_demand[0])
        demand.append(cur_demand)
    return location, demand, K, Q


def get_problem(location):
    """
    use the parameters to generate the content such as distance matrix,decision variables,rows and etc.
    """
    num_of_customers = len(location)-1
    cus_depot = len(location)
    # # manhatten distance
    # for i in range(len(location)):
    #     for j in range(len(location)):
    #         distance[i,j] = abs(location[i][0]-location[j][0])+abs(location[i][1]-location[j][1])

    # euclidean distance
    distance = np.zeros((cus_depot,cus_depot), dtype=np.int32)
    for i in range(len(location)):
        for j in range(len(location)):
            distance[i, j] = ((location[i][0]-location[j][0])
                              ** 2+(location[i][1]-location[j][1])**2)**0.5
    decision_variables = []
    for i in range(num_of_customers+1):
        decision_variables.append([])
        for j in range(num_of_customers+1):
            decision_variables[i].append(
                Variable('I', [0, 1], 'x%d%d' % (i, j)))
    for i in range(num_of_customers+1):
        decision_variables[0][i]['upper_bound'] = 2.0

    variables_1dim = []
    rel = np.zeros((cus_depot, cus_depot), dtype=np.int16)
    x = 0
    dist_1dim = []
    mapping = dict()  # get a dict like : mapping = {(0,1):0,(0,2):1,(0,3):2 ...}
    ind1 = []  # ind1 each customer has remain decision_variables
    list_customer = list(range(cus_depot))
    for i in range(cus_depot):
        ind1.append(num_of_customers-i)

    for i in range(cus_depot):
        for j in range(ind1[i]):
            variables_1dim.append(decision_variables[i][i+j+1])
            dist_1dim.append(float(distance[i][i+j+1]))
            rel[i][i+j+1] = x
            mapping[(i, i+j+1)] = x
            x += 1

    # for customer i
    # m<i,give x_mi
    # m>i give x_im m\in {0,1,...,5}
    rows1 = []
    for i in range(num_of_customers):
        rows1.append([])
        for j in range(2):
            rows1[i].append([])
    for i in range(1, cus_depot):
        list_cur = copy.deepcopy(list_customer)
        list_cur.remove(i)
        for j in list_cur:
            if j < i:
                rows1[i-1][0].append(mapping[(j, i)])
                rows1[i-1][1].append(1)
            else:
                rows1[i-1][0].append(mapping[(i, j)])
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

    my_obj = Objective('min', dist_1dim)

    right_side = [2.0]*num_of_customers
    right_side.append(2.0*K)
    constraints = [Constraint('c%d' % (i+1), rows[i],
                              'E', right_side[i]) for i in range(len(rows))]
    relation = ['E']*len(constraints)
    var_names = ['x%d' % (i+1) for i in range(int(cus_depot*(cus_depot-1)/2))]
    row_names = ['c%d' % (i+1) for i in range(cus_depot)]
    lowerbounds = []
    upperbounds = []
    var_types = []
    for i in range(len(variables_1dim)):
        # lowerbounds.append(float(variables_1dim[i].lower_bound))
        # upperbounds.append(float(variables_1dim[i].upper_bound))
        lowerbounds.append(variables_1dim[i].lower_bound)
        upperbounds.append(variables_1dim[i].upper_bound)
        var_types.append(variables_1dim[i].type)
    lin_expression = [cplex.SparsePair(
        ind=rows[i][0], val=rows[i][1]) for i in range(len(rows))]
    return dist_1dim, cus_depot, num_of_customers, my_obj, lowerbounds, upperbounds, var_types, var_names, lin_expression, row_names, relation, right_side, mapping
# location = [(50, 50),(0, 50),(0, 0),(50, 0),(50, 100),(100,100)]
# init the decision variables


def generate_problem(my_obj, lowerbounds, upperbounds, var_types, var_names, lin_expression, row_names, relation, right_side, prob):
    """
    generate the problem using the problem concrete various data structure.
    """
    if my_obj.preference == 'min':
        prob.objective.set_sense(prob.objective.sense.minimize)
    elif my_obj.preference == 'max':
        prob.objective.set_sense(prob.objective.sense.maximize)
    else:
        print('You had input the wrong objective preference!')
    # !!! all obj&ub&lb need be float.
    prob.variables.add(obj=my_obj.coefficient, lb=lowerbounds,
                       ub=upperbounds, names=var_names, types=var_types)
    prob.linear_constraints.add(
        lin_expr=lin_expression, senses=relation, rhs=right_side, names=row_names)
    pass


def calculate():
    """
    calculate the problem and output the result.
    """
    try:
        my_prob = cplex.Cplex()
        alg = my_prob.parameters.lpmethod.values
        my_prob.parameters.lpmethod.set(alg.auto)
        generate_problem(my_obj, lowerbounds, upperbounds, var_types, var_names,
                         lin_expression, row_names, relation, right_side, my_prob)

        # add a UserCutCallback:
        usercb = my_prob.register_callback(MyCutCallback)
        # add a LazyConstraintCallback:
        userlz = my_prob.register_callback(LazyCallback)
        userlz.mapping = mapping
        my_prob.solve()
    except CplexError as exc:
        print(exc)
    num_rows = my_prob.linear_constraints.get_num()
    num_cols = my_prob.variables.get_num()
    print("Solution status = ", my_prob.solution.get_status(), ":", end=' ')
    print(my_prob.solution.status[my_prob.solution.get_status()])
    print("Solution value  = ", my_prob.solution.get_objective_value())
    x = my_prob.solution.get_values()
    # for j in range(num_cols):
    #     print("Column %d:  Value = %10f " % (j, x[j]))
    res = Result(is_solved=my_prob.solution.get_status(),
                 objective_value=my_prob.solution.get_objective_value(),
                 x_value=x, status=my_prob.solution.status[my_prob.solution.get_status()])
    print("Problem:{0}\nOptimal Value:{1}\nSolution:{2}".format(
        my_prob.solution.status[res.is_solved], res.obj_value, [int(res.x_value[i]) for i in range(len(res.x_value))]))
    # my_prob.write("vrp.lp")
    return x


def get_connect(x):
    """
    from the result, get the connection from each point(customers & depot).
    generate the list(tuple) like:[(0, 1), (0, 3), (0, 4), (0, 5), (1, 2), (2, 3), (4, 5)]
    """
    x = [int(x[i]) for i in range(len(x))]
    connection = []
    connection_2 = []
    for k, value in zip(mapping.keys(), x):
        if value == 1:
            connection.append(k)
        elif value == 2:
            connection.append(k)
        else:
            pass
    conn_lines = connection
    return conn_lines


def plot_result(conn_lines):
    """
    using the connection list, location and etc, plot the result by matplotlib.pyplot.
    """
    x = []
    y = []
    txt = ['depot_0'] + ['customer_%d' % (i+1) for i in range(len(location)-1)]
    for i in range(len(location)):
        x.append(location[i][0])
        y.append(location[i][1])
    connect_x = []
    connect_y = []
    for i in range(len(conn_lines)):
        connect_x.append([location[conn_lines[i][0]][0],
                          location[conn_lines[i][1]][0]])
        connect_y.append([location[conn_lines[i][0]][1],
                          location[conn_lines[i][1]][1]])
    plt.grid(True)
    for i in range(len(connect_x)):
        plt.plot(connect_x[i], connect_y[i], color='#00BFFF')
    plt.scatter(x, y, color='orange')
    plt.scatter(x[0], y[0], color='r')
    for i in range(len(x)):
        plt.annotate(txt[i]+'\n(%d,%d)' % (x[i], y[i]), xy=(x[i], y[i]),
                     xytext=(x[i]+1, y[i]+1), color='black')
    plt.show()


if __name__ == '__main__':
    file_name = 'A-n32-k5.vrp'
    # file_name = 'A-n6-k2.vrp'
    location, demand, K, Q = get_parameter(file_name)
    dist_1dim, cus_depot, num_of_customers, my_obj, lowerbounds, upperbounds, var_types, var_names, lin_expression, row_names, relation, right_side, mapping = get_problem(
        location)
    x = calculate()
    conn_lines = get_connect(x)
    plot_result(conn_lines)
