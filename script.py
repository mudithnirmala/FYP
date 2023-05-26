from asyncio import subprocess
import math
import random
import matplotlib.pyplot as plt
from population import GAPopulation 
from Input import getInput
from constraint import ConstraintManager
from CostCalculator import CostCalculator
from loads import LoadManager
from dp import find_optimal_battery_dispatch

# Constants
T = 24
M1=0
M2=0
diesel_capacity = 600000
CHARGING_LEVELS = 10


# Data for the microgrid
solar_generation = []
soc_0 = 0
load_consumption = []
electricity_tariff = []
shiftable_loads = []
sheddable_loads = []
actual_solar = []
actual_building = []

shiftable_load_consumption = []

def plot(xx,yy,fname):
    plt.plot(xx,yy)
    plt.savefig(fname)


if __name__ == '__main__':
    battery_idle_cost =[]
    optimal_cost = []
    n_iterations =50
    p_size = 1000 #f  larger the population higher chance of finding local min/max, but program becomes slow
    random.seed(666)

    for d in range(1):

        print("This is day ",d)

        min_f = pow(10,10)

        T,soc_0,solar_generation,load_consumption,actual_solar,actual_building,electricity_tariff,shiftable_loads,sheddable_loads = getInput(d)
        grid_disconnection_period = [18,21]
        CHARGING_LEVELS = 10
        soc_limits = [15,85]
        diesel_capacity = 600000

        M1 = len(shiftable_loads)
        M2 = len(sheddable_loads)
        
        penalties = [sheddable_loads[i]['penalty'] for i in range(len(sheddable_loads))]
        
        
        load_manager = LoadManager(T, sheddable_loads, shiftable_loads, load_consumption, solar_generation, grid_disconnection_period)
        calculator = CostCalculator(T, electricity_tariff, penalties, load_manager)
        constraint_manager = ConstraintManager(load_manager, soc_0, diesel_capacity, soc_limits, grid_disconnection_period)

        print("dp solution ",find_optimal_battery_dispatch(T,calculator))
        #battery_idle_cost.append(calculator.calculate_total_cost({'battery_schedule':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],'shed_l_schedule':[],'shift_l_schedule':[]}))
        creature = {'battery_schedule':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],'shed_l_schedule':[],'shift_l_schedule':[]}
        grid_load = load_manager.get_grid_load(creature)
        #print(grid_load)
        #print(calculator.get_total_cost(grid_load,[],0 ))
        #print("electricity tariff ",electricity_tariff)

        population = GAPopulation(T, M1, M2,calculator,constraint_manager)
        population.init_population(p_size,CHARGING_LEVELS,shiftable_loads)
  
        for iteration in range(n_iterations): # iteration = echo
            print()
            print("######################Generation",iteration,"######################")
            print()
            

            population = population.next_generation(iteration,p_size)
            if(iteration %1==0):  
                population.print_stats(load_manager)

        # optimal_cost.append() max(0,calculate_total_cost(population.get_best()[0])) # for Sri Lanka
        # optimal_cost.append(calculate_total_cost(population.get_best()[0])) # for Australia


print("idle vs optimal ",battery_idle_cost)
