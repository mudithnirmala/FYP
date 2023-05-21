class ConstraintManager:
    def __init__(self, shiftable_loads, sheddable_loads, max_grid_charge, soc_0, diesel_capacity, soc_limits=[15, 85], grid_disconnection_period=[18, 21]):
        self.shiftable_loads = shiftable_loads
        self.sheddable_loads = sheddable_loads
        self.max_grid_charge = max_grid_charge
        self.soc_limits = soc_limits
        self.diesel_capacity = diesel_capacity
        self.soc_0 = soc_0
        self.grid_disconnection_period = grid_disconnection_period
        self.soc_penalty_coefficient = 20000
        self.c_rate_to_units = 400*0.05
        self.diesel_unit_cost = 0.12

    def calculate_penalties(self, chromosome, grid_load):
        c_rates = chromosome["battery_schedule"]
        battery_soc_penalty = -sum(c_rates) * self.max_grid_charge
        cumulative_list = [sum(c_rates[:i+1])+self.soc_0 for i in range(len(c_rates))]

        soc_penalty = self.soc_penalty_coefficient*sum([max(0, soc - self.soc_limits[1]) + max(0, self.soc_limits[0] - soc) for soc in cumulative_list])

        grid_load_copy = grid_load.copy()
        shed_penalty = 0
        diesel_units = 0
        for i in range(self.grid_disconnection_period[0], self.grid_disconnection_period[1]):
            if grid_load_copy[i] > 0:
                diesel_needed = min(grid_load_copy[i], self.diesel_capacity)
                grid_load_copy[i] -= diesel_needed
                diesel_units += diesel_needed

                if grid_load_copy[i]>0 :
                    shedding_n = len(chromosome['shed_l_schedule'])
                    for j,isShed in enumerate(chromosome['shed_l_schedule']):
                        sl = self.sheddable_loads[j]
                        if(isShed and grid_load_copy[i]>0):
                            grid_load_copy[i] -= sl['consumption']
                            grid_load_copy[i] = max(0, grid_load_copy[i])
                            shed_penalty += sl["penalty"]
                            break
                        elif grid_load_copy[i] == 0 and isShed:
                            chromosome['shed_l_schedule'][j] = 0
        print("grid_load - ",grid_load)    
        penalty = battery_soc_penalty + soc_penalty + shed_penalty
        return penalty + diesel_units*self.diesel_unit_cost

    def correct_constraints(self, chromosome):
        c_rates = chromosome["battery_schedule"]
        shed_loads = chromosome["shed_l_schedule"]
        battery_soc_penalty = -sum(c_rates) * self.max_grid_charge
        cumulative_list = [sum(c_rates[:i+1])+self.soc_0 for i in range(len(c_rates))]
        
        chromosome["battery_schedule"] = cumulative_list
        chromosome["shed_l_schedule"] = shed_loads

        return chromosome, self.diesel_capacity
