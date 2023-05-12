import numpy as np 
from asyncio import subprocess
import random
import math
from bisect import bisect_right
import matplotlib.pyplot as plt
from tkinter import W 
import subprocess
import sys
import os
import fileinput
from battery import calculate_cyclelife
from battery import battery_degradation_cost, calculate_soc_level
from Input import getInput
from loads import calculate_shiftable_load_consumption, calculate_shedding_results, calculate_total_load

EPS = pow(10,-30)
min_f = pow(10,10)
class GAPopulation:
    @staticmethod
    def mutation(individual, cost_function):
        individual = individual['battery_schedule']
        n = len(individual)
        pos = random.sample(range(n), 2) 
        best_cost = float('inf')
        best_value = -1
        
        for pos1 in pos:
            for value in range(-CHARGING_LEVELS,CHARGING_LEVELS+1):
                new_individual = individual[:pos1] + [value] + individual[pos1+1:]
                cost = cost_function(new_individual)
                if cost < best_cost:
                    best_cost = cost
                    best_value = value
            
            individual = individual[:pos1] + [best_value] + individual[pos1+1:]
            creature = {'battery_schedule':individual,'shed_l_schedule':individual['shed_l_schedule'],'shift_l_schedule':individual['shift_l_schedule']}
        
        return creature
    
        
    @staticmethod
    def get_fitness(self,creature):
        return self.calculator.calculate_total_cost(creature)

    @staticmethod
    def crossover(self,chromosome1,chromosome2):
        min_cost = float('inf')
        for i in range(1,self.T):
            cost1 = self.get_fitness(self,{key: chromosome1[key][:i] + chromosome2[key][i:] for key in chromosome1})
            if cost1   < min_cost:
                min_cost = cost1 
                crossover_point = i
        offspring1 = {}
        offspring2 = {}
        
        for key in chromosome1:
            offspring1[key] = chromosome1[key][:crossover_point] + chromosome2[key][crossover_point:]
        return offspring1
    
    def build_probability(self):
        global min_f
        assert len(self.creatures) > 0
        probs = []
        self.fitness = []
        prob_den =0
        for c in self.creatures:
            f = GAPopulation.get_fitness(self,c)
            min_f = min(f,min_f)
            self.fitness.append(f)
            prob =  1/math.sqrt(math.sqrt(max(100,f-min_f)))
            probs.append(prob)
            prob_den += prob
        self.probs = list(map(lambda x:x/prob_den,probs))

        for i in range(1,len(self.probs)-1):
            self.probs[i] += self.probs[i-1]
            self.probs[-1] = 1+ EPS

    def get_stochastic(self):
        val = random.random() 
        idx = bisect_right(self.probs,val) 
        return self.creatures[idx]

    def __init__(self,T,M1,M2,calculator,creatures=None):
        self.creatures = creatures
        self.CHARGING_LEVELS=10
        self.T = T
        self.M1 = M1
        self.M2 = M2
        self.calculator = calculator
        
        if creatures is not None:
            self.n = len(creatures)
            self.build_probability()

    def init_population(self,size):
        self.n = size
        self.creatures = []
        for _ in range(size): 
            creature ={}
            creature['battery_schedule'] = np.round([max(min(random.gauss(0, self.CHARGING_LEVELS/2),self.CHARGING_LEVELS),-self.CHARGING_LEVELS) for _ in range(self.T)]).astype(int).tolist()
            creature['shift_l_schedule'] = [random.randint(shiftable_loads[i]['start'], shiftable_loads[i]['end']-shiftable_loads[i]['duration']) for i in range(self.M1)]
            creature['shed_l_schedule'] = [random.randint(0,1) for i in range(self.M2)]
            self.creatures.append(creature)
        self.build_probability()

    def next_generation(self,size):
        n_crs = []
        for _ in range(size):
            c1 = self.get_stochastic()
            c2 = self.get_stochastic()
            offs = GAPopulation.crossover(self,c1,c2)
            n_crs.append(offs)
        return GAPopulation(self.T,self.M1,self.M2,self.calculator,n_crs)

    def get_best(self):
        best_val = self.fitness[0]
        best_idx=0
        for i in range(1,len(self.fitness)):
            if self.fitness[i] < best_val:
                best_val = self.fitness[i]
                best_idx = i
        return (self.creatures[best_idx],best_val)

    def print_stats(self):
        global actual_building, actual_solar
        avg_fitness = (sum(self.fitness) + 1.0)/len(self.fitness)
        print('Average Cost of Population  ' + str(avg_fitness)) 
        print(self.get_best())
        print("Daily - Electricity_cost of Best Creature:",self.get_fitness(self,self.get_best()[0])) 

    def get_avg(self):
        return (sum(self.fitness) + 1.0)/len(self.fitness)

    def set_charging_levels(self,cl):
        self.CHARGING_LEVELS=cl