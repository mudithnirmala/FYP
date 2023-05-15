class CostCalculator:
    BATTERY_CAPACITY = 400000
    def __init__(self,T, electricity_tariff,diesel_capacity,diesel_unit_cost,penalties):
        
        self.electricity_tariff = electricity_tariff
        self.T = T
        self.diesel_unit_cost = diesel_unit_cost
        self.diesel_capacity = diesel_capacity
        self.penalties = penalties

    def calculate_bill(self,grid_load):
        rates = self.electricity_tariff
        #grid_sell_back_rate = 37
        bill=0
        for i in range(len(grid_load)):
            bill+=rates*grid_load/1000

        return bill

    def calculate_diesel_cost(self,diesel_gen_period):
        return self.diesel_unit_cost*self.diesel_capacity*diesel_gen_period

    def calculate_load_shedding_penalties(self,shed_loads):
        p = 0
        for l in shed_loads:
            p+= self.penalties[l]

        return p
    def get_total_cost(self,grid_load,diesel_gen_period,shed_loads):
        return self.calculate_bill(self,grid_load) + self.calculate_diesel_cost(self,diesel_gen_period)+self.calculate_load_shedding_penalties(self,shed_loads)
       