class ConstraintManager:
    def __init__(self, shiftable_loads,shedding_levels, max_grid_charge, soc_0, diesel_capacity, soc_limits=[15, 85], grid_disconnection_period=[18, 21]):
        self.shiftable_loads = shiftable_loads
        self.shedding_levels = shedding_levels
        self.max_grid_charge = max_grid_charge
        self.soc_limits = soc_limits
        self.diesel_capacity = diesel_capacity
        self.soc_0 = soc_0
        self.grid_disconnection_period = grid_disconnection_period
        self.soc_penalty_coefficient = 1000 # UPDATE THIS LATER
        self.c_rate_to_units = 400*0.05

    def calculate_penalties(self, chromosome, grid_load):  # SOC Limits, battery degradation, maximum charging rates
        c_rates = chromosome["battery_schedule"]
        battery_soc_penalty = -sum(c_rates) * self.max_grid_charge
        cumulative_list = [sum(c_rates[:i+1])+self.soc_0 for i in range(len(c_rates))]

        # Calculate penalty for SOC limits violation ### TRY to SQUARE THIS
        soc_penalty = self.soc_penalty_coefficient*sum([max(0, soc - self.soc_limits[1]) + max(0, self.soc_limits[0] - soc) for soc in cumulative_list])

        # Calculate penalty for battery degradation (assuming it's proportional to the sum of c_rates)
        degradation_penalty = abs(sum(c_rates)) #### USE BATTERY DEGRADATION COST ESTIMATION

        # Correct for grid disconnection period
        shed_penalty =0
        for i in range(self.grid_disconnection_period[0], self.grid_disconnection_period[1]):
            if grid_load[i] > 0:
                # Use diesel generator if available
                if self.diesel_capacity > grid_load[i]:
                    diesel_needed = min(grid_load[i], self.diesel_capacity)
                    grid_load[i] -= diesel_needed
                    diesel_units += diesel_needed

                else:
                    # Shed load if diesel generator is not enough
                    sheddling_n = len(chromosome['shed_l_schedule'])
                    for i,isShed in enumerate(chromosome['shed_l_schedule']):
                        if(isShed grid_load[i]<sl["load"]):
                            shed_penalty += sl["penalty"]
                            break
                    
        penalty = battery_soc_penalty + soc_penalty + degradation_penalty +shed_penalty

        return penalty

    def correct_constraints(self, chromosome):  # grid disconnection, schedule out of allowable period, battery soc level below 0
        c_rates = chromosome["battery_schedule"]
        shed_loads = chromosome["shed_l_schedule"]
        battery_soc_penalty = -sum(c_rates) * self.max_grid_charge
        cumulative_list = [sum(c_rates[:i+1])+self.soc_0 for i in range(len(c_rates))]
        
        chromosome["battery_schedule"] = cumulative_list
        chromosome["shed_l_schedule"] = shed_loads

        return chromosome, self.diesel_capacity
