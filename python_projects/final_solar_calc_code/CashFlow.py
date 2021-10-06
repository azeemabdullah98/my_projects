# function to calculate the yearly savings and to calculate the to get the transition of value from -ve to +ve, returns list of values... 
def CashFlow(EconomyYearlyIncome,economyEMI,MaintenanceCost,downpayment):
    net_cash_flow = []
    cum_cash_flow = []
    count = 1
    for income,maintCost in zip(EconomyYearlyIncome,MaintenanceCost):
        if count == 1:
            downpayment = -downpayment
            net_cash_flow.append(downpayment)
            cum_cash_flow.append(downpayment)
            count += 1
        else:
            net_cash = income-maintCost-economyEMI
            net_cash_flow.append(net_cash)
            cum_cash = cum_cash_flow[-1]+net_cash_flow[-1]
            cum_cash_flow.append(cum_cash)
    return net_cash_flow,cum_cash_flow