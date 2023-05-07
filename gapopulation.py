import numpy as np 
from asyncio import subprocess
import random
import math
from bisect import bisect_right
import matplotlib.pyplot as plt
from tkinter import W # right most number we can insert the number
#import matplotlib.pyplot as plt
import subprocess
import sys
import os
import fileinput
from cost_calculator import calculate_bill,calculate_total_cost
from battery import calculate_cyclelife
from battery import battery_degradation_cost,calculate_soc_level
from Input import getInput
from loads import calculate_shiftable_load_consumption, calculate_shedding_results, calculate_total_load

class Population:
    @staticmethod
    def mutation(individual, cost_function):
        individual = individual['battery_schedule']
        n = len(individual)
        pos = random.sample(range(n), 2) # try to make this as the standard deviation of the
        best_cost = float('inf')
        best_value = -1
        
        for pos1 in pos:
            # Find best mutation value for first position
            for value in range(-CHARGING_LEVELS,CHARGING_LEVELS+1):
                new_individual = individual[:pos1] + [value] + individual[pos1+1:]
                cost = cost_function(new_individual)
                if cost < best_cost:
                    best_cost = cost
                    best_value = value
            
            # Perform mutation at first position
            individual = individual[:pos1] + [best_value] + individual[pos1+1:]
            creature = {'battery_schedule':individual,'shed_l_schedule':individual['shed_l_schedule'],'shift_l_schedule':individual['shift_l_schedule']}
        
        return creature
    
        
    @staticmethod
    def get_fitness(creature,n):
        return calculate_total_cost(creature)

    @staticmethod
    def crossover(chromosome1, chromosome2,n):
    # determine the crossover point with minimum total cost
        min_cost = float('inf')
        for i in range(1,T):
            cost1 = calculate_total_cost({key: chromosome1[key][:i] + chromosome2[key][i:] for key in chromosome1})
            if cost1   < min_cost:
                min_cost = cost1 
                crossover_point = i
        # perform the crossover at the chosen point for each key in the chromosome
        offspring1 = {}
        offspring2 = {}
        
        for key in chromosome1:
            offspring1[key] = chromosome1[key][:crossover_point] + chromosome2[key][crossover_point:]

        #print ('P1',chromosome1,'\n','P2', chromosome2,'\n','Off_s', offspring1)

        return offspring1
    
    def build_probability(self):
        global min_f
        assert len(self.creatures) > 0
        probs = []
        self.fitness = []
        prob_den =0
        for c in self.creatures:
            f = Population.get_fitness(c,self.n) # total journey distance
            min_f = min(f,min_f)
            self.fitness.append(f)
            #prob = 1/(f-80000) #pow(1.5,-f) # more conflicts-> less probability, FIND TUNE LATTER
            #prob = 1/max(100,f+EPS-min_f+2)
            prob =  1/math.sqrt(math.sqrt(max(100,f-min_f)))
            probs.append(prob)
            prob_den += prob
        self.probs = list(map(lambda x:x/prob_den,probs))
        #print(max(self.probs))

        for i in range(1,len(self.probs)-1):
            self.probs[i] += self.probs[i-1]
            self.probs[-1] = 1+ EPS

    def get_stochastic(self):
        val = random.random() # random number between 0-1
        idx = bisect_right(self.probs,val) #python built in binary search
        return self.creatures[idx]

    def __init__(self,creatures=None):
        self.creatures = creatures
        if creatures is not None:
            self.n = len(creatures)
            self.build_probability()

    def init_population(self,N,size):
        global M1,M2
        self.n = N-1
        self.creatures = []
        base = list(range(1,N))
        #print (M1,M2)
        for _ in range(size): #Size = 1000
            creature ={}
            #creature['battery_schedule'] = [random.randint(-CHARGING_LEVELS, CHARGING_LEVELS) for _ in range(N)]  
            creature['battery_schedule'] = np.round([max(min(random.gauss(0, CHARGING_LEVELS/2),CHARGING_LEVELS),-CHARGING_LEVELS) for _ in range(N)]).astype(int).tolist()
            creature['shift_l_schedule'] = [random.randint(shiftable_loads[i]['start'], shiftable_loads[i]['end']-shiftable_loads[i]['duration']) for i in range(M1)]
            #print(*[(l['start'], l['end'] - l['duration']) for l in shiftable_loads], sep='\n')
            creature['shed_l_schedule'] = [random.randint(0,1) for i in range(M2)]
            self.creatures.append(creature)
           # print (creature['battery_schedule'],calculate_total_cost(creature))
            #print (creature['shed_l_schedule'],calculate_total_cost(creature))
        self.build_probability()

    def next_generation(self,size):
        n_crs = []
        for _ in range(size):
            c1 = self.get_stochastic()
            c2 = self.get_stochastic()
            offs = Population.crossover(c1,c2,self.n)
            #offs = Population.mutation(c1)
            n_crs.append(offs)
        return Population(n_crs)

    def get_best(self):
        best_val = self.fitness[0]
        best_idx=0
        for i in range(1,len(self.fitness)):
            if self.fitness[i] < best_val:
                best_val = self.fitness[i]
                best_idx = i
        return (self.creatures[best_idx],best_val)
        #return ([],best_val)

    def print_stats(self):
        global actual_building, actual_solar
        avg_fitness = (sum(self.fitness) + 1.0)/len(self.fitness)
        print('Average Cost of Population  ' + str(avg_fitness)) 
        #print("Best Schedule is ",self.get_best()[1])
        print(self.get_best())
        #print("Forecasted - Electricity_cost :",calculate_total_cost(self.get_best()[0])) 
        print("Daily - Electricity_cost of Best Creature:",calculate_actual_total_cost(self.get_best()[0])) 
        #print("Number of Vehicles : ",int(calculate_total_cost(self.get_best()[0])[-1]/WORK_SECS) +1 )
  
    def get_avg(self):
        return (sum(self.fitness) + 1.0)/len(self.fitness)

