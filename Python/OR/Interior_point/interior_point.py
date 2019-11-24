import numpy as np
import numdifftools as nd
from read_file import *
import matplotlib.pyplot as plt
"""
n: number of variables x
m: number of constraints g_i(X)
we get a (m+n)*(m+n) matrix and manipulate & calculate.
"""


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


def interior_point(f, g, lambd, x, shape):
    """
    matrix manipulation & calculation.
    """
    n, m = shape
    f_Gradient = nd.Gradient(f)
    f_Hessian = nd.Hessian(f)
    g_Hessian = []
    g_Gradient = []
    fff = [0,1] 
    for i in range(m):
        g_Hessian.append(nd.Hessian(g[i]))
        g_Gradient.append(nd.Gradient(g[i]))
    x_delta = np.array([1, 1])
    sign = [True]*len(u)
    for j in range(len(u)):
        # while (x_delta > eps).any():
        # while np.linalg.norm(x_delta,ord=2) > eps:
        # while np.linalg.norm(np.array(f_Gradient(x))) > eps:
        
        while np.linalg.norm(x_delta, ord=2) >= eps or sign[j]:
            sign[j] = False
            
            # assert(feasible(g, x , b, m))
            Sigma_lambda_Hg = 0
            Sigma_lambda_Gg = 0
            for i in range(m):
                Sigma_lambda_Gg += lambd[i]*g_Gradient[i](x)
                Sigma_lambda_Hg += lambd[i]*g_Hessian[i](x)
            gx_t = g_Gradient[0](x)
            for i in range(1, m):
                gx_t = np.append(gx_t, g_Gradient[i](x))
            gx_t = gx_t.reshape(-1, m, order='F')
            # matrix_left
            ml = np.zeros((m+n, m+n), dtype=np.float64)
            ml[0:n, 0:n] = f_Hessian(x) - Sigma_lambda_Hg
            ml[0:n, n:n+m] = - gx_t
            ml[n:n+m, 0:n] = -np.dot(np.diag(lambd), gx_t.T)
            ml[n:n+m, n:n +
                        m] = np.diag([b[i]-g[i](x) for i in range(m)])
            # matrix_right
            mr = np.zeros((n+m, 1), dtype=np.float64)
            mr[0:n, 0] = (- f_Gradient(x) + Sigma_lambda_Gg)
            mr[n:n+m, 0] = [e[i]*u[j] for i in range(len(e))] - (np.dot(np.diag(lambd), np.array(
                [b[i]-g[i](x) for i in range(m)]).reshape(-1, 1))).T
            # judge whether the matrix is invertible.
            if invertible(ml):
                res = np.dot(mr.T, np.linalg.inv(ml))
            else:
                print('we cannot get a invertiable matrix!')

            # res_norm2 = np.linalg.norm(res)
            # direction = res/res_norm2
            x_delta = res[0, 0:n]
            x_delta = np.array(x_delta)
            lambda_delta = res[0, n:n+m]
            x += alpha*x_delta
            lambd += alpha*lambda_delta
            # print(matrix_left)
            print("*"*80)
            print('at this time, i take %f as u' % u[j])
            # print(u[j])
            print("▲x = ", x_delta)
            print("x = ", x)
            print("\033[1;33;40mcurrent lambda = {}\033[0m".format(lambd))
            print("\033[1;33;40mf(x) = {} \033[0m".format(f(x)))
            fff.append(f(x))

    return x, fff


if __name__ == "__main__":
    file_path = "prob1.txt"
    # file_path = "prob2.txt"
    my_obj_type, f, g, shape, b = get_fg(file_path)
    nov, noc = shape
    x = [-1] * nov 
    lambd = [1] * noc
    e = np.ones((1, noc))
    u = np.array([1, 0.5, 0.2, 0.1,0.01])
    alpha = 1
    eps = 1e-2
    x,fff = interior_point(f, g, lambd, x, shape)
    xxx = np.arange(len(fff))
    plt.plot(xxx, fff,'b')  
    plt.show()
