"""
read the .txt to get the problem.
"""


def read_file(file_name):
    """
    read the .txt and get contents & parameters.
    """
    input_problem = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            input_problem.append(line.strip('\n'))
    my_obj_type = input_problem[0].split()[0]
    my_obj_expr = input_problem[0].split()[1]
    # get num of variables
    while True:
        num_of_var = 0
        for i in range(20):
            if 'x%d' % i in my_obj_expr:
                num_of_var += 1
        break
    num_of_constraints = len(input_problem)-1
    # record a list including all the constraints
    g = []
    b = []
    for i in range(1, num_of_constraints+1):
        # judge the sign of inequality
        if '<' in input_problem[i].split()[1]:
            g.append(input_problem[i].split()[0])
            b.append(input_problem[i].split()[2])
            pass
        elif '>' in input_problem[i].split()[1]:
            g.append('-' + input_problem[i].split()[0])
            b.append('-' + input_problem[i].split()[2])

        else:
            raise AssertionError(
                "This problem has a or more binding constaints!")

    return my_obj_type, my_obj_expr, num_of_var, num_of_constraints, g, b


def expr_process(line, n_var):
    for i in range(n_var):
        line = line.replace('x%d' % (i), 'x[%d]' % i)
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


def get_fg(file_path):
    my_obj_type, moe, nov, noc, gx, b = read_file(file_path)
    b = [float(b[i]) for i in range(len(b))]
    shape = (nov, noc)
    moe = expr_process(moe, nov)
    my_obj_expr = expr_process(moe, nov)
    # f= 0
    exec("def f(x): return " + my_obj_expr)
    ff = []
    exec("ff.append(f)")
    for i in range(noc):
        gx[i] = expr_process(gx[i], nov)
        exec("def g_%d(x): return "%(i+1) + gx[i])
    g = []
    for i in range(noc):
        exec("g.append(g_" + str(i+1)+")")
    
    return my_obj_type , ff[0], g, shape,b

    

if __name__ == "__main__":
    file_path = "prob.txt"
    x = [1,1]
    my_obj_type , f, g, shape, b = get_fg(file_path)
    print(f(x))
    print(g)
    print(my_obj_type,f,g,shape,b)
