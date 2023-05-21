import csv
def getInput(d):
    N = 24
    import csv

    sheddable_loads = []  # List to store the dictionaries

    with open('shedable_dataframe.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')  # Assuming the data is tab-separated

        for row in reader:
            sheddable_loads.append(dict(row))

    print(sheddable_loads)

    shiftable_loads = []  # List to store the dictionaries

    with open('shiftable_dataframe.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')  # Assuming the data is tab-separated

        for row in reader:
            shiftable_loads.append(dict(row))

    print(shiftable_loads)

    with open('february_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            solar_forecasting.append(float(row['Solar Forecasting']))
            actual_solar.append(float(row['Actual Solar']))
            building_forecasting.append(float(row['Building Forecasting']))
            actual_building.append(float(row['Actual Building']))

    df = pd.read_csv('tariff_data.csv', delimiter='\t')  # Assuming the data is tab-separated

    electricity_tariff = df['Rates'].tolist()

    print(electricity_tariff)

    solar_forecasting = solar_forecasting[24*d:24*(d+1)]
    actual_solar = actual_solar[24*d:24*(d+1)]
    building_forecasting = building_forecasting[24*d:24*(d+1)]
    actual_building = actual_building[24*d:24*(d+1)]

    #return N,battery_state_0,solar_generation,load_consumption,electricity_tariff,shiftable_loads,sheddable_loads
    return N,battery_state_0,solar_forecasting,building_forecasting,actual_solar,actual_building, electricity_tariff,shiftable_loads,sheddable_loads


