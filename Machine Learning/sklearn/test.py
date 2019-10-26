# 1.1.1
from sklearn import linear_model
reg = linear_model.LinearRegression()
res = reg.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])
print(res.coef_)

# 1.1.2
reg1 = linear_model.Ridge(alpha=0.5)
reg1.fit([[0, 0], [0, 0], [1, 1]], [0, .1, 1])
print(reg1.coef_)
print(reg1.intercept_)

# 1.1.3
reg2 = linear_model.Lasso(alpha=0.1)
reg2.fit([[0, 0], [1, 1]], [0, 1])
print(reg2.coef_)
print(reg2.intercept_)
print(reg2.predict([[1,1]]))