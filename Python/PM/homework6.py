import numpy as np
from itertools import combinations

K = 80
h = 2
d = [12, 55, 40, 15, 19]

dis = np.zeros((5,6))
for i in range(5):
    for j in range(i+1, 6):
        dis[i, j] = K + sum([ind*item*h for ind, item in enumerate(d[i:j])])

print(dis)
com = [()]
for i in range(1,5):
    com += list(combinations(list(range(2,6)), i))
solution = []
for i in com:
    tmp = [1]+list(i)+[6]
    d = 0
    for t in range(len(tmp)-1):
        d += dis[tmp[t]-1, tmp[t+1]-1]
    solution.append(d)
    print(tmp, d)

print(solution.index(min(solution)), min(solution))

