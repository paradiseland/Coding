import copy
import heapq
import random
import time

import matplotlib.pyplot as plt
import numpy as np

from get_parameter import get_parameters
from haversine import get_distance, haversine
from plot_result import plot


def initialize_poulation():
    """
    Initializing the population, give chromosomes.
    """
    shape_of_population = (POPULATION_SIZE, NUM_OF_CUSTOMER)
    initial_population = np.zeros(shape_of_population, dtype=np.int16)
    for i in range(POPULATION_SIZE):
        initial_population[i] = np.random.permutation(
            range(1, NUM_OF_CUSTOMER + 1))

    return initial_population


def split(population, infomation, trunk):
    """
    Insert 0 into the population to decode the chromosome.
    """
    insert_place = []
    for i in range(POPULATION_SIZE):
        insert_place.append([])
        chromosome = population[i]
        j = 0
        weight = 0
        volume = 0
        while j<= NUM_OF_CUSTOMER - 1:
            if j == NUM_OF_CUSTOMER-1:
                insert_place[i].append(j)
                break
            else:
                if weight+infomation["demand_weight"][chromosome[j]] > trunk[0] or volume+infomation["demand_volume"][chromosome[j]] > trunk[1]:
                    insert_place[i].append(j)
                    weight = 0
                    volume = 0
                else:         
                    weight += infomation["demand_weight"][chromosome[j]]
                    volume += infomation["demand_volume"][chromosome[j]]
                    j += 1
    return insert_place


def get_fitness(population, insert_place, distance):
    """
    According to the decoded chromosomes, compute their fitness 
    """
    shape = (1, POPULATION_SIZE)
    fitness = np.zeros(shape, dtype=np.float32)
    for i in range(POPULATION_SIZE):
        chromosome = population[i]
        Tour = 0
        j_0 = 0
        for j in insert_place[i]:
            Sub_tour = 0
            for k in range(j_0, j):
                Sub_tour += distance[chromosome[k], chromosome[k+1]]
            Sub_tour += distance[0, chromosome[j_0]] + distance[0, chromosome[j]]
            j_0 = j
            Tour += Sub_tour
        fitness[0, i] = Tour
    return fitness


def reproduce(population, fitness, k=40):
    """
    Reproduce from last population.Using the Roulette.
    k: number of elites to be reproduced.
    """
    fitness_new = fitness
    min_num_index = np.argsort(fitness)[0, 0:k]
    elites = population[min_num_index]
    population_reproduced = copy.copy(population)
    population_reproduced[0:k] = elites
    fitness_new[0, 0:k] = fitness[0, min_num_index]

    sum_fit = fitness.sum()
    fitness1 = 1/fitness[0]
    maxFit = np.max(fitness1)
    choose_index = []
    for i in range(POPULATION_SIZE-k):
        ind = int(POPULATION_SIZE*random.random())
        if random.random() <= fitness1[ind]/ maxFit:
            choose_index.append(ind)
            break
    
    # accumulator = 0.0
    # choose_index = []
    # for i in range(POPULATION_SIZE-k):
    #     for ind, val in enumerate(fitness[0]):
    #         accumulator += val
    #         randpoint = random.uniform(0, sum_fit)
    #         if accumulator >= randpoint:
    #             choose_index.append(ind)
    #             break
    population_reproduced[k:POPULATION_SIZE] = population[choose_index]
    fitness_new[0, k:POPULATION_SIZE] = fitness[0, choose_index]
    return population_reproduced, elites, fitness_new


def crossover(population, pc1, pc2, fitness):
    """
    Crossover the population, give the children.
    """
    population_crossovered = np.zeros(population.shape, dtype=np.int16)
    # if int(pc*POPULATION_SIZE) % 2 != 0:
    #     pop_stay = int((1-pc)*POPULATION_SIZE) + 1
    # else:
    #     pop_stay = int((1-pc)*POPULATION_SIZE)

    fit_max = np.max(fitness)
    fit_avg = np.average(fitness)

    tmp = list(range(POPULATION_SIZE))
    # chosen_stayindex = np.random.choice(tmp, pop_stay)
    # population_crossovered[:pop_stay] = population[chosen_stayindex]
    np.random.shuffle(tmp)
    P1 = tmp[:int(POPULATION_SIZE/2)]
    P2 = tmp[int(POPULATION_SIZE/2):]
    Children = np.zeros(population.shape, dtype=np.int16)
    for i in range(int(POPULATION_SIZE/2)):
        mark = max(fitness[0, P1[i]],fitness[0, P2[i]])
        if mark >= fit_avg:
            pc = pc1-(pc1-pc2)*(mark-fit_avg)/(fit_max-fit_avg)
            rand01 = random.random()
            if rand01 < pc:
                new_p1 = np.zeros((1, NUM_OF_CUSTOMER), dtype=np.int16)
                new_p2 = np.zeros((1, NUM_OF_CUSTOMER), dtype=np.int16)
                tmp = list(range(NUM_OF_CUSTOMER))
                m, n = np.random.choice(tmp, 2)
                if m > n:
                    m, n = n, m

                new_p1[0, m:n] = population[P1[i]][m:n]
                new_p2[0, m:n] = population[P2[i]][m:n]

                index_p1_chosen = []
                index_p2_chosen = []
                for j in range(m, n):
                    index_p1_chosen.append(population[P1[i]][j])
                    index_p2_chosen.append(population[P2[i]][j])

                p1_left = copy.deepcopy(population[P1[i]].tolist())
                p2_left = copy.deepcopy(population[P2[i]].tolist())

                for j in index_p2_chosen:
                    p1_left.remove(j)
                for j in index_p1_chosen:
                    p2_left.remove(j)

                for j in population[P2[i], list(range(n, NUM_OF_CUSTOMER))+list(range(NUM_OF_CUSTOMER))]:
                    if j not in population[P1[i]][m:n]:
                        p2_insert_first_element = j
                        break
                for j in population[P1[i], list(range(n, NUM_OF_CUSTOMER))+list(range(NUM_OF_CUSTOMER))]:
                    if j not in population[P2[i]][m:n]:
                        p1_insert_first_element = j
                        break
                p1_insert_first_index = p1_left.index(p1_insert_first_element)
                p2_insert_first_index = p2_left.index(p2_insert_first_element)
                p1_left = p1_left[p1_insert_first_index:] + \
                    p1_left[:p1_insert_first_index]
                p2_left = p2_left[p2_insert_first_index:] + \
                    p2_left[:p2_insert_first_index]
                new_p1[0, n:NUM_OF_CUSTOMER] = p2_left[:NUM_OF_CUSTOMER-n]
                new_p1[0, 0:m] = p2_left[NUM_OF_CUSTOMER-n:]
                new_p2[0, n:NUM_OF_CUSTOMER] = p1_left[:NUM_OF_CUSTOMER-n]
                new_p2[0, 0:m] = p1_left[NUM_OF_CUSTOMER-n:]
                Children[2*i] = new_p1
                Children[2*i+1] = new_p2
        else:
            Children[2*i] = population[P1[i]]
            Children[2*i+1] = population[P2[i]]
            
        
    # tmp = list(range(POPULATION_SIZE))
    # chosen_index = np.random.choice(tmp, POPULATION_SIZE-pop_stay)
    # population_crossovered[pop_stay:] = Children[chosen_index]
    population_crossovered = Children
    return population_crossovered


def mutate(population, pm, elites):
    """
    Mutate the poppulation
    """
    population_mutated = copy.deepcopy(population)
    cur_insert = split(population_mutated, infomation, trunk)
    cur_fit = get_fitness(population_mutated, cur_insert, dist)
    little = len(elites)
    max_num_index = np.argsort(cur_fit)[0, -little:]
    for i, j in zip(max_num_index, range(len(elites))):
        population_mutated[i] = elites[j]
    mutate_size = int(pm * POPULATION_SIZE)
    tmp0 = list(range(POPULATION_SIZE))
    pop_mutated_ind = np.random.choice(tmp0, mutate_size)
    tmp1 = list(range(NUM_OF_CUSTOMER))
    for i in pop_mutated_ind:
        m, n = np.random.choice(tmp1, 2)
        population_mutated[i][m], population_mutated[i][n] = population_mutated[i][n], population_mutated[i][m]

    return population_mutated


def get_solution(chromosome, inser):
    Tour = []
    v_0 = 0
    for i, v in enumerate(inser+[len(location) - 1]):
        Tour.append([])
        Tour[i].append(0)
        for j in range(v_0, v):
            Tour[i].append(chromosome[j])
        v_0 = v
        Tour[i].append(0)
    return Tour

def GA(infomation, trunk, dist):
    iteration = 100
    pc1 = 0.9
    pc2 = 0.6
    pm = 0.2
    pop = initialize_poulation()
    fit = np.full((1, POPULATION_SIZE), 10000)
    Fit = []
    for i in range(iteration):
        reprodeced, elites, fit  = reproduce(pop, fit)
        crossed = crossover(pop, pc1, pc2, fit)
        mutated = mutate(pop, pm, elites)
        pop = mutated
        insert = split(pop, infomation, trunk)
        fit = get_fitness(pop, insert, dist)
        min_index = np.argmin(fit)
        chromosome_best = pop[min_index]
        inse = insert[min_index]

        

        print("min:", fit[0, min_index])
        Fit.append(np.min(fit))
    Tour = get_solution(chromosome_best, inse)
    
    file_handle=open('E:\\SIGS\\Courses\\物流地理信息系统\\作业\\期末作业\\GA_result\\n={}\\Tour.txt'.format(len(dist)-1),mode='a')
    file_handle.write('\n\nmin:{} km'.format(Fit[-1])+'\n'+str(Tour))
    file_handle.close()
    name = 'n={}_converage_min={}.jpg'.format(len(dist)-1, Fit[-1])
    plt.plot(Fit)
    plt.savefig("E:\\SIGS\\Courses\\物流地理信息系统\\作业\\期末作业\\GA_result\\n={}\\".format(len(dist)-1)+name)
    plt.clf()
    # plt.show()
    print(chromosome_best, inse)
    print(Tour)
    plt1 = plot(chromosome_best, inse, location)
    name1 = 'n={}_res_min={}.jpg'.format(len(dist)-1, Fit[-1])
    plt1.savefig("E:\\SIGS\\Courses\\物流地理信息系统\\作业\\期末作业\\GA_result\\n={}\\".format(len(dist)-1)+name1)

    


if __name__ == "__main__":
    start = time.clock()
    #long running
    #do something other
    
    file_name = "assignment.xls"
    info, trunks = get_parameters(file_name)
    prob = 3
    infomation = info[prob]
    trunk = trunks[0]
    dist = get_distance(infomation["location"])
    NUM_OF_CUSTOMER = len(infomation["location"]) - 1
    location = info[prob]["location"]
    POPULATION_SIZE = 100
    GA(infomation, trunk, dist)
    end = time.clock()
    file_t=open('E:\\SIGS\\Courses\\物流地理信息系统\\作业\\期末作业\\GA_result\\n=80\\Tour.txt',mode='a')
    file_t.write('\nCPU time: {}s'.format(end-start))
    file_t.close()
    print ("CPU time:{} s".format(end-start))


