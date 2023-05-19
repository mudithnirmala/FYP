class LoadManager:
    def __init__(self, T, sheddable_loads, shiftable_loads, load_consumption, solar_generation):
        self.T = T
        self.sheddable_loads = sheddable_loads
        self.shiftable_loads = shiftable_loads
        self.load_consumption = load_consumption
        self.solar_generation = solar_generation
        self.BATTERY_CAPACITY = 400000

    def add_load(self,schedule, start_time, period, consumption):
        for i in range(start_time, start_time + period):
            schedule[i % self.T] += consumption

    def remove_load(self, schedule,start_time, period, consumption):
        for i in range(start_time, start_time + period):
            schedule[i % self.T] -= consumption

    def add_generation(self, schedule, start_time, period, generation):
        for i in range(start_time, start_time + period):
            schedule[i % self.T] += generation

    def add_battery_power(self, schedule, battery_charging_rates):
        for i in range(self.T):
            schedule[i] += (0.05*self.BATTERY_CAPACITY)*battery_charging_rates[i]

    def get_grid_load(self,creature):
        return [max(0, self.load_consumption[i] - self.schedule[i] - self.solar_generation[i] + self.battery_charging_rates[i]) for i in range(self.T)]

    def get_grid_load(self, creature):
        net_load_adjustments = [0 for i in range(self.T)] 
      
        shed_loads = [i if creature['shed_l_schedule'][i] == 1 else 0 for i in range(len(creature['shed_l_schedule']))]
        shift_loads = creature['shift_l_schedule']

        battery_charging_rates = creature["battery_schedule"]
        self.add_battery_power(net_load_adjustments, battery_charging_rates)

        for l in shed_loads:
            self.remove_load(net_load_adjustments, l["start_time"],l["period"],l["consumption"])

        for l in shift_loads:
            self.add_load(net_load_adjustments, l["start_time"],l["period"],l["consumption"])

        grid_load = [max(0, self.load_consumption[i] + net_load_adjustments[i] - self.solar_generation[i]) for i in range(self.T)]
        
        return grid_load