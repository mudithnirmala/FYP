from battery import calculate_cyclelife
from battery import battery_degradation_cost,calculate_soc_level
from loads import calculate_shiftable_load_consumption, calculate_shedding_results, calculate_total_load

BATTERY_CAPACITY = 400000
def calculate_bill(load_consumption, solar_generation, c_rates):
    global BATTERY_CAPACITY
    rates = [39, 39, 39, 39, 39, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 55, 55, 55, 55, 39, 39, 39]
    #rates = [0.09656, 0.09735, 0.09536, 0.09415, 0.09679, 0.12579, 0.16202, 0.20157, 0.13004, 0.09948, 0.10538, 0.08557, 0.08311, 0.08446, 0.09026, 0.08750, 0.09040, 0.12684, 0.25969, 0.13004, 0.13004, 0.12770, 0.11762, 0.12463]
    grid_sell_back_rate = 37
    bill=0
    #print('c',c_rates)
    #print(len(load_consumption))
    for i in range(len(load_consumption)):
        # Calculate net power consumption or generation
        net_load = load_consumption[i] +(0.05*BATTERY_CAPACITY)*c_rates[i] - solar_generation[i] 
        
        # Determine time of day and apply appropriate rate
        rate = rates[i]

        if(net_load<0): rate = 0 # not in australia
        bill+=rate*net_load/1000

        #print (i,rate,net_load,rate*net_load/1000,bill)
    return bill

def calculate_total_cost(creature,load_consumption,solar_generation,soc_0):
        c_rates = creature['battery_schedule']

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