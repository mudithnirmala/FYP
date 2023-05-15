class LoadManager:
    def __init__(self, T, sheddable_loads, shiftable_loads, load_consumption, solar_generation):
        self.T = T
        self.sheddable_loads = sheddable_loads
        self.shiftable_loads = shiftable_loads
        self.load_consumption = load_consumption
        self.solar_generation = solar_generation
        self.schedule = [0 for _ in range(T)]
        self.battery_charging_rates = [0 for _ in range(T)]

    def add_load(self, start_time, period, consumption):
        for i in range(start_time, start_time + period):
            self.schedule[i % self.T] += consumption

    def remove_load(self, start_time, period, consumption):
        for i in range(start_time, start_time + period):
            self.schedule[i % self.T] -= consumption

    def add_generation(self, start_time, period, generation):
        for i in range(start_time, start_time + period):
            self.schedule[i % self.T] += generation

    def add_battery_power(self, battery_charging_rates):
        for i in range(self.T):
            self.battery_charging_rates[i] += battery_charging_rates[i]
    

    def get_shifted_load():
        return

    

    def get_grid_load(self,creature):
        return [max(0, self.load_consumption[i] - self.schedule[i] - self.solar_generation[i] + self.battery_charging_rates[i]) for i in range(self.T)]

    def get_grid_load(self, creature):
        shed_load = [self.sheddable_loads[i] if creature['shed_l_schedule'][i] == 1 else 0 for i in range(self.T)]
        grid_load = [max(0, self.load_consumption[i] - self.schedule[i] - self.solar_generation[i] + self.battery_charging_rates[i] - shed_load[i]) for i in range(self.T)]
        return grid_load