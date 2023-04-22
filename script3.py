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

        return bill

        
def objective_function(schedule):
    # Convert the 24-element list to a numpy array
    schedule = np.array(schedule)
    # Calculate the total cost of the schedule
    cost = calculate_total_cost(schedule)
    # Minimize the cost, so return the negative of the cost
    return -cost

# Define the constraints on the battery schedule
constraints = ({'type': 'ineq', 'fun': lambda x: 24 - sum(x)},  # The sum of the battery schedule must be zero
               {'type': 'ineq', 'fun': lambda x: 8 - sum(x < 0)},  # No more than 8 hours of discharging allowed
               {'type': 'ineq', 'fun': lambda x: 8 - sum(x > 0)})  # No more than 8 hours of charging allowed

# Define the bounds on the battery schedule
bounds = [(i, i) for i in range(-3, 4)]

# Define the initial guess for the battery schedule
x0 = [0] * 24

# Use the minimize function to find the optimal battery schedule
result = minimize(objective_function, x0, method='SLSQP', bounds=bounds, constraints=constraints)

# Print the optimal battery schedule and its cost
print("Optimal battery schedule:", result.x)
print(result)
