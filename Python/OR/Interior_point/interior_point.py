import numpy as np
import numdifftools as nd
from read_file import *

"""
n: number of variables x
m: number of constraints g_i(X)
we get a (m+n)*(m+n) matrix 
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
    n, m = shape
    f_Gradient = nd.Gradient(f)
    f_Hessian = nd.Hessian(f)
    g_Hessian = []
    g_Gradient = []
    for i in range(m):
        g_Hessian.append(nd.Hessian(g[i]))
        g_Gradient.append(nd.Gradient(g[i]))

    x_delta = np.array([1, 1])
    for i in range(len(u)):
        uu = u[i]
        while (x_delta > eps).any():
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
            matrix_left = np.zeros((m+n, m+n), dtype=np.float64)
            matrix_left[0:n, 0:n] = f_Hessian(x) - Sigma_lambda_Hg
            matrix_left[0:n, n:n+m] = - gx_t
            matrix_left[n:n+m, 0:n] = np.dot(np.diag(lambd), gx_t.T)
            matrix_left[n:n+m, n:n+m] = np.diag([b[i]-g[i](x) for i in range(m)])
            # matrix_right
            matrix_right = np.zeros((n+m, 1), dtype=np.float64)
            matrix_right[0:n, 0] = (- f_Gradient(x) + Sigma_lambda_Gg)
            matrix_right[n:n+m, 0] = [e[i]*uu for i in range(len(e))] - (np.dot(np.diag(lambd), np.array(
                [b[i]-g[i](x) for i in range(m)]).reshape(-1, 1))).T
            # judge whether the matrix is invertible.
            if invertible(matrix_left):
                res = np.dot(matrix_right.T, np.linalg.inv(matrix_left))
            else:
                print('we cannot get a invertiable matrix!')
            x_delta = res[0, 0:n]
            x_delta = np.array(x_delta)
            lambda_delta = res[0, n:n+m]
            x += alpha*x_delta
            lambd += alpha*lambda_delta
            print(matrix_left)
            print(x_delta)
            print(x)
        return x


if __name__ == "__main__":
    file_path = "prob.txt"
    my_obj_type, f, g, shape, b = get_fg(file_path)
    noc = shape[1]
    x = [1, 1]
    lambd = [2, 2, 2, 2]
    e = [1]*noc
    u = np.array([1, 0.5, 0.25, 0.1, 0.01])
    alpha = 0.5
    eps = 0.1
    x = interior_point(f, g, lambd, x, shape)
    print(f(x))
    print(x)
