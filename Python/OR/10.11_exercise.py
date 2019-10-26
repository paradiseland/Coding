import numpy as np
from scipy import optimize

# 1 iteration
c = np.array([2, -4, 0, 0, 0, 0])
aeq = np.array([[2, 1, 1, 0, 0, 0],
                [-4, 4, 0, 1, 0, 0],
                [0, 0, -1/3, -1/6, 1, 0],
                [0, 0, 0, -1, 0, 1]])
beq = np.array([5, 5, -1/2, -1])
res = optimize.linprog(c, A_eq=aeq, b_eq=beq)
print(res,'\n',"*"*50)
# cut 1
c = np.array([2, -4, 0, 0, 0])
aeq = np.array([[2, 1, 1, 0, 0], [-4, 4, 0, 1, 0],[0, 0, -1/3, -11/12, 1]])
beq = np.array([5, 5, -1/14])

res1 = optimize.linprog(c, A_eq=aeq, b_eq=beq)
print(res1)
# [1.25 2.5  0.   0.  ]

