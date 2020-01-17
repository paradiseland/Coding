import numpy as np
import matplotlib.pyplot as plt
from get_parameter import get_parameters
from haversine import haversine

def get_distance(location):
    distance = np.zeros((len(location),len(location)))
    for i in range(len(location)):
        for j in range(len(location)):
            distance[i, j] = haversine(location[i], location[j])
    return distance


def total_distance(tours, distance):
    """
    from given tours, calculate the total distance / Objective Function.
    """
    total_distance = 0
    for tour in tours:
        tour_distance = 0
        for i in range(len(tour)-1):
            tour_distance += distance[tour[i], tour[i+1]]
        total_distance += tour_distance
    return total_distance


def main():
    pass
    Nb_NoImp = 0
    iter = 0
    Improvement = 'inf'

    Neighbour_order = [4,5,6,7,8,9,10,1,2,3]

    Neighbour_Str = 0
    stop = False

    while stop != True:
        iter += 1
        if Neighbour_order[Neighbour_Str] == 0: # 2opt
            [] = two_opt_Search()

        elif  todo :
        
        ...


        Best_Improvement = round(Improvement, 5)
        
        if Best_Improvement < 0:
            get_newtour()
        else:
            Nb_NoImp += 1

            if Nb_NoImp > len(Neighbour_order):
                stop = True
            else:
                if Neighbour_Str >= len(Neighbour_order) - 1:
                    Neighbour_Str = 0
                    stop = False
                else:
                    Neighbour_Str += 1

def shaking():
    pass

file_name = "assignment.xls"

dis_matrix = get_distance()

# Route Construction
customer = 0
Sub_tour = []
for i in range(1, customer+1):
    sub = [0, i, 0]
    Sub_tour.append(sub)
sub_size = len(Sub_tour) 

saving_list = []
for i in range(sub_size):
    for j in range(sub_size):
        if i != j:
            saving = round(dis_matrix[i,0]+dis_matrix[0,j]-dis_matrix[i,j], 2)
            saving_list._append([i, j, saving])

np.asarray(saving_list)
saving_list_sorted = sorted(saving_list,key=lambda x: x[2], reverse = True)
while len(saving_list_sorted) > 0:
    ind = saving_list_sorted[0][:2]
    a = [i for i in range(len(Sub_tour)) if ind[0] in Sub_tour[i]]
    b = [i for i in range(len(Sub_tour)) if ind[1] in Sub_tour[i]]

    if a != b:
        new_sub1 = Sub_tour[a[0]][::-1][:-1] + Sub_tour[b[0]][1:]
        new_sub12 = Sub_tour[a[0]][::-1][:-1] + Sub_tour[b[0]][::-1][1:]
        new_sub13 = Sub_tour[a[0]][:-1] + Sub_tour[b[0]][1:]
        new_sub14 = Sub_tour[a[0]][:-1] + Sub_tour[b[0]][::-1][1:]    












        
def vns(info,trunk):
    """
    main program of variable neighbourhood search
    """
    # shaking
    distance = get_distance(info[0]["location"])
    pass
    

if __name__ == "__main__":
    file_name = "assignment.xls"
    info, trunk = get_parameters(file_name)
    neighbourhood = []
    dist = get_distance(info[0]["location"])
    print(dist, np.amax(dist), type(dist),sep="\n")
