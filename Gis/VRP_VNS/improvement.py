distance = []
demand_weight = []
demand_volume = []
capacity = 100
weight = 100
volume = 100

def two_opt(tour):
    """
    intra-route improve.
    given the two-opt algorithm to improve current route.
    """
    best_improvement = 0
    node1 = -1
    node2 = -1

    if len(tour) >= 5:
        for i in range(len(tour)-3):
            for j in range(i+2, len(tour)-1):
                new_tour = tour[:i+1] + tour[i+1:j+1][::-1] + tour[j+1:]
                improvement = distance[i, j] + distance[i+1, j+1] - distance[i, i+1] - distance[j, j+1]
                if improvement < best_improvement:
                    node1 = i
                    node2 = j
                    best_improvement = improvement
    return node1, node2, best_improvement


def two_opt_search(sub_tour, distance):
    """
    for all subtour, search that whether there are better subtours.
    """
    Best_Imp = 0
    Tour = []
    Position1 = []
    Position2 = []

    for i in range(len(sub_tour)):
        [Node1, Node2, Imp] = two_opt(sub_tour[i], distance)

        if Node1 != -1:
            Best_Imp += Imp
            Tour.append(i)
            Position1.append(Node1)
            Position2.append(Node2)
    return Tour, Position1, Position2, Best_Imp


def or_opt(tour, distance, K):
    """
    --------------------------
    given the two-opt algorithm to improve current route.
    --------------------------
    K is number of moving customers once. K takes 1, 2 or 3.
    
    return moving interval [i,j], insert place k and best improvement.
    """
    best_imprpvement = 0
    node1 = -1
    node2 = -2
    ndoe3 = -1

    if len(tour) >= K + 3:
        for i in range(len(tour) - K - 1):
            # [i,j] is the moving elements.
            j = i+K
            for k in range(len(tour) - 1):
                # k is the insert place.
                if (k < i) or (j > k):
                    if k < i: # previous: [0, k, i, j]
                        
                        new_tour = tour[0:k+1] + tour[i+1:j+1] + tour[k+1:i+1] + tour[j+1:]
                    else:     # previous: [0, i, j, k:]
                        new_tour = tour[0:i+1] + tour[j+1:k+1] + tour[i+1:j+1] + tour[k+1:]
                    # take apart [i,i+1],[j,j+1] and connect[k,i+1],[j,k+1]
                    Del_Cost = distance[tour[i], tour[i+1]] + distance[tour[j], tour[j+1]] + distance[tour[k], tour[k+1]]
                    improvement = distance[tour[i], tour[j+1]] + distance[tour[k], tour[i+1]] + distance[tour[j], tour[k+1]] - Del_Cost
                    if improvement < best_imprpvement:
                        node1 = i
                        node2 = j
                        node3 = k
                        best_imprpvement = improvement
    return node1, node2, node3, best_imprpvement


def or_opt_search(sub_tour, distance, K):
    Best_Imp = 0
    Tour = []
    Position1 = []
    Position2 = []
    Position3 = []

    for i in range(len(sub_tour)):
        [Node1,Node2,Node3, Imp] = or_opt(sub_tour[i], distance, K)

    if Node1 != -1:
        Best_Imp += Imp
        Tour.append(i)
        Position1.append(Node1)
        Position2.append(Node2)
        Position3.append(Node3)

    return Tour, Position1, Position2, Position3, Best_Imp

def relocate(tour1, tour2, distance, trunk):
    """
    for one customer, arrange it into another subtour.
    """
    best_improvement = 0
    customer = -1
    position = -1

    for i in range(1, len(tour1) - 1):
        if demand_weight[tour1[i]] + sum(demand_weight[tour2]) <= weight and demand_volume[tour1[i]] + sum(demand_volume[tour2]) <= volume:
            for j in range(len(tour2) - 1):
                new_tour2 = tour2[:j+1] + [tour1[i]]+ tour2[j+1:]
            tour1_imp = distance[tour1[i - 1], tour1[i]] + distance[tour1[i], tour1[i+1]] - distance[tour1[i - 1], tour1[i + 1]]
            tour2_inc = distance[tour2[j],tour1[i]] + distance[tour1[i], tour2[j+1]] - distance[tour2[j], tour2[j+1]]
            if (tour2_inc - tour1_imp) < best_improvement:
                best_improvement = tour2_inc - tour1_imp
                customer = i
                position = j
    
    return customer, position, best_improvement


def relocate_search(sub_tour, distance):
    Best_Imp = 0
    T1 = -1
    T2 = -2
    Customer = -1
    Position = -1

    for t1 in range(len(sub_tour)):
        for t2 in range(len(sub_tour)):
            if t1 != t2:
                [customer, position, improvement] = relocate(sub_tour[t1], sub_tour[t2], distance)
                if improvement < Best_Imp:
                    T1 = t1
                    T2 = t2
                    Cust = customer
                    Position = position
                    Best_Imp = improvement
    return T1, T2, Cust, Position, Best_Imp

def exchange(tour1, tour2, distance):
    """
    exchange two customer in two subtours.
    """
    best_improvement = 0
    position = -1
    position = -1

    for i in range(1,len(tour1) - 1):
        for j in range(1, len(tour2)-1):
            tour1_new_weight = demand_weight[tour2[j]] + sum(demand_weight[tour1]) - demand_weight[tour1[i]]
            tour2_new_weight = demand_weight[tour1[i]] + sum(demand_weight[tour2]) - demand_weight[tour2[j]]
            tour1_new_volume = demand_volume[tour2[j]] + sum(demand_volume[tour1]) - demand_volume[tour1[i]]
            tour2_new_volume = demand_volume[tour1[i]] + sum(demand_volume[tour2]) - demand_volume[tour2[j]]
            
            if (tour1_new_weight <= weight) and (tour1_new_volume <= volume) and (tour2_new_weight <= weight) and (tour2_new_volume <= volume):
                ex_cost1 = distance[tour1[i-1], tour2[j]] + distance[tour2[j], tour1[i]] - distance[tour1[i], tour1[i+1]] - distance[tour1[i-1], tour1[i]]
                ex_cost2 = distance[tour2[j-1], tour1[i]] + distance[tour1[i], tour2[j+1]] - distance[tour2[j-1], tour2[j]] - distance[tour2[j], tour2[j+1]]
                if (ex_cost1 + ex_cost2) < best_improvement:
                    best_improvement = ex_cost1 + ex_cost2
                    position1 = i
                    position2 = j

    return position1, position2, best_improvement


def exchange_search(sub_tour, distance):
    Best_Imp = 0
    T1 = -1
    T2 = -1
    Position1 = -1
    Position2 = -1

    for t1 in range(len(sub_tour) - 1):
        for t2 in range(t1 + 1, len(sub_tour)):
            [position1,position2, imp] = exchange(sub_tour[t1], sub_tour[t2], distance)
            if imp < Best_Imp:
                T1 = t1
                T2 = t2
                Position1 = position1
                Position2 = position2
                Best_Imp = imp
    
    return T1, T2, Position1, Position2, Best_Imp

def cross(tour1, tour2, distance):
    best_improvement = 0
    node11 = -1
    node12 = -1
    node21 = -1
    node22 = -1

    for i in range(1, len(tour1) - 2):
        for k in range(i+1, len(tour1)-1):
            for j in range(1, len(tour2) - 2):
                for l in range(j+1, len(tour2) - 1):
                    tour1_new_weight = sum(demand_weight[tour1])
                    tour1_new_volume = 

