import numpy as np
import matplotlib.pyplot as plt

lambd = 10
K =30
h = 1


n = list(range(1,100))

x = np.arange(1,200, step=.1)

def y(n, T): return n*K/T + lambd*h*T/(2*n)

# for i in n:

#     plt.plot(x,y(i,x))

# plt.show()


# plot min value under different n

# print(list(min([y(i, x) for i in n])))

y_value = []
for j in x:
    tmp = [y(i, j) for i in n]
    # for a fixed t, we have different n to get result
    y_min = min(tmp)
    y_value.append(y_min)
    # print(list(min([y(i,j) for i in n])))
    # print(y_value)
plt.plot(x, y_value, color='red')
plt.show()
