from asyncio import subprocess
import random
from bisect import bisect_right
from tkinter import W # right most number we can insert the number
#import matplotlib.pyplot as plt
import subprocess
import sys
import os
import fileinput


# Constants
N = 24
EPS = pow(10,-30)
CHARGING_LEVELS = 2
shiftable_loads = []
sheddable_loads = []

min_f = pow(10,10)
# Data for the microgrid
solar_generation = []
battery_state = []
load_consumption = []
electricity_cost = []

# Function to calculate the total cost for a day
def calculate_total_cost(battery_state):
    global solar_generation,solar_generation,load_consumption
    total_cost = 0
    battery_capacity = 418.5 # in kWh
    battery_charge = 0 # in Ah

    for i in range(len(solar_generation)):
        excess_solar = max(solar_generation[i] - load_consumption[i], 0)

        if battery_state[i] == 1: # Battery charging
            battery_charge += excess_solar
        elif battery_state[i] == 2: # Battery discharging
            if battery_charge >= load_consumption[i] - solar_generation[i]:
                battery_charge -= load_consumption[i] - solar_generation[i]
            else:
                total_cost += (load_consumption[i] - solar_generation[i] - battery_charge) * electricity_cost[i]
                battery_charge = 0

        else: # Idle state
            if excess_solar > 0:
                total_cost += excess_solar * electricity_cost[i] # Selling excess solar
            elif load_consumption[i] > solar_generation[i] + battery_charge:
                total_cost += (load_consumption[i] - solar_generation[i] - battery_charge) * electricity_cost[i] # Buying from grid
                battery_charge = 0
            else:
                battery_charge -= load_consumption[i] - solar_generation[i]

        if battery_charge > battery_capacity:
            battery_charge = battery_capacity

    return total_cost

# Testing the function with the provided data
total_cost = calculate_total_cost(battery_state)
print(f"Total cost for the microgrid: ${total_cost:.2f}")
class Population:
    @staticmethod
    def mutate(offspring,n):
       # cnt = random.randint(0,5)
        if random.random() < 0.7: 
        #  for i in range(cnt):
            i1 = random.randint(0,n-1)
            i2 = random.randint(0,n-1)
            tmp = offspring[i1]
            offspring[i1] = offspring[i2]
            offspring[i2] = tmp
        return offspring

    @staticmethod
    def get_fitness(creature,n):
        return calculate_total_cost(creature)

    @staticmethod
    def crossover_1(c1,c2,n):
        global N
        ll = random.randint(1,N)
        offspring = [0]*(N)
        for i in range(ll):
            offspring[i]= c1[i]
        for i in range(ll,n):
            offspring[i]= c2[i]
        return Population.mutate(offspring,n)
    
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
            prob = 1/max(100,f+EPS-min_f+2) #pow(1.5,-f) # more conflicts-> less probability, FIND TUNE LATTER
            probs.append(prob)
            prob_den += prob
        self.probs = list(map(lambda x:x/prob_den,probs))

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
            self.n = len(creatures[0])
            self.build_probability()

    def init_population(self,N,size):
        self.n = N-1
        self.creatures = []
        base = list(range(1,N)) 

        for _ in range(size): #Size = 1000
            battery_scedule = [random.randint(0, 2) for _ in range(N)]
            self.creatures.append(battery_scedule)
        self.build_probability()


    def next_generation(self,size):
        n_crs = []
        for _ in range(size):
            c1 = self.get_stochastic()
            c2 = self.get_stochastic()
            offs = Population.crossover_1(c1,c2,self.n)
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
        avg_fitness = (sum(self.fitness) + 1.0)/len(self.fitness)
        #print('ABG Weakness: ' + str(avg_fitness)) 
        #print(self.get_best()[1])
        #print(self.get_best()[0])
        print("Electricity_cost :",calculate_total_cost(self.get_best()[0])) 
        #print("Number of Vehicles : ",int(calculate_total_cost(self.get_best()[0])[-1]/WORK_SECS) +1 )
  
    def get_avg(self):
        return (sum(self.fitness) + 1.0)/len(self.fitness)


def getInput():

    global N,solar_generation, battery_state, load_consumption, electricity_cost

    with open('input.txt','r') as file:
        N = int(file.readline().strip())
        solar_generation = list(map(int,file.readline().strip().split()))
        battery_state = list(map(int,file.readline().strip().split()))
        load_consumption = list(map(int,file.readline().strip().split()))
        electricity_cost = list(map(int,file.readline().strip().split()))

        M1 = int(file.readline().strip())
        for i in range(M1):
            load_data = {}

            start, end, duration, consumption = map(int, file.readline().strip().split())
            load_data['start'] = start
            load_data['end'] = end
            load_data['duration'] = duration
            load_data['consumption'] = consumption

            shiftable_loads.append(load_data)

        M2 = int(file.readline().strip())
        for i in range(M1):
            load_data = {}

            start, end, consumption, cost = map(int, file.readline().strip().split())
            load_data['start'] = start
            load_data['end'] = end
            load_data['consumption'] = consumption
            load_data['cost'] = duration

            sheddable_loads.append(load_data)

#def plot(xx,yy,fname):
    #plt.plot(xx,yy)
    #plt.savefig(fname)


if __name__ == '__main__':

    getInput()

    random.seed(666)
    p_size = 10000 #f  larger the population higher chance of finding local min/max, but program becomes slow

    xx = []
    yy = []
    fname = 'graph.png'

    #if len(sys.argv) > 1:
        #plot(xx,yy,fname)

    population = Population()
    population.init_population(N,p_size)


    for iteration in range(1000): # iteration = echo
        xx.append(iteration)
        yy.append(population.get_avg())
        #plot(xx,yy,fname)

        population = population.next_generation(p_size)
        if(iteration %20==0):  
            population.print_stats()

        if population.get_best()[1] == 0:
            break
