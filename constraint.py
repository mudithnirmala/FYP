class ConstraintManager:

    def __init__(self,load_manager, soc_0, diesel_capacity, soc_limits=[15, 85], grid_disconnection_period=[18, 21]):
        self.soc_limits = soc_limits
        self.diesel_capacity = diesel_capacity
        self.soc_0 = soc_0
        self.load_manager = load_manager
        self.grid_disconnection_period = grid_disconnection_period

    def check_constraints(self, chromosome):
        c_rates = chromosome["battery_schedule"]

        battery_soc_penalty = -sum(c_rates) * self.max_grid_charge
        
        battery_soc = [sum(c_rates[:i+1])+self.soc_0 for i in range(len(c_rates))]

        if any(soc_i < self.soc_limits[0] or soc_i > self.soc_limits[1] for soc_i in battery_soc):
            return False

        grid_load = self.load_manager.get_grid_load(chromosome)

        for i in range(self.grid_disconnection_period[0], self.grid_disconnection_period[1]):
            if grid_load[i] > self.diesel_capacity:
                return False
                
        return True

