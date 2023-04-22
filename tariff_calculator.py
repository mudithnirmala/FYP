BATTERY_CAPACITY = 400000
def calculate_bill(load_consumption, solar_generation, c_rates):
    global BATTERY_CAPACITY
    rates = [39, 39, 39, 39, 39, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 55, 55, 55, 55, 39, 39, 39]
    #rates = [0.09656, 0.09735, 0.09536, 0.09415, 0.09679, 0.12579, 0.16202, 0.20157, 0.13004, 0.09948, 0.10538, 0.08557, 0.08311, 0.08446, 0.09026, 0.08750, 0.09040, 0.12684, 0.25969, 0.13004, 0.13004, 0.12770, 0.11762, 0.12463]
    grid_sell_back_rate = 37
    bill=0
    #print('c',c_rates)
    #print(len(load_consumption))
    for i in range(len(load_consumption)):
        # Calculate net power consumption or generation
        net_load = load_consumption[i] +(0.05*BATTERY_CAPACITY)*c_rates[i] - solar_generation[i] 
        
        # Determine time of day and apply appropriate rate
        rate = rates[i]

        if(net_load<0): rate = 0 # not in australia
        bill+=rate*net_load/1000

        #print (i,rate,net_load,rate*net_load/1000,bill)
    return bill


load_consumption = [100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 1100,
                    1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 1800, 1600]

solar_generation = [0, 0, 0, 0, 0, 0, 0, 100, 200, 300, 400, 500, 600,
                    700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1200, 900]

battery_charging_rates = [0, 0, 0, 0, 0, 0, 5, 15, 35, 50, 60, 70, 80, 85, 90, 95, 98, -100, -100, -100, 80, -50, -20, -10]

battery_charging_rates = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#bill = calculate_bill(load_consumption, solar_generation, battery_charging_rates)

# print('Electricity bill for the day: Rs. {:.2f}'.format(bill))