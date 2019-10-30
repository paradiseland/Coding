from Variable import Variable
from Constraint import Constraint
from Objective import Objective
from Result import Result
import cplex
from cplex.exceptions import CplexError


def generate_problem(prob):
    var_list = [Variable(type_of_var[i], [my_bounds[0][i], my_bounds[1][i]], 'x%d' % (i+1))
                for i in range(len(my_obj.coefficient))]

    var_names = [var_list[i].name for i in range(len(var_list))]
    constraints = [Constraint('x%d' % (i+1), rows[i][1], relation[i], right_side[i])
                   for i in range(len(rows))]
    row_names = [constraints[i].name for i in range(len(constraints))]

    if my_obj.preference == 'min':
        prob.objective.set_sense(prob.objective.sense.minimize)
    elif my_obj.preference == 'max':
        prob.objective.set_sense(prob.objective.sense.maximize)
    else:
        print('You had input the wrong objective preference!')
    prob.variables.add(obj=my_obj.coefficient, lb=my_bounds[0], ub=my_bounds[1], names=var_names, types=type_of_var)
    prob.linear_constraints.add(lin_expr=rows, senses=relation, rhs=right_side, names=row_names)
    return var_list, constraints


def calculate():
    try:
        my_prob = cplex.Cplex()
        variables, cons = generate_problem(my_prob)
        my_prob.solve()
    except CplexError as exc:
        print(exc)
    num_rows = len(cons)
    num_cols = len(variables)
    print("Solution status = ", my_prob.solution.get_status(), ":", end=' ')
    print(my_prob.solution.status[my_prob.solution.get_status()])
    print("Solution value  = ", my_prob.solution.get_objective_value())
    slack = my_prob.solution.get_linear_slacks()
    x = my_prob.solution.get_values()
    for i in range(num_rows):
        print("Row %d:  Slack = %10f" % (i, slack[i]))
    for j in range(num_cols):
        print("Column %d:  Value = %10f " % (j, x[j]))
    res = Result(is_solved=my_prob.solution.get_status(),
                 objective_value=my_prob.solution.get_objective_value(),
                 x_value=x, status=my_prob.solution.status[my_prob.solution.get_status()])
    print("Problem:{0}\nOptimal Value:{1}\nSolution:{2}".format(my_prob.solution.status[res.is_solved],
                                                                res.obj_value, res.x_value))
    # my_prob.write("cplex.lp")


if __name__ == "__main__":
    # input the problem
    # Objective
    my_obj = Objective('min', [2, -4])
    # Variable
    my_bounds = [[0, 0],
                 [cplex.infinity, cplex.infinity]]
    type_of_var = 'II'
    # Constraints
    rows = [[["x1", "x2"], [2, 1]],
            [["x1", "x2"], [-4, 4]]]
    relation = 'LL'
    right_side = [5, 5]
    calculate()
