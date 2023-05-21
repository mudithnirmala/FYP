class MicrogridManager:
    def __init__(self, electricity_tariff, penalties, shiftable_loads, sheddable_loads, 
                 max_grid_charge, soc_0, diesel_capacity, load_consumption,
                 diesel_unit_cost=120, soc_limits=[15, 85], grid_disconnection_period=[18, 21]):

        self.electricity_tariff = electricity_tariff
        self.penalties = penalties
        self.shiftable_loads = shiftable_loads
        self.sheddable_loads = sheddable_loads
        self.max_grid_charge = max_grid_charge
        self.soc_limits = soc_limits
        self.diesel_capacity = diesel_capacity
        self.diesel_unit_cost = diesel_unit_cost
        self.soc_0 = soc_0
        self.grid_disconnection_period = grid_disconnection_period
        self.soc_penalty_coefficient = 20000
        self.c_rate_to_units = 400 * 0.05
        self.load_consumption = load_consumption

    def calculate_bill(self, grid_load):
        bill = sum(rate * load / 1000 for rate, load in zip(self.electricity_tariff, grid_load))
        return bill

    def calculate_diesel_cost(self, diesel_gen_period):
        return self.diesel_unit_cost * self.diesel_capacity * diesel_gen_period

    def calculate_load_shedding_penalties(self, shed_loads):
        return sum(self.penalties[l] for l in shed_loads)
        
    def get_total_cost(self, grid_load, shed_loads, diesel_gen_period):        
        return (self.calculate_bill(grid_load) + 
                self.calculate_diesel_cost(diesel_gen_period) + 
                self.calculate_load_shedding_penalties(shed_loads))
    
    def add_shift_load(self, shift_l_schedule):
        shift_load_consumption = [0]*24
        for idx, load in enumerate(self.shiftable_loads):
            for hour in range(shift_l_schedule[idx], shift_l_schedule[idx] + load['duration']):
                shift_load_consumption[hour % 24] += load['consumption']
        return shift_load_consumption

    def calculate_penalties(self, chromosome):
        c_rates = chromosome["battery_schedule"]
        battery_soc_penalty = -sum(c_rates) * self.max_grid_charge
        cumulative_list = [sum(c_rates[:i+1]) + self.soc_0 for i in range(len(c_rates))]
        soc_penalty = self.soc_penalty_coefficient * sum(
            max(0, soc - self.soc_limits[1]) + max(0, self.soc_limits[0] - soc) 
            for soc in cumulative_list)

        shift_load_consumption = self.add_shift_load(chromosome['shift_l_schedule'])

        grid_load = [load - shift + self.c_rate_to_units * rate 
                     for load, shift, rate in zip(self.load_consumption, shift_load_consumption, c_rates)]

        shed_penalty = 0
        diesel_units = 0
        for i in range(self.grid_disconnection_period[0], self.grid_disconnection_period[1]):
            if grid_load[i] > 0:
                diesel_needed = min(grid_load[i], self.diesel_capacity)
                grid_load[i] -= diesel_needed
                diesel_units += diesel_needed

                if grid_load[i] > 0:
                    for j, isShed in enumerate(chromosome['shed_l_schedule']):
                        sl = self.sheddable_loads[j]
                        if isShed and grid_load[i] > 0:
                            grid_load[i] -= sl['consumption']
                            grid_load[i] = max(0, grid_load[i])
                            shed_penalty += sl["penalty"]
                            break

        penalty = battery_soc_penalty + soc_penalty + shed_penalty
        return penalty + diesel_units * self.diesel_unit_cost

    def correct_constraints(self, chromosome):
        c_rates = chromosome["battery_schedule"]
        cumulative_list = [sum(c_rates[:i+1]) + self.soc_0 for i in range(len(c_rates))]
        chromosome["battery_schedule"] = cumulative_list
        return chromosome







#####################################--------------------------------------------------------###############################

class Microgrid:
    def __init__(self, load_consumption, grid_disconnection, battery_soc, shiftable_loads, sheddable_loads, diesel_capacity, creature):
        self.load_consumption = load_consumption
        self.grid_disconnection = grid_disconnection
        self.battery_soc = battery_soc
        self.shiftable_loads = shiftable_loads
        self.sheddable_loads = sheddable_loads
        self.diesel_capacity = diesel_capacity
        self.creature = creature
        self.diesel_cost = 0

    def add_shiftable_loads(self):
        for index, shift_time in enumerate(self.creature['shift_l_schedule']):
            for load in self.shiftable_loads:
                if load['start_time'] <= shift_time <= load['end_time']:
                    self.load_consumption[index] += load['consumption']

    def calculate_diesel_cost(self):
        for hour in self.grid_disconnection:
            if self.load_consumption[hour] > self.diesel_capacity:
                self.diesel_cost += (self.load_consumption[hour] - self.diesel_capacity)
                self.load_consumption[hour] = self.diesel_capacity

    def shed_loads(self):
        for hour in self.grid_disconnection:
            for index, load in enumerate(self.sheddable_loads):
                if self.creature['shed_l_schedule'][index] == 1 and self.load_consumption[hour] + load['consumption'] > self.diesel_capacity:
                    self.load_consumption[hour] -= load['consumption']

    def total_cost(self):
        self.add_shiftable_loads()
        self.calculate_diesel_cost()
        self.shed_loads()
        return self.diesel_cost
