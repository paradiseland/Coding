# -*- coding: utf-8 -*-
# The MIP problem solved in this example is:
#(2,6),(2,3),(6,5),(5,4),(4,6)，：：(2,1),(3,3),(6,9),(5,7),(4,5)，：：(2,2),(2,4.5),(6,7.5),(5.5,4。5),(7.4,8.6）
#   Maximize  6x1 + 3 x2 + 5 x3 + 4 x4 +6 x5+ x6 +3x7 + 9 x8+7 x9+5 x10+ 2 x11 +4.5 x12+7.5 x13 + 4.5x14 +8.6x15= 价值最大化
#   Subject to
#      (2,6),(2,3),(6,5),(5,4),(4,6)，：：(2,1),(3,3),(6,9),(5,7),(4,5)，：：(2,2),(2,4.5),(6,7.5),(5.5,4。5),(7.4,8.6）      重量小于背包的盛重量
#       2x1 + 2 x2 + 6 x3 + 5 x4 +4 x5+ 2 x6 +3x7 + 6 x8+7 x9+5 x10+ 2 x11 +2 x12+6 x13 + 5.5 x14 +7.4x15
#      -x2+ x5<=0                2号背包必须在五号背包之前放入
#   Bounds             对于各个背包要么取要么不取0 1二值问题

#        0 <= x1 <= 1
#        0 <= x2 <= 1
#        0 <= x3 <= 1
#        0 <= x4 <= 1
#        0 <= x5 <= 1
#        0 <= x6 <= 1
#        0 <= x7 <= 1
#        0 <= x8 <= 1
#        0 <= x9 <= 1
#        0 <= x10 <= 1
#        0 <= x11 <= 1
#        0 <= x12 <= 1
#        0 <= x13 <= 1
#        0 <= x14 <= 1
#        0 <= x15 <= 1
#   Integers
#       x1,x2,x3,x4,x5，x6,x7,x8,x9,x10,x11,x12,x13,x14,x15

import cplex
from cplex.exceptions import CplexError
# (2,6),(2,3),(6,5),(5,4),(4,6)，：：(2,1),(3,3),(6,9),(5,7),(4,5)，：：(2,2),(2,4.5),(6,7.5),(5.5,4。5),(7.4,8.6）
# data common to all populateby functions
my_obj = [2, -4]
my_ub = [cplex.infinity, cplex.infinity]
my_lb = [0, 0]
my_ctype = "II"     #表示参数的类型 c应该表示数值，I表示整数
my_colnames = ["x1", "x2"]  #表示实验的
my_rhs = [5, 5]
my_rownames = ["r1", "r2"]
my_sense = 'LL'


def populatebyrow(prob):
  prob.objective.set_sense(prob.objective.sense.minimize)
  # 指要优化的目标函数是要求最大化
  prob.variables.add(obj=my_obj, lb=my_lb, ub=my_ub, types=my_ctype,
                     names=my_colnames)

  rows = [[["x1", "x2"], [2, 1]],
          [["x1","x2"],[-4,4]]
          ]
  prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
                              rhs=my_rhs, names=my_rownames)


try:
  my_prob = cplex.Cplex()
  handle = populatebyrow(my_prob)
  my_prob.solve()

except CplexError as exc:
  print(exc)

print()
# solution.get_status() returns an integer code
print("Solution status = ", my_prob.solution.get_status(), ":", end=' ')
# the following line prints the corresponding string
print(my_prob.solution.status[my_prob.solution.get_status()])
print("Solution value  = ", my_prob.solution.get_objective_value())

numcols = my_prob.variables.get_num()
numrows = my_prob.linear_constraints.get_num()

slack = my_prob.solution.get_linear_slacks()
x = my_prob.solution.get_values()

print('x: ')
print(x)