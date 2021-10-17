# function to calculate the yearly increment in maintenance, returns list of maintenance costs...
def MaintenanceIncrementCost(Economy_maintenance_charge,maintenance_rate):
    maintenance_cost = []
    rate = (maintenance_rate/100)
    count = 1
    for i in range(26):
        if count <= 2:
            maintenance_cost.append(Economy_maintenance_charge)
            count += 1
        else:
            maintenance_cost.append(round(maintenance_cost[-1]+(rate*maintenance_cost[-1]),2))
    return maintenance_cost