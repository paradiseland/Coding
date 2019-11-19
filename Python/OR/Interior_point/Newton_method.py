"""
@author Xingwei CHEN
"""

import numdifftools as nd
import numpy as np


def feasible(A, x, b):
    """
    verify the solution is feasible, i.e. whether subject to the constraints
    """
    pass
    (row, col) = A.shape
    assert(col == len(x))
    assert(row == len(b))
    slack = b - A.dot(x)
    for i in range(len(slack)):
        if slack[i] < 0:
            return False
    return True


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


# def f(X):
#     """
#     input the function f(x)
#     """
#     pass
#     return X[0]**2-X[0]*X[1]+X[1]**2+X[0]*X[2]+X[2]**2


def newton_method(accuracy, X_t, func,A, x0, b):
    """
    use newton method to slove the root of the function = 0
    """
    pass
    assert(feasible(A,x0,b))
    eps = 1.0e-8
    count = 0
    max_iter_num = 20
    while True:
        count += 1
        if count > max_iter_num:
            break
        gradient = nd.Gradient(func)
        hessian = nd.Hessian(func)    
        assert(invertible(hessian))
        x = x0 - np.linalg.inv(hessian).dot(gradient)
        error = np.linalg.norm(x - x0)
        print('count={},error = {}'.format(count,error))
        x0 = x
        assert(feasible(A, x0, b))
        if error < eps:
            break
    return x0

def solver(t0, A, b, c ,x0, factor, solutionRecords):
    assert(factor > 1)
    assert(t0 > 0)
    upper_bound = 1000 * t0
    t = []
    t.append(t0)
    solution = []
    assert(feasible(A, x0, b))
    solution.append(x0)
    eps = 1.0e-10
    while t0 < upper_bound:
        solution = newton_method(t0, A, c, x0)
        if feasible(A, solution, b):
            diff = solution - x0
            error = np.linalg.norm(diff)
            solution.append(solution)
            print(solution)
            x0 = solution
            t0 = factor * t0
            t.append(t0)
            print("t={},error={}".format(t0,error))
            if error < eps:
                break
        else:
            break
    return x0 




# y_t = func(X_t)
# gap = 1
# df = nd.Gradient(func)
# ddf = nd.Hessian(func)
# while gap > accuracy:
#     X_t = X_t - np.dot(np.linalg.inv(ddf(X_t)), df(X_t))
#     gap = abs(func(X_t))
# return X_t, y_t, gap


def expr_process(line, n_var):
    for i in range(n_var):
        line = line.replace('x%d' % (i+1), 'x[%d]' % i)
    if 'exp' in line:
        line = line.replace('exp', 'np.exp')
    if 'ln' in line:
        line = line.replace('ln', 'np.log')
    if 'log' in line:
        line = line.replace('log', 'np.log10')
    if 'cos' in line:
        line = line.replace('cos', 'np.cos')
    if 'sin' in line:
        line = line.replace('sin', 'np.sin')
    if 'tan' in line:
        line = line.replace('tan', 'np.tan')
    return line


def input_prob(file_path):
    """
    output a f(x) like f(x1,x2,...)+u*\Sigma ln(w_i)
    """
    pass
    input_problem = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            input_problem.append(line.strip('\n'))
    my_obj_type = input_problem[0]
    my_obj_expr = input_problem[1]
    my_obj_split = [int(i) for i in input_problem[1].split(' ')]
    # get num of variables
    while True:
        num_of_var = 0
        for i in range(20):
            if 'x%d' % i in my_obj_expr:
                num_of_var += 1
        break
    # slack variables
    num_of_constraints = len(input_problem)-2
    # give the objective function expression
    my_obj_expr = expr_process(my_obj_expr, num_of_var)
    constraints = []
    for i in range(len(input_problem)-2):
        constraints.append(expr_process(input_problem[2+i], num_of_var))
    # get rightside
    b = []
    for i in range(len(constraints)):
        con_split = constraints[i].split()
        b.append(float(con_split[-1]))
        del con_split[-1]
        del con_split[-1]
        constraints_without_rh = ' '.join(con_split)
    return my_obj_expr, my_obj_type, constraints, b, num_of_constraints

    

    def get_f(obj, cons, b, num_of_constraints):
        """
        give final expression of f(x)
        """
        exec("def f(X):return "+obj+'')
