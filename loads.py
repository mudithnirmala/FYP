class LoadManager:
    def __init__(self, T, sheddable_loads, shiftable_loads, load_consumption, solar_generation):
        self.T = T
        self.sheddable_loads = sheddable_loads
        self.shiftable_loads = shiftable_loads
        self.load_consumption = load_consumption
        self.solar_generation = solar_generation

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
            schedule[i] += battery_charging_rates[i]

    def get_grid_load(self,creature):
        return [max(0, self.load_consumption[i] - self.schedule[i] - self.solar_generation[i] + self.battery_charging_rates[i]) for i in range(self.T)]

    def get_grid_load(self, creature):
        schedule = [0 for i in range(self.T)] 
        shed_loads = [self.sheddable_loads[i] if creature['shed_l_schedule'][i] == 1 else 0 for i in range(self.T)]
        shift_loads = creature['shift_l_schedule']

        battery_charging_rates = creature["battery_schedule"]
        self.add_battery_power(schedule, battery_charging_rates)

        for l in shed_loads:
            self.remove_load(schedule, l["start_time"],l["period"],l["consumption"])

        for l in shift_loads:
            self.add_load(schedule, l["start_time"],l["period"],l["consumption"])

        grid_load = [max(0, self.load_consumption[i] + schedule[i] - self.solar_generation[i]) for i in range(self.T)]
        
        return grid_load