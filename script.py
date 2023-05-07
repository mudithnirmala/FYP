from asyncio import subprocess
import math
import random
import matplotlib.pyplot as plt
from cost_calculator import calculate_bill,calculate_total_cost
import gapopulation
from Input import getInput

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
     
        battery_idle_cost.append(calculate_total_cost({'battery_schedule':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],'shed_l_schedule':[],'shift_l_schedule':[]},solar_generation,load_consumption,soc_0))
        xx = []
        yy = []
        fname = 'graph.png'

        if len(sys.argv) > 1:
            plot(xx,yy,fname)

        population = gapopulation.Population()
        population.init_population(N,p_size)
  
        for iteration in range(n_iterations): # iteration = echo
            print()
            print("######################Generation",iteration,"######################")
            print()
            xx.append(iteration)
            yy.append(population.get_avg())
            plot(xx,yy,fname)

            population = population.next_generation(p_size)
            if(iteration %10==0):  
                population.print_stats()

        #optimal_cost.append() max(0,calculate_total_cost(population.get_best()[0])) # for Sri Lanka
        optimal_cost.append(calculate_total_cost(population.get_best()[0])) # for Australia
        # if population.get_best()[1] == 0:
            #    break
        
print("idle vs optimal ",battery_idle_cost,optimal_cost)
print("idle vs optimal ",sum(battery_idle_cost),sum(optimal_cost))