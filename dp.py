from battery import battery_degradation_cost

def get_fitness(calculator,creature):
    
    operating_cost = calculator.get_total_cost(creature)
    bd_cost = battery_degradation_cost(creature['battery_schedule'])
    
    return operating_cost+ bd_cost

def find_optimal_battery_dispatch(T, calculator):
    soc_levels = 20
    charging_levels = 10  # Default value for charging levels
    battery_capacity = 100  # Replace with the actual battery capacity

    # Initialize the DP table
    dp = [[float('inf')] * (soc_levels + 1) for _ in range(T + 1)]
    dp[0][charging_levels] = 0  # Base case: starting with fully charged battery

    # Initialize the battery dispatch schedule table
    dispatch_schedule = [[[0] *T for j in range(soc_levels + 1)] for _ in range(T + 1)]

    # Iterate over time steps
    for t in range(T):
        # Iterate over possible state of charges
        for soc_level in range(soc_levels + 1):
            # Iterate over possible charging levels
            for c_level in range(-charging_levels, charging_levels + 1):
                if(-1*c_level>soc_level): continue
                new_soc = soc_level - c_level
                new_soc = max(0, min(new_soc, soc_levels))
                print(dispatch_schedule[t - 1][new_soc])

                creature = {
                    'battery_schedule': dispatch_schedule[t - 1][new_soc],
                    'shed_l_schedule': [],  # Replace with your actual shed load schedule
                    'shift_l_schedule': [],  # Replace with your actual shift load schedule
                }
                creature['battery_schedule'][t] = c_level
                cost = get_fitness(calculator,creature)

                if cost < dp[t][soc_level]:
                    dp[t][soc_level] = cost
                    dispatch_schedule[t][soc_level] = c_level

    return dispatch_schedule
