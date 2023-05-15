from battery import calculate_cyclelife
from battery import battery_degradation_cost,calculate_soc_level
from loads import calculate_shiftable_load_consumption, calculate_shedding_results, calculate_total_load

class CostCalculator:
    BATTERY_CAPACITY = 400000
    def __init__(self, N,soc_0,solar_generation,load_consumption,actual_solar,actual_building,electricity_tariff,shiftable_loads,sheddable_loads):
        
        self.load_consumption = load_consumption
        self.solar_generation = solar_generation
        self.soc_0 = soc_0
        self.shiftable_loads = shiftable_loads
        self.sheddable_loads = sheddable_loads
        self.electricity_tariff = electricity_tariff
    def calculate_bill(self,creature):
        rates = [39, 39, 39, 39, 39, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 55, 55, 55, 55, 39, 39, 39]
        grid_sell_back_rate = 37
        bill=0
        c_rates = creature['battery_schedule']
        for i in range(len(self.load_consumption)):
            net_load = self.load_consumption[i] + (0.05*self.BATTERY_CAPACITY)*c_rates[i] - self.solar_generation[i] 
            rate = rates[i]
            if(net_load<0): rate = 0
            bill+=rate*net_load/1000
        return bill

    def calculate_total_cost(self,creature):

        c_rates = creature['battery_schedule']
        #penalty_1, shed_l = calculate_shedding_results(self.sheddable_loads, creature['shed_l_schedule'])
        #penalty_2, s_loads = calculate_shiftable_load_consumption(self.shiftable_loads, creature['shift_l_schedule'])
        bill = self.calculate_bill(creature)
        bd_cost = battery_degradation_cost(calculate_soc_level(self.soc_0,c_rates))
        soc_level = calculate_soc_level(self.soc_0,c_rates)
        penalty_3 = 1000*abs(sum(c_rates)) if sum(c_rates) < 0 else 0
        if min(soc_level)<15 or max(soc_level)>85:
            penalty_3 +=25000
        return bill + penalty_3
