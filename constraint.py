class ConstraintManager:
<<<<<<< HEAD
    def __init__(self, shiftable_loads, max_grid_charge, soc_0, diesel_capacity, soc_limits=[15, 85], grid_disconnection_period=[18, 21]):
        self.shiftable_loads = shiftable_loads
        self.max_grid_charge = max_grid_charge
        self.soc_limits = soc_limits
        self.diesel_capacity = diesel_capacity
        self.soc_0 = soc_0
        self.grid_disconnection_period = grid_disconnection_period

    def calculate_penalties(self, chromosome):  # SOC Limits, battery degradation, maximum charging rates
        c_rates = chromosome["battery_schedule"]
        battery_soc_penalty = -sum(c_rates) * self.max_grid_charge
        cumulative_list = [sum(c_rates[:i+1])+self.soc_0 for i in range(len(c_rates))]

        # Calculate penalty for SOC limits violation
        soc_penalty = sum([max(0, soc - self.soc_limits[1]) + max(0, self.soc_limits[0] - soc) for soc in cumulative_list])

        # Calculate penalty for battery degradation (assuming it's proportional to the sum of c_rates)
        degradation_penalty = abs(sum(c_rates))

        penalty = battery_soc_penalty + soc_penalty + degradation_penalty

        return penalty

    def correct_constraints(self, chromosome, grid_load):  # grid disconnection, schedule out of allowable period, battery soc level below 0
        c_rates = chromosome["battery_schedule"]
        shed_loads = chromosome["shed_l_schedule"]
        battery_soc_penalty = -sum(c_rates) * self.max_grid_charge
        cumulative_list = [sum(c_rates[:i+1])+self.soc_0 for i in range(len(c_rates))]

        diesel_units =0
        # Correct SOC if it goes below 0
        for i, soc in enumerate(cumulative_list):
            if soc < 0:
                # Use diesel generator if available
                if self.diesel_capacity > 0:
                    diesel_needed = min(-soc, self.diesel_capacity)
                    self.diesel_capacity -= diesel_needed
                    cumulative_list[i] += diesel_needed
                    diesel_units += diesel_needed

                # Shed load if diesel generator is not enough
                if cumulative_list[i] < 0 and i < len(shed_loads):
                    load_shed = min(-cumulative_list[i], shed_loads[i])
                    shed_loads[i] -= load_shed
                    cumulative_list[i] += load_shed

        # Correct for grid disconnection period
        for i in range(self.grid_disconnection_period[0], self.grid_disconnection_period[1]):
            if grid_load[i] > 0:
                # Use diesel generator if available
                if self.diesel_capacity > 0:
                    diesel_needed = min(grid_load[i], self.diesel_capacity)
                    self.diesel_capacity -= diesel_needed
                    grid_load[i] -= diesel_needed
                    diesel_units += diesel_needed

                # Shed load if diesel generator is not enough
                if grid_load[i] > 0 and i < len(shed_loads):
                    load_shed = min(grid_load[i], shed_loads[i])
                    shed_loads[i] -= load_shed
                    grid_load[i] -= load_shed

        chromosome["battery_schedule"] = cumulative_list
        chromosome["shed_l_schedule"] = shed_loads

        return chromosome, self.diesel_capacity
=======

    def __init__(self,load_manager, soc_0, diesel_capacity, soc_limits=[15, 85], grid_disconnection_period=[18, 21]):
        self.soc_limits = soc_limits
        self.diesel_capacity = diesel_capacity
        self.soc_0 = soc_0
        self.load_manager = load_manager
        self.grid_disconnection_period = grid_disconnection_period

    def check_constraints(self, chromosome):
        c_rates = chromosome["battery_schedule"]

        battery_soc = [sum(c_rates[:i+1])+self.soc_0 for i in range(len(c_rates))]

        if any(soc_i < self.soc_limits[0] or soc_i > self.soc_limits[1] for soc_i in battery_soc):
            return False

        grid_load = self.load_manager.get_grid_load(chromosome)

        for i in range(self.grid_disconnection_period[0], self.grid_disconnection_period[1]):
            if grid_load[i] > self.diesel_capacity:
                return False
                
        return True

>>>>>>> main_sl
