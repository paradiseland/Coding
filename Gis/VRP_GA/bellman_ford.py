import numpy as np


def bellman_ford(chromosome, distance, info, trunk):
    """
    Using bellman-ford method to compute the minimal route form O point.
    """
    cus_dep = distance.shape[2]
    shape = (1, cus_dep)
    V = np.zeros(shape, dtype=np.float32)
    P = [] # predecessor of node
    for i in range(cus_dep - 1):
        v[i] = 'inf'
        P[i] = i

    for i in range(cus_dep - 1):
        weight = 0
        volume = 0
        length = 0
        j = i
        while True:
            if i == j:
                weight += info["demand_weight"][chromosome[j]]
                volume += info["demand_volume"][chromosome[j]]
                length += distance[0, chromosome[j]]
            else:
                weight += info["demand_weight"][chromosome[j]]
                volume += info["demand_volume"][chromosome[j]]
                length = 0
                length += distance[0, chromosome[j]]
            if weight <= [trunk][0][0] and volume <= trunk[0][1]:
                if V[chromosome[j]] > V[chromosome[i-1]] + length:
                    V[chromosome[j]] = V[chromosome[i-1]] + length
                    P[chromosome[j]] = chromosome[i-1]
                j += 1
            if j > cus_dep or weight > [trunk][0][0] or volume > trunk[0][1]:
                break
    
        Tour = []
        Sub_Tour = []
        tmp = P[chromosome[cus_dep]]
        i = cus_dep

        while i > 0:
            if P[chromosome[i]] == tmp:
                Sub_Tour.append()
