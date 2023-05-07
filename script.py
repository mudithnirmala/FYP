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
from tariff_calculator import calculate_bill
from battery import calculate_cyclelife
from battery import battery_degradation_cost,calculate_soc_level
from Input import getInput
from loads import calculate_shiftable_load_consumption, calculate_shedding_results, calculate_total_load

# Constants
T = 24
M1=0
M2=0
EPS = pow(10,-30)
CHARGING_LEVELS = 10

min_f = pow(10,10)
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
def calculate_total_cost(creature):
        c_rates = creature['battery_schedule']
        global load_consumption,solar_generation,soc_0

        penalty_1, shed_l = calculate_shedding_results(sheddable_loads, creature['shed_l_schedule'])
        penalty_2, s_loads = calculate_shiftable_load_consumption(shiftable_loads, creature['shift_l_schedule'])
        
        bill = calculate_bill(load_consumption, solar_generation, c_rates)
        bd_cost = battery_degradation_cost(calculate_soc_level(soc_0,c_rates))
        load_cost = 0
        soc_level = calculate_soc_level(soc_0,c_rates)
        penalty_3 = 1000*abs(sum(c_rates)) if sum(c_rates) < 0 else 0# abs(sum(c_rates)*800)

        if min(soc_level)<15 or max(soc_level)>85:
            penalty_3 +=25000
        return bill + penalty_3 #+ bd_cost
        #return bill + penalty_3             

def calculate_actual_total_cost(creature):
        c_rates = creature['battery_schedule']
        global load_consumption,solar_generation,soc_0,actual_building, actual_solar

        penalty_1, shed_l = calculate_shedding_results(sheddable_loads, creature['shed_l_schedule'])
        penalty_2, s_loads = calculate_shiftable_load_consumption(shiftable_loads, creature['shift_l_schedule'])
        
        bill = calculate_bill(actual_building, actual_solar, c_rates)
        bd_cost = battery_degradation_cost(calculate_soc_level(soc_0,c_rates))
        load_cost = 0
        soc_level = calculate_soc_level(soc_0,c_rates)
        penalty_3 = 1000*abs(sum(c_rates)) if sum(c_rates) < 0 else 0# abs(sum(c_rates)*800)

        if min(soc_level)<15 or max(soc_level)>85:
            penalty_3 +=25000
        return bill + penalty_3 #+ bd_cost
        #return bill + penalty_3             

def plot(xx,yy,fname):
    plt.plot(xx,yy)
    plt.savefig(fname)


if __name__ == '__main__':
    battery_idle_cost =[]
    optimal_cost = []
    n_iterations =50
    p_size = 1000 #f  larger the population higher chance of finding local min/max, but program becomes slow
    

    for d in range(1):

        print("This is day ",d)

        min_f = pow(10,10)

        N,soc_0,solar_generation,load_consumption,actual_solar,actual_building,electricity_tariff,shiftable_loads,sheddable_loads = getInput(d)
        M1 = len(shiftable_loads)
        M2 = len(sheddable_loads)
        random.seed(666)
     
        #print ('cost', calculate_total_cost({'battery_schedule':[3,3,3,3,3,0,0,0,0,0,0,0,0,0,-2,-2,-2,0,-3,-2,-2,-2,0,0],'shed_l_schedule':[],'shift_l_schedule':[]}))
        print ('Battery idle cost', calculate_actual_total_cost({'battery_schedule':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],'shed_l_schedule':[],'shift_l_schedule':[]}))

        battery_idle_cost.append(calculate_actual_total_cost({'battery_schedule':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],'shed_l_schedule':[],'shift_l_schedule':[]}))
        xx = []
        yy = []
        fname = 'graph.png'

        if len(sys.argv) > 1:
            plot(xx,yy,fname)

        population = Population()
        population.init_population(N,p_size)
        #population.set_input(soc_0,solar_generation,load_consumption,electricity_tariff,shiftable_loads,sheddable_loads)
        #print(population)

        for iteration in range(n_iterations): # iteration = echo
            print()
            print("######################Generation",iteration,"######################")
            print()
            xx.append(iteration)
            yy.append(population.get_avg())
            plot(xx,yy,fname)

            population = population.next_generation(p_size)
            #population.set_input(soc_0,solar_generation,load_consumption,electricity_tariff,shiftable_loads,sheddable_loads)
           # if(iteration %10==0):  
            population.print_stats()

        #optimal_cost.append() max(0,calculate_total_cost(population.get_best()[0])) # for Sri Lanka
        optimal_cost.append(calculate_actual_total_cost(population.get_best()[0])) # for Australia
        # if population.get_best()[1] == 0:
            #    break
        
print("idle vs optimal ",battery_idle_cost,optimal_cost)
print("idle vs optimal ",sum(battery_idle_cost),sum(optimal_cost))