import copy
mapping = {(0, 1): 0, (0, 2): 1}
cur_solution = [0.9, 0.7, 0.5, ...]
mapping_inv = {v:k for k, v in mapping}
label = [True] * len(cur_solution)

solution = copy.deepcopy(cur_solution)
super_vertex = []
cur_nodes = []
eps = 1e-3
def contain_T(x):
    for i in x：
        if i == True:
            temp = True
            break
        else:
            temp = False
    return temp 

while contain_T(label):
    ind_max = solution.index(max(solution))
    solution[ind_max] = 0 
    new_nodes = []
    for p in mapping_inv[ind_max]:
        new_nodes.append(p)
        cur_nodes.append(p)

        
        for m in cur_nodes:
            label[m] = False
            new_nodes = []
            for i in set(range(len(solution)))-{m}:
                if i < m :
                    if mapping[(i, m)] >= eps:
                        new_nodes.append(i)
                else:
                    if mapping[(m, i)] >= eps:
                        new_nodes.append(i)
        
