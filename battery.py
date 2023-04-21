import math
T = 24

def calculate_soc_level(soc_0,c_rates):
    global T
    soc_levels = []
    soc_levels.append(soc_0+c_rates[0]*5)
    for i in range (T):
        state = soc_levels[-1]+c_rates[i]*5
        if state < 0:
            state = 0
        if state > 100:
            state = 100
        soc_levels.append(state)
        
    return soc_levels


def calculate_cyclelife(dod,c_rate): # Latter consider charging rate.
    alpha = -27918 #-20567.24 #103567.84767 # we have to calculate these values according to our case
   # alpha = -103567.84767
    beta = 6000 #
    beta = 133402 #
    #beta = 1191.54
    if dod <= 0:
        dod = 1
    return alpha * math.log(dod) + beta

def battery_degradation_cost(soc_levels):

    capital_cost = 74621471.24/330
    #capital_cost = 226812.98

    bd_cost =0 #battery degradation cost
    global T
    for i in range(T-1):
        c_rate = abs(soc_levels[i+1]-soc_levels[i])
        bd_cost+=(1/2)*capital_cost*abs(1/calculate_cyclelife(soc_levels[i],c_rate)-1/calculate_cyclelife(soc_levels[i+1],c_rate))

    return bd_cost

#soc_levels = [40, 42, 45, 48, 40, 34, 30, 25, 15, 20, 40, 50, 60, 55, 60, 65, 60, 55, 60, 65, 70, 75, 80, 85]
soc_levels = [40, 45, 50, 60, 55, 60, 65, 70, 65, 50, 30, 25, 25, 25, 30, 35, 40, 45, 60, 65, 70, 75, 80, 85]
soc_levels = [20,30,40,50,60,70,80,70,60,50,40,35,30,25,20,20,20,20,20,20,20,20,20,20]
#soc_levels = [20,80,20,80,20,80,20,80,20,80,20,80,20,80,20,80,20,80,20,80,20,80,20,80]
soc_levels = [40,30,40,30,40,30,40,30,40,30,40,30,40,30,40,30,40,30,40,30,40,30,40,40]
c_rates = [-3,-2,0,3, 1 ,3 ,-3,-2,0,3, 1 ,3 ,1 ,3 ,-3,-2,0,3,0,3, 1 ,3 ,1 ,3]
soc_0 = 20
#print (calculate_cyclelife(100,1))
#print (battery_degradation_cost(soc_levels))

#print(calculate_soc_level(soc_0,c_rates))