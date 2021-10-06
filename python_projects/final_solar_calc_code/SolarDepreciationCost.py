# function to calculate the yearly depreciation of solar power generation, returns list of depreciated values...
def SolarDepreciationCost(Economy_power_gen,cuf_factor,grid_tariff):
    solarDepreciation = []
    yearlyIncome = []
    cuf = 1-(cuf_factor/100)
    count = 1
    for i in range(26):
        if count <= 2:
            solarDepreciation.append(Economy_power_gen)
            yearlyIncome.append(solarDepreciation[0]*grid_tariff)
            count += 1
        else:
            solarDepreciation.append(round(solarDepreciation[-1]*cuf,2))
            yearlyIncome.append(round(solarDepreciation[-1]*grid_tariff,2))
    return solarDepreciation,yearlyIncome