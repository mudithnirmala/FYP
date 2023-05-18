#input a chromosome 
#return penalty for constraint violation
# this is a class

class ConstraintManager:
    def __init__(self,shiftable_laods,max_grid_charge,soc_0, soc_limits = [15,85],grid_disconnection_period = []):
        self.constraints = constraints  # list of tuples with (min, max) for each gene in the chromosome
        self.shiftable_laods= shiftable_laods
        self.max_grid_charge= max_grid_charge
        self.soc_limits= soc_limits
    
    def calculate_penalties(self,chromosome): # SOC Limits, battery degradation,  maximum charging rates
        c_rates = chromosome["battery_schedule"]
        battery_soc_penalty = -sum(c_rates) * max_grid_charge
        cumulative_list = [sum(c_rates[:i+1])+soc_0 for i in range(len(c_rates))]

        
        return penalty
    
    def correct_constraints(self,chromosome): # grid disconnection, schedule out of allowable period, battery soc level below 0,
        c_rates = chromosome["battery_schedule"]
        battery_soc_penalty = -sum(c_rates) * max_grid_charge
        cumulative_list = [sum(c_rates[:i+1])+soc_0 for i in range(len(c_rates))]


        return chromosome
