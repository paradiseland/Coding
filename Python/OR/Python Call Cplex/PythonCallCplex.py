"""
use Cplex-Python API to call cplex to solve the mathmatic programming,
especially in mixed integer programming & integer programming.
"""
from Variable import Variable
from Constraint import Constraint
from Objective import Objective
from Result import Result
import cplex
from cplex.exceptions import CplexError


def get_parameter(file_name):
    """
    get the parameters of the problem from the txt file.
    """
    input_problem = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            input_problem.append(line.strip('\n'))
    my_obj_type = input_problem[0]
    my_obj_coe = [int(i) for i in input_problem[1].split(' ')]
    my_lower_bounds = [float(i) for i in input_problem[2].split(' ')]
    my_upper_bounds = [float(i) for i in input_problem[3].split(' ')]
    type_of_variable = [i for i in input_problem[4].split(' ')]
    name_of_variable = [i for i in input_problem[5].split(' ')]
    tech_coe = [j.split(' ')
                for j in [coes for coes in input_problem[6].split(',')]]
    for i in range(len(tech_coe)):
        for j in range(len(tech_coe[i])):
            tech_coe[i][j] = int(tech_coe[i][j])
    sign_of_cons = [i for i in input_problem[7].split(' ')]
    right_of_cons = [float(i) for i in input_problem[8].split(' ')]
    return my_obj_type, my_obj_coe, my_lower_bounds, my_upper_bounds, type_of_variable, name_of_variable, tech_coe, sign_of_cons, right_of_cons


def generate_problem(prob):
    """
    generate the problem from various parameters.
    """
    var_list = [Variable(type_of_var[i], [my_bounds[0][i], my_bounds[1][i]], 'x%d' % (i+1))
                for i in range(len(my_obj.coefficient))]

    var_names = [var_list[i].name for i in range(len(var_list))]
    constraints = [Constraint('c%d' % (i+1), rows[i][1], relation[i], right_side[i])
                   for i in range(len(rows))]
    row_names = [constraints[i].name for i in range(len(constraints))]

    if my_obj.preference == 'min':
        prob.objective.set_sense(prob.objective.sense.minimize)
    elif my_obj.preference == 'max':
        prob.objective.set_sense(prob.objective.sense.maximize)
    else:
        print('You had input the wrong objective preference!')
    prob.variables.add(obj=my_obj.coefficient,
                       lb=my_bounds[0], ub=my_bounds[1], names=var_names, types=type_of_var)
    prob.linear_constraints.add(
        lin_expr=rows, senses=relation, rhs=right_side, names=row_names)
    return var_list, constraints


def calculate():
    try:
        my_prob = cplex.Cplex()
        variables, cons = generate_problem(my_prob)
        my_prob.solve()
    except CplexError as exc:
        print(exc)

    num_rows = my_prob.linear_constraints.get_num()
    num_cols = my_prob.variables.get_num()
    print("Solution status = ", my_prob.solution.get_status(), ":", end=' ')
    print(my_prob.solution.status[my_prob.solution.get_status()])
    print("Solution value  = ", my_prob.solution.get_objective_value())
    # slack = my_prob.solution.get_linear_slacks()
    x = my_prob.solution.get_values()
    # for i in range(num_rows):
    #     print("Row %d:  Slack = %10f" % (i, slack[i]))
    for j in range(num_cols):
        print("Column %d:  Value = %10f " % (j, x[j]))
    res = Result(is_solved=my_prob.solution.get_status(),
                 objective_value=my_prob.solution.get_objective_value(),
                 x_value=x, status=my_prob.solution.status[my_prob.solution.get_status()])
    print("\033[1;31;40m\tProblem:{0}\033[0m\n\033[1;32;40m\tOptimal Value:{1}\033[0m\n\033[1;33;40m\tSolution:{2}\033[0m".format(my_prob.solution.status[res.is_solved],
                                                                res.obj_value, res.x_value))
    outputfile = "output.txt"
    with open(outputfile, 'a+') as out:
        out.write("Solution status = {0}:{1}\n".format(my_prob.solution.get_status(),
                                                       my_prob.solution.status[my_prob.solution.get_status()]))
        out.write("Optimal objective value = {0}".format(
            my_prob.solution.get_objective_value())+'\n')
        for j in range(num_cols):
            out.write("x%d: %.1f" % (j, x[j])+'\n')
    my_prob.write("cplex.lp")


# if __name__ == "__main__":
#     # input the problem
#     # Objective
#     my_obj = Objective('min', [2, -4])
#     # Variable
#     my_bounds = [[0, 0],
#                  [float('inf'), float('inf')]]
#     type_of_var = 'II'
#     # Constraints
#     rows = [[["x1", "x2"], [2, 1]],
#             [["x1", "x2"], [-4, 4]]]
#     relation = 'LL'
#     right_side = [5, 5]
#     calculate()

if __name__ == "__main__":
    my_obj_type, my_obj_coe, my_lower_bounds, my_upper_bounds, type_of_variable, name_of_variable, tech_coe, sign_of_cons, right_of_cons = get_parameter(
        'input2.txt')
    my_obj = Objective(my_obj_type, my_obj_coe)
    my_bounds = [my_lower_bounds, my_upper_bounds]
    type_of_var = type_of_variable[0]
    rows = [[name_of_variable, tech_coe[i]]for i in range(len(tech_coe))]
    relation = sign_of_cons[0]
    right_side = [int(i) for i in right_of_cons]
    calculate()
