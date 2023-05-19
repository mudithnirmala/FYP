import csv
def getInput(d):


    with open('input.txt','r') as file:
        N = int(file.readline().strip())
        battery_state_0 = int(file.readline().strip())
        solar_generation = list(map(int,file.readline().strip().split()))
        load_consumption = list(map(int,file.readline().strip().split()))
        electricity_tariff = list(map(int,file.readline().strip().split()))

        shiftable_loads=[]
        sheddable_loads=[]

        M1 = int(file.readline().strip())
        for i in range(M1):
            load_data = {}

            start, end, duration, consumption = map(int, file.readline().strip().split())
            load_data['start'] = start
            load_data['end'] = end
            load_data['duration'] = duration
            load_data['consumption'] = consumption

            shiftable_loads.append(load_data)

        M2 = int(file.readline().strip())
        for i in range(M2):
            load_data = {}

            start, end, consumption, penalty = map(int, file.readline().strip().split())
            load_data['start'] = start
            load_data['end'] = end
            load_data['consumption'] = consumption
            load_data['penalty'] = penalty

            sheddable_loads.append(load_data)

    solar_forecasting = []
    actual_solar = []
    building_forecasting = []
    actual_building = []

    with open('february_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            solar_forecasting.append(float(row['Solar Forecasting']))
            actual_solar.append(float(row['Actual Solar']))
            building_forecasting.append(float(row['Building Forecasting']))
            actual_building.append(float(row['Actual Building']))

    solar_forecasting = solar_forecasting[24*d:24*(d+1)]
    actual_solar = actual_solar[24*d:24*(d+1)]
    building_forecasting = building_forecasting[24*d:24*(d+1)]
    actual_building = actual_building[24*d:24*(d+1)]

    #return N,battery_state_0,solar_generation,load_consumption,electricity_tariff,shiftable_loads,sheddable_loads
    return N,battery_state_0,solar_forecasting,building_forecasting,actual_solar,actual_building, electricity_tariff,shiftable_loads,sheddable_loads


