import matplotlib.pyplot as plt
import numpy as np
def f(x):
 return -2*x[0]**2-x[1]**2+x[0]*x[1]+5
 
# 生成x,y的数据
n = 256
x = np.linspace(-1.036, 0.964, n)
y = np.linspace(-1.015, 0.985, n)
 
# 把x,y数据生成mesh网格状的数据，因为等高线的显示是在网格的基础上添加上高度值
X, Y = np.meshgrid(x, y)
 
# 填充等高线
plt.contourf(X, Y, f([X, Y]),cmap=plt.cm.hot)

# 添加等高线
C = plt.contour(X, Y, f([X, Y]), 100)
plt.clabel(C, inline=True, fontsize=12)
# 显示图表
plt.show()
