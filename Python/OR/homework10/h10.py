import numpy as np
import copy
import tabulate

def get_newF(P,F):
    np.fill_diagonal(F,0)
    F = np.dot(P, F)
    # print(tabulate.tabulate(F,"grid"))
    return F


List = [[1/3, 0, 1/3, 0, 0, 1/3],
        [1/2, 1/4, 1/4, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [1/4, 1/4, 1/4, 0, 0, 1/4],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1]]
P = np.array(List)
F = copy.deepcopy(P)
sumF = copy.deepcopy(P)

for i in range(10):
    F = get_newF(P,F)
    sumF += F
    print(tabulate.tabulate(sumF,"grid"))
# print(tabulate.tabulate(P,"grid"))
