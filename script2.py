import numpy as np
from scipy.optimize import minimize
import numpy as np 
from asyncio import subprocess
import random
from bisect import bisect_right
from tkinter import W # right most number we can insert the number
#import matplotlib.pyplot as plt
import subprocess
import sys
import os
import fileinput
from tariff_calculator import calculate_bill
from battery import calculate_cyclelife
from battery import battery_degradation_cost,calculate_soc_level
from Input import getInput
from loads import calculate_shiftable_load_consumption, calculate_shedding_results, calculate_total_load

# Constants
N = 24
M1=0
M2=0
EPS = pow(10,-30)
CHARGING_LEVELS = 3

min_f = pow(10,10)
# Data for the microgrid
solar_generation = []
soc_0 = 20
load_consumption = []
electricity_tariff = []
shiftable_loads = []
sheddable_loads = []

shiftable_load_consumption = []
def calculate_total_cost(creature):
        c_rates = creature
        global load_consumption,solar_generation,soc_0

    
        bill = calculate_bill(load_consumption, solar_generation, c_rates)
        bd_cost = battery_degradation_cost(calculate_soc_level(soc_0,c_rates))
        load_cost = 0
        soc_level = calculate_soc_level(soc_0,c_rates)

        penalty_3 = 0
        if min(soc_level)<15 or max(soc_level)>85:
            penalty_3 +=25000
        return bill+ penalty_3

        
# Define the genetic algorithm
def genetic_algorithm(population_size, mutation_rate, generations):
    # Define the initial population
    population = [np.array([random.choice([-3, -2, -1, 0, 1, 2, 3]) for _ in range(24)]) for _ in range(population_size)]

    # Run the genetic algorithm for the specified number of generations
    for gen in range(generations):
        # Calculate the fitness of each individual in the population
        fitness = [calculate_total_cost(schedule) for schedule in population]

        # Select the fittest individuals to serve as parents
        parents = [population[i] for i in np.argsort(fitness)[:int(population_size/2)]]

        # Generate new offspring by crossover and mutation
        offspring = []
        for i in range(population_size - len(parents)):
            parent1, parent2 = random.sample(parents, 2)
            crossover_point = random.randint(1, 23)
            offspring.append(np.concatenate((parent1[:crossover_point], parent2[crossover_point:])))

        # Mutate the offspring
        for i in range(len(offspring)):
            for j in range(24):
                if random.random() < mutation_rate:
                    offspring[i][j] = random.choice([-3, -2, -1, 0, 1, 2, 3])

        # Replace the old population with the new generation of offspring
        population = parents + offspring

    # Return the fittest individual
    fitness = [calculate_total_cost(schedule) for schedule in population]
    fittest_index = np.argmin(fitness)
    return population[fittest_index]

N,soc_0,solar_generation,load_consumption,electricity_tariff,shiftable_loads,sheddable_loads = getInput()
M1 = len(shiftable_loads)
M2 = len(sheddable_loads)
# Run the genetic algorithm to optimize the battery schedule
optimal_schedule = genetic_algorithm(population_size=100, mutation_rate=0.1, generations=100)
print("Optimal battery schedule:", optimal_schedule)
print("Total cost:", calculate_total_cost(optimal_schedule))
