from math import sqrt

a = 4.3/1.2

z = [2, 3, 1, 3]
q = [20, 24, 12, 4]

def cost(k):
    n = len(z)
    cost = 0
    for i in range(n):
        cost += 1/(2*z[i])*(k-1) + (a/2)*(1/z[i])*((q[i]/(z[i]*k)+1)/2)
    print(cost)
    return cost

cost(3)
cost(4)

10.11304012345679
9.695023148148149
