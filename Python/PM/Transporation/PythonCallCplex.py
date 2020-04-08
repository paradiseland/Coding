import numpy as np
import cplex
from cplex.exceptions import CplexError
from Getinput import get_parameters


def get_problem(supply, demand, shape, tech_coe):


    mapping = np.zeros(shape)
    num_of_var = (shape[0]*shape[1])
    # generate a dictionary map 2d->1d variables
    x = 0
    for i in range(shape[0]):
        for j in range(shape[1]):
            mapping[i, j] = x
            x += 1
    rows = []
    for i in range(shape[0]):
        rows.append([['x%d'%(mapping[i,j]) for j in range(shape[1])],[1.0]*shape[1]])
    for i in range(shape[1]):
        rows.append([['x%d'%(mapping[j,i]) for j in range(shape[0])], [1.0]*shape[0]])
    lin_exp = [cplex.SparsePair(ind=rows[i][0], val=rows[i][1]) for i in range(len(rows))]
    var_names = ['x%d'%(i) for i in range(num_of_var)]
    obj_coe = tech_coe
    relation = 'E'*(sum(shape))
    right_side = supply + demand
    rownames = ['r%d'%(i) for i in range(sum(shape))]
    lowerbounds = [0.0] * num_of_var
    upperbounds = [cplex.infinity] * num_of_var
    var_types = 'I' * num_of_var

    return obj_coe, lowerbounds, upperbounds, var_types, var_names, lin_exp, rownames, relation, right_side 


def generate_problem(prob, obj_coe, lowerbounds, upperbounds, var_types, var_names, lin_exp, rownames, relation, right_side):
    """
    generate the problem from parameters
    """
    prob.objective.set_sense(prob.objective.sense.minimize)
    prob.variables.add(obj = obj_coe, lb =lowerbounds, ub=upperbounds, names=var_names,types=var_types)
    prob.linear_constraints.add(lin_expr=lin_exp, senses=relation, rhs=right_side, names=rownames)

def calculate():
    """
    calculate the problem and output the result.
    """
    try:
        my_prob = cplex.Cplex()
        generate_problem(my_prob, obj_coe, lowerbounds, upperbounds, var_types, var_names, lin_exp, rownames, relation, right_side)
        my_prob.solve()
    except CplexError as exc:
        print(exc)
    print("Solution status = ", my_prob.solution.get_status(), ":", end=' ')
    print(my_prob.solution.status[my_prob.solution.get_status()])
    print("Solution value  = ", my_prob.solution.get_objective_value())
    print("decision variables:",my_prob.solution.get_values())

if __name__ == "__main__":
    data_name = "data.txt"
    supply, demand, tech_coe = get_parameters(data_name)
    shape = (len(supply), len(demand))
    obj_coe, lowerbounds, upperbounds, var_types, var_names, lin_exp, rownames, relation, right_side = get_problem(supply, demand, shape, tech_coe)
    calculate()

