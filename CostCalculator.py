class CostCalculator:
<<<<<<< HEAD
    BATTERY_CAPACITY = 400000
    def __init__(self,T, electricity_tariff,penalties,diesel_capacity=100000,diesel_unit_cost=120):
=======
    def __init__(self,T, electricity_tariff,sheddable_penalties,load_manager,diesel_unit_cost=0.120):
>>>>>>> main_sl
        
        self.electricity_tariff = electricity_tariff
        self.T = T
        self.diesel_unit_cost = diesel_unit_cost
<<<<<<< HEAD
        self.diesel_capacity = diesel_capacity
        self.penalties = penalties

    def calculate_bill(self,grid_load):
        rates = self.electricity_tariff
        #grid_sell_back_rate = 37
        bill=0
        for i in range(len(grid_load)):
            bill+=rates[i]*grid_load[i]/1000

        return bill

    def calculate_diesel_cost(self,diesel_gen_period):
        return self.diesel_unit_cost*self.diesel_capacity*diesel_gen_period

    def calculate_load_shedding_penalties(self,shed_loads):
        p = 0
        for l in shed_loads:
            p+= self.penalties[l]

        return p
        
    def get_total_cost(self,grid_load,shed_loads,diesel_gen_period):
        
        return self.calculate_bill(grid_load) + self.calculate_diesel_cost(diesel_gen_period)+self.calculate_load_shedding_penalties(shed_loads)
       
=======
        self.sheddable_penalties = sheddable_penalties
        self.load_manager = load_manager

    def calculate_bill(self, grid_load):
        bill = sum(rate * load / 1000 for rate, load in zip(self.electricity_tariff, grid_load))
        return bill
    
    def calculate_diesel_cost(self,diesel_units):
        return diesel_units*self.diesel_unit_cost

    def calculate_shed_penalties(self,shedded_loads):
        return sum(self.sheddable_penalties[p_i] for i, p_i in enumerate(shedded_loads))

    def get_total_cost(self,chromosome):
        grid_load = self.load_manager.get_grid_load(chromosome)
        diesel_units = self.load_manager.get_diesel_units(chromosome)
        shedded_loads = [i if chromosome['shed_l_schedule'][i] == 1 else 0 for i in range(len(chromosome['shed_l_schedule']))]
        
        return self.calculate_bill(grid_load) + self.calculate_diesel_cost(diesel_units) + self.calculate_shed_penalties(shedded_loads)
>>>>>>> main_sl
