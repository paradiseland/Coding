# Column generation
__author__ = "XW CHEN"
__version__ = '0.1'


"""
ITER:
while objective_a >= 0:
    do solving the primal 
    from sub problem generate a new column
    add new column into the B/column of constraints
    record the optimal value of the sub problem
get the optimal of the primal
technology coefficients here are the cutting patterns
and the decision variables are  how much optimal solution choose to cut
"""

import pulp
import numpy as np
import copy

M = np.array([[5, 0, 0],
              [0, 4, 0],
              [0, 0, 3]])

b = [20, 25, 30]


def solve_primal(M, b):
    current_prob = pulp.LpProblem('curr-Primal', pulp.LpMinimize)
    num_of_variables = M.shape[1]
    num_of_constraints = M.shape[0]
    variables = [pulp.LpVariable('X%d' % i, lowBound=0, cat=pulp.LpContinuous) for i in range(num_of_variables)]
    constraints = []
    for i in range(num_of_constraints):
        constraints.append(sum([M[i, j] * variables[j] for j in range(num_of_variables)]) >= b[i])
    objective = sum([variables[i] for i in range(num_of_variables)])
    current_prob += objective
    for cons in constraints:
        current_prob += cons
    current_prob.solve()
    res = [v.varValue for v in current_prob.variables()]
    return res


def solve_dual(M,b):
    # Dual：原价值系数为右端常数，原右端常数为价值系数，原系数矩阵的转置为新的系数矩阵，符号约束一致，不等号方向改变
    current_prob_dual = pulp.LpProblem('curr-dual', pulp.LpMaximize)
    B_dual = copy.deepcopy(M)
    B_dual = B_dual.transpose()
    num_of_variables_dual = B_dual.shape[1]
    num_of_constraints_dual = B_dual.shape[0]
    variables_y = [pulp.LpVariable('y%d' % i, lowBound=0, cat=pulp.LpContinuous) for i in range(num_of_variables_dual)]
    objective_y = sum([b[i] * variables_y[i] for i in range(num_of_variables_dual)])
    constraints_y = []
    for i in range(num_of_constraints_dual):
        constraints_y.append(sum([B_dual[i, j] * variables_y[j] for j in range(num_of_variables_dual)]) <= 1)
    current_prob_dual += objective_y
    for cons in constraints_y:
        current_prob_dual += cons
    current_prob_dual.solve()
    res_of_dual = [v.varValue for v in current_prob_dual.variables()]
    return res_of_dual


def column_generate(rod, M):
    # column generation
    variables_a = [pulp.LpVariable('a%d' % i, lowBound=0, cat=pulp.LpInteger) for i in range(3)]
    sub_prob = pulp.LpProblem('sub-prob', pulp.LpMinimize)
    sub_coe = [3, 4, 5]
    constraints_a = []
    # constraints_a.append(sum([sub_coe[i] * variables_a[i] for i in range(len(sub_coe))]) <= 17)
    objective_a = 1 - sum([i * j for i, j in zip(rod, variables_a)])
    sub_prob += objective_a
    sub_prob += 3*variables_a[0] + 4*variables_a[1] + 5*variables_a[2] <= 17
    sub_prob.solve()
    res_of_sub = np.array([v.varValue for v in sub_prob.variables()])
    objective_ = 1 - sum([i * j for i, j in zip(rod, res_of_sub)])
    M = np.c_[M, res_of_sub]
    return M, objective_


# 假设=1 即，让问题进入循环
objective_value = -1
count = 0
while objective_value < -1e-3:
    res_of_primal = solve_primal(M, b)
    res_of_dual = solve_dual(M, b)
    M, objective_value = column_generate(res_of_dual,M)
    print(res_of_dual)
res_of_primal = solve_primal(M, b)
x1 = [0, 0, 0, 2, 12, 0, 4, 0]
print('Cutting patterns Matrix:\n', M)
print('Decision variables:\n', res_of_primal)
print('Reduced Cost:', objective_value)
print('satisfied solution to choose:\n', 'x1:',x1,sum(x1))
