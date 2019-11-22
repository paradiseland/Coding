import numpy as np
import numdifftools as nd

"""
n: number of variables x
m: number of constraints g_i(X)
we get a (m+n)*(m+n) matrix 
"""

m = 4
n = 2


def invertible(matrix):
    """
    verify that whether the matrix is invertible
    """
    (row, col) = matrix.shape
    assert(row == col)
    inverse = np.linalg.inv(matrix)
    identity = np.diag(np.ones(row))
    eps = 1.0e-10
    return np.linalg.norm(identity - inverse.dot(matrix)) < eps


def f(x): return 8*x[0] + 5*x[1]


def g_1(x): return x[0] + x[1]


def g_2(x): return 9*x[0] + 5*x[1]


def g_3(x): return -x[0]


def g_4(x): return -x[1]



g = []
x = [1,1]
lambd = [2,2,2,2]
b = [6, 45, 0, 0]
e = [1]*m
u = 1
alpha = 0.5
eps = 1e-2
# add a series of constraints into a list
g.append(g_1)
g.append(g_2)
g.append(g_3)
g.append(g_4)

f_Gradient = nd.Gradient(f)
f_Hessian = nd.Hessian(f)
g_Hessian = []
g_Gradient = []
for i in range(m):
    g_Hessian.append(nd.Hessian(g[i]))
    g_Gradient.append(nd.Gradient(g[i]))

x_delta = np.array([1,1])
while (x_delta > eps).all():
    Sigma_lambda_Hg = 0
    Sigma_lambda_Gg = 0
    for i in range(m):
        Sigma_lambda_Gg += lambd[i]*g_Gradient[i](x)
        Sigma_lambda_Hg += lambd[i]*g_Hessian[i](x)
    gx_t = g_Gradient[0](x)

    for i in range(1, m):
        gx_t = np.append(gx_t,g_Gradient[i](x))
        # gx_t = np.append(gx_t, g_Gradient[i](x), axis=1)
    gx_t = gx_t.reshape(-1,m,order='F')
    # matrix_left
    matrix_left = np.zeros((m+n, m+n), dtype=np.float64)
    matrix_left[0:n, 0:n] = f_Hessian(x) - Sigma_lambda_Hg
    matrix_left[0:n, n:n+m] = - gx_t
    matrix_left[n:n+m, 0:n] = np.dot(np.diag(lambd), gx_t.T)

    matrix_left[n:n+m, n:n+m] = np.diag([b[i]-g[i](x) for i in range(m)])
    # matrix_right
    matrix_right = np.zeros((n+m, 1), dtype=np.float64)
    matrix_right[0:n, 0] = (- f_Gradient(x) + Sigma_lambda_Gg)
    matrix_right[n:n+m, 0] = u*e - (np.dot(np.diag(lambd), np.array([b[i]-g[i](x) for i in range(m)]).reshape(-1,1))).T

    if invertible(matrix_left):
        res = np.dot(matrix_right.T, np.linalg.inv(matrix_left))
    else:
        print('we cannot get a invertiable matrix!')
    x_delta = res[0, 0:n]
    x_delta = np.array(x_delta)
    lambda_delta = res[0, n:n+m]

    x += alpha*x_delta
    lambd += alpha*lambda_delta
print('*'*30)
print(x)
print('*'*30)
print(f(x))
