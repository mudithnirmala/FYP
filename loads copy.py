# schedule = [3 2 5 24 7 8 2 10 5 6] M1 values

T = 24 

sheddable_loads = []
shiftable_loads = []
load_consumption = []

def calculate_shiftable_load_consumption(shiftable_load_starttime):
    global N
    M1 = len(shiftable_loads)
    # in the schedule, the time the load start is given
    penalty = 0
    shiftable_load_consumption = [0]*T
    for i in range(M1):
        if shiftable_loads[i]['start'] > shiftable_load_starttime[i] or shiftable_load_starttime[i] + shiftable_loads[i]['duration'] > shiftable_loads[i]['end']:
            penalty = 25000
        for j in range(shiftable_loads[i]['duration']):
            shiftable_load_consumption[(shiftable_load_starttime[i]+j)%24] += shiftable_loads[i]['consumption']
    return penalty, shiftable_load_consumption
### No loads passing 24 hour

def calculate_shedding_results(shedded_loads):#boolean array
    global T,sheddable_loads,shiftable_loads
    shedded_loads = [i for i, x in enumerate(shedded_loads) if x] # index array
    total_penalty = 0
    sheddable_load_consumption_reducton =[0]*T

    for l in range(len(sheddable_loads)):
        total_penalty+=sheddable_loads[l]['penalty']
        #print (len(sheddable_loads),len(shedded_loads))
        for j in range(shedded_loads[l]['duration']):
             sheddable_load_consumption_reducton[(sheddable_loads[l]['start']+j)%24] += sheddable_loads[l]['consumption']
    return total_penalty,sheddable_load_consumption_reducton

def calculate_total_load(shift_l,shed_l):
    global T,sheddable_loads,shiftable_loads
    global load_consumption
    total_load = [0]*T
    for i in range(N):
        total_load[i] = load_consumption[i]+shift_l[i]-shed_l[i]
        
    return total_load

def setFlexibleLoads(shed_loads,shift_loads,loads,t):
    global sheddable_loads,shiftable_loads,load_consumption
    sheddable_loads = shed_loads
    shiftable_loads = shift_loads
    load_consumption = loads
    T=t