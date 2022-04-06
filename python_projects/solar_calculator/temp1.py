import pandas as pd
import re
import numpy as np
import json
import boto3
from io import StringIO

client = boto3.client('s3',
    aws_access_key_id='AKIAS6HQEKBHT52I2SGT',
    aws_secret_access_key='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',
)

bucket_name = 'solar-calc-bucket'

object_key1 = 'final_data.csv'
object_key2 = 'SKU - Sheet1.csv'
csv_obj1 = client.get_object(Bucket=bucket_name, Key=object_key1)
csv_obj2 = client.get_object(Bucket=bucket_name,Key=object_key2)
body1 = csv_obj1['Body']
body2 = csv_obj2['Body']
csv_string1 = body1.read().decode('utf-8')
csv_string2 = body2.read().decode('utf-8')

df = pd.read_csv(StringIO(csv_string1))
# df = pd.read_csv("c:/python_projects/solar_calculator/final_data.csv")
df1 = pd.read_csv(StringIO(csv_string2))
# df1 = pd.read_csv("c:/python_projects/solar_calculator/SKU - Sheet1.csv")

def ConditionalFunc(CondValue,new_df):
    try:
        lowerValue = [lv for lv in new_df['LowerValue'] if pd.notna(lv) == True] # lower range...
        upperValue = [uv for uv in new_df['UpperValue'] if pd.notna(uv) == True] # upper range...
        for low,up in zip(lowerValue,upperValue):
            if (CondValue > low and CondValue <= up) or (low==up and CondValue > up):
                lv = new_df[(new_df['LowerValue'] == low)]
                lineText = lv.at[lv.index[0],'Cond Value']
                print(lineText) 
            elif CondValue < lowerValue[0]:
                print("Value not available in the table. Please provide a different value")
                break
        monthly_billing = eval(lineText)
        return monthly_billing
    except Exception as e:
        monthly_billing = CondValue
        return monthly_billing

# to check if sanction load is present for the discom provided and return none if no sanction load is present...
def CheckSanctionLoad(new_df,SanctionLoad):
#     try:
    regex = re.compile(r'SanctionLoad.*')
    sLoad = regex.findall(new_df['Line Text'].to_string())
    if len(sLoad) == 1:
        sl_formula = new_df[(new_df['Line Text'] == sLoad[0])]
        sl_formula = sl_formula.at[sl_formula.index[0],'Cond Value']
    elif len(sLoad) == 2:
        if SanctionLoad <=5 or SanctionLoad <= 10 or SanctionLoad <=20:
            sl_formula = new_df[(new_df['Line Text'] == sLoad[0])]
            sl_formula = sl_formula.at[sl_formula.index[0],'Cond Value']
        elif SanctionLoad > 5 or SanctionLoad >10 or SanctionLoad >20:
            sl_formula = new_df[(new_df['Line Text'] == sLoad[1])]
            sl_formula = sl_formula.at[sl_formula.index[0],'Cond Value']
    elif len(sLoad) == 3:
        if SanctionLoad <= 20:
            sl_formula = new_df[(new_df['Line Text'] == sLoad[0])]
            sl_formula = sl_formula.at[sl_formula.index[0],'Cond Value']
        elif SanctionLoad > 20 and SanctionLoad <= 50:
            sl_formula = new_df[(new_df['Line Text'] == sLoad[1])]
            sl_formula = sl_formula.at[sl_formula.index[0],'Cond Value']
        elif SanctionLoad > 50:
            sl_formula = new_df[(new_df['Line Text'] == sLoad[2])]
            sl_formula = sl_formula.at[sl_formula.index[0],'Cond Value']
            
    else:
        sl_formula = None
    return sl_formula


# to check if tax is available for the particular discom else return none...
def CheckTax(new_df):
    
    tax = list(new_df[(new_df['Line Text'] == 'Tax')]['Cond Value'].values)
    
    if len(tax) == 0:
        tax = None
    else:
        tax = float(tax[0])
    return tax    
    
      

# function for Economy recommendation (Smart and Pro), returns DC unit, cost for low and high structure height 
# (for both Smart and Pro option )...
def SmartRecommendation(df1,rooftopArea,struct_height,energyReq):
        # for 'Smart' option (for high and low values)...
    dc_capacity = df1[(df1['Option'] == 'Smart') & (df1['Structure Height'] == struct_height)]['DC Capacity (kWp)']
    dc_capacity = dc_capacity.tolist()
    min_rooftoparea = dc_capacity[0]*100
    if rooftopArea >= min_rooftoparea and energyReq >= min_rooftoparea/100 :
        smart_unit = []
        for i in range(len(dc_capacity)):
            if rooftopArea/100 <= dc_capacity[-1] and energyReq <= dc_capacity[-1]:
                if (energyReq > dc_capacity[i] and energyReq < dc_capacity[i+1]) or (rooftopArea/100 > dc_capacity[i] and rooftopArea/100 < dc_capacity[i+1]):
                    final_units = dc_capacity[i]
                    smart_unit.append(final_units)
                elif energyReq == dc_capacity[i] or ((rooftopArea/100) == dc_capacity[i]):
                    final_units = dc_capacity[i]
                    smart_unit.append(final_units) 
            elif rooftopArea/100 > dc_capacity[-1] and energyReq <= dc_capacity[-1]:
                if (energyReq > dc_capacity[i] and energyReq < dc_capacity[i+1]) and (rooftopArea/100 > dc_capacity[i] or rooftopArea/100 < dc_capacity[i+1]):
                    final_units = dc_capacity[i]
                    smart_unit.append(final_units)
                elif energyReq == dc_capacity[i] or ((rooftopArea/100) == dc_capacity[i]):
                    final_units = dc_capacity[i]
                    smart_unit.append(final_units) 
            elif rooftopArea/100 <= dc_capacity[-1] and energyReq > dc_capacity[-1]:
                if (rooftopArea/100 > dc_capacity[i] and rooftopArea/100 < dc_capacity[i+1]):
                    final_units = dc_capacity[i]
                    smart_unit.append(final_units)
                elif rooftopArea/100 == dc_capacity[i]:
                    final_units = dc_capacity[i]
                    smart_unit.append(final_units)
        else:
            final_units = dc_capacity[-1]
            smart_unit.append(final_units)
                
        print("Recommended unit (Smart option) for the given input (based on rooftop area given) is ",smart_unit[0])
        value = df1[(df1['Option'] == 'Smart') & (df1['Structure Height'] == struct_height) & (df1['DC Capacity (kWp)'] == smart_unit[0])].loc[:,['Internal SKU','AC Capacity (kW)','Sale Price(With GST)']].values.tolist()
        return value[0][0],value[0][1],smart_unit[0],value[0][2]
    else:
        print("Minimun rooftop area should be ",min_rooftoparea," and Minimum Energy requirement is ",min_rooftoparea/100)
        return None,None,0,0




def ProRecommendation(df1,rooftopArea,struct_height,energyReq):
     # for 'Pro' option (for high and low values)...
    dc_capacity1 = df1[(df1['Option'] == 'Pro') & (df1['Structure Height'] == struct_height)]['DC Capacity (kWp)']
    dc_capacity1 = dc_capacity1.tolist()
    min_rooftoparea1 = dc_capacity1[0]*80
    if rooftopArea >= min_rooftoparea1 and energyReq >= min_rooftoparea1/80:
        pro_unit = []
        for i in range(len(dc_capacity1)):
            if rooftopArea/80 <= dc_capacity1[-1] and energyReq <= dc_capacity1[-1]:
                if (energyReq > dc_capacity1[i] and energyReq < dc_capacity1[i+1]) or (rooftopArea/80 > dc_capacity1[i] and rooftopArea/80 < dc_capacity1[i+1]):
                    final_units = dc_capacity1[i]
                    pro_unit.append(final_units)
                elif energyReq == dc_capacity1[i] or ((rooftopArea/80) == dc_capacity1[i]):
                    final_units = dc_capacity1[i]
                    pro_unit.append(final_units) 
            elif rooftopArea/80 > dc_capacity1[-1] and energyReq <= dc_capacity1[-1]:
                if (energyReq > dc_capacity1[i] and energyReq < dc_capacity1[i+1]) and (rooftopArea/80 > dc_capacity1[i] or rooftopArea/80 < dc_capacity1[i+1]):
                    final_units = dc_capacity1[i]
                    pro_unit.append(final_units)
                elif energyReq == dc_capacity1[i] or ((rooftopArea/80) == dc_capacity1[i]):
                    final_units = dc_capacity1[i]
                    pro_unit.append(final_units)
            elif rooftopArea/80 <= dc_capacity1[-1] and energyReq > dc_capacity1[-1]:
                if (rooftopArea/80 > dc_capacity1[i] and rooftopArea/80 < dc_capacity1[i+1]):
                    final_units = dc_capacity1[i]
                    pro_unit.append(final_units)
                elif rooftopArea/80 == dc_capacity1[i]:
                    final_units = dc_capacity1[i]
                    pro_unit.append(final_units)
        else:
            final_units = dc_capacity1[-1]
            pro_unit.append(final_units)
                    
        print("Recommended unit (Pro option) for the given input (based on rooftop area given) is ",pro_unit[0])
        value = df1[(df1['Option'] == 'Pro') & (df1['Structure Height'] == struct_height) & (df1['DC Capacity (kWp)'] == pro_unit[0])].loc[:,['Internal SKU','AC Capacity (kW)','Sale Price(With GST)']].values.tolist()
        return value[0][0],value[0][1],pro_unit[0],value[0][2]
    else:
        print("Minimun rooftop area should be ",min_rooftoparea1," and Minimum Energy requirement is ",min_rooftoparea1/80)
        return None,None,0,0



# function for Premium Recommendation (Secure)
def PremiumRecommendation(df1,rooftopArea,struct_height,energyReq,battery_capacity):
    battery_value = list(df1[(df1['Option'] == 'Secure') & (df1['Structure Height'] == struct_height)]['Battery Backup'].unique())
    if battery_capacity not in battery_value:
        battery_capacity = battery_value[-1]
    dc_capacity = df1[(df1['Option'] == 'Secure') & (df1['Battery Backup'] == battery_capacity) & (df1['Structure Height'] == struct_height)]['DC Capacity (kWp)']
    dc_capacity = dc_capacity.tolist()
    min_rooftoparea = dc_capacity[0]*100
    if rooftopArea >= min_rooftoparea and energyReq >= min_rooftoparea/100:
        secure_unit = []
        for i in range(len(dc_capacity)):
            if rooftopArea/100 <= dc_capacity[-1] and energyReq <= dc_capacity[-1]:
                if (energyReq > dc_capacity[i] and energyReq < dc_capacity[i+1]) or (rooftopArea/100 > dc_capacity[i] and rooftopArea/100 < dc_capacity[i+1]):
                    final_units = dc_capacity[i]
                    secure_unit.append(final_units)
                elif energyReq == dc_capacity[i] or ((rooftopArea/100) == dc_capacity[i]):
                    final_units = dc_capacity[i]
                    secure_unit.append(final_units) 
            elif rooftopArea/100 > dc_capacity[-1] and energyReq <= dc_capacity[-1]:
                if (energyReq > dc_capacity[i] and energyReq < dc_capacity[i+1]) and (rooftopArea/100 > dc_capacity[i] or rooftopArea/100 < dc_capacity[i+1]):
                    final_units = dc_capacity[i]
                    secure_unit.append(final_units)
                elif energyReq == dc_capacity[i] or ((rooftopArea/100) == dc_capacity[i]):
                    final_units = dc_capacity[i]
                    secure_unit.append(final_units)
            elif rooftopArea/100 <= dc_capacity[-1] and energyReq > dc_capacity[-1]:
                if (rooftopArea/100 > dc_capacity[i] and rooftopArea/100 < dc_capacity[i+1]):
                    final_units = dc_capacity[i]
                    secure_unit.append(final_units)
                elif rooftopArea/100 == dc_capacity[i]:
                    final_units = dc_capacity[i]
                    secure_unit.append(final_units)
        else:
            final_units = dc_capacity[-1]
            secure_unit.append(final_units)
                    
        print("For a Given battery backup ",battery_capacity)
        print("Recommended unit (Secure option) for the given input (based on rooftop area given) is ",secure_unit[0])
        value = df1[(df1['Option'] == 'Secure') & (df1['Battery Backup'] == battery_capacity) & (df1['Structure Height'] == struct_height) & (df1['DC Capacity (kWp)'] == secure_unit[0])].loc[:,['Internal SKU','AC Capacity (kW)','Sale Price(With GST)']].values.tolist()
        return value[0][0],value[0][1],secure_unit[0],value[0][2]
    else:
        return None,None,0,0

# function to calculate yearly EMI for both Economy and Secure...
def EMI(P1,P2,R,N,downpaymentFrac):
    EMI_formula = df[(df['Line Text'] == 'EMI')]['Cond Value'].values[0]
    numerator, denominator = EMI_formula.split("/")
    R = (R)/(12*100)
    N = N*12
    temp = [P1*downpaymentFrac,P2*downpaymentFrac]
    # for 'Economy option...
    P = P1-temp[0]
    EconomyEMI = (eval(numerator)/eval(denominator))*12
    print(EconomyEMI)
    # for 'secure' option...
    P = P2-temp[1]
    secureEMI = (eval(numerator)/eval(denominator))*12
    print(secureEMI)
    return EconomyEMI,secureEMI

# function to calculate the yearly increment in maintenance, returns list of maintenance costs...
def MaintenanceIncrementCost(choice,maintenance_charge,maintenance_rate):
    maintenance_cost = []
    rate = (maintenance_rate/100)
    count = 1
    if choice == 'residential':
        for i in range(26):
            if count <= 2:
                maintenance_cost.append(maintenance_charge)
                count += 1
            else:
                maintenance_cost.append(round(maintenance_cost[-1]+(rate*maintenance_cost[-1]),2))
    elif choice == 'commercial':
        for i in range(26):
            if count == 1:
                maintenance_cost.append(maintenance_charge)
                count += 1
            else:
                maintenance_cost.append(maintenance_cost[-1]*(1+rate))
    return maintenance_cost

# function to calculate the yearly depreciation of solar power generation, returns list of depreciated values...
def SolarDepreciationCost(power_gen,cuf_factor,grid_tariff,tariff_escalation):
    solarDepreciation = []
    yearlyIncome = []
    gridTariffList = []
    cuf = 1-(cuf_factor/100)
    
    count = 1
    for i in range(26):
        if count <= 2:
            solarDepreciation.append(power_gen)
            gridTariffList.append(grid_tariff)
            yearlyIncome.append(solarDepreciation[0]*gridTariffList[0])
            count += 1
        else:
            solarDepreciation.append(round(solarDepreciation[-1]*cuf,2))
            gridTariffList.append(round(gridTariffList[-1]*(1+(tariff_escalation/100)),2))
            yearlyIncome.append(round(solarDepreciation[-1]*gridTariffList[-1],2))
    return solarDepreciation,yearlyIncome

# for commercial...
def DepreciationCost(Cost,depPer1,depPer2,TaxBenfit):
    dep_cost = []
    incomeTaxBenefit = []
    for i in range(27):
        if i == 0:
            dep = Cost*(float(depPer1)/100)
            dep_cost.append(dep)
            taxBenefit = dep_cost[0]*(TaxBenfit/100)
            incomeTaxBenefit.append(taxBenefit)
        elif i > 1:
            cost = Cost-sum(dep_cost)
            dep = cost*(float(depPer2)/100)
            dep_cost.append(dep)
            taxBenefit = dep_cost[-1]*(TaxBenfit/100)
            incomeTaxBenefit.append(taxBenefit)
    return dep_cost,incomeTaxBenefit

def ElectricityBill(input_bill,inflationTariff,SavingEff):
    monthly_bill = []
    yearly_bill = []
    count = 0
    if SavingEff != None:
        for sf in SavingEff:
            if count == 0:
                bill = input_bill*(1-(sf/100))
                monthly_bill.append(bill)
                yearly_bill.append(bill*12)
                count += 1
            else:
                bill = input_bill*(1+(inflationTariff/100))**count*(1-(sf/100))
                monthly_bill.append(bill)
                yearly_bill.append(bill*12)
                count += 1
    else:
        for i in range(26):
            if count == 0:
                bill = input_bill
                monthly_bill.append(bill)
                yearly_bill.append(bill*12)
                count += 1
            else:
                bill = input_bill*(1+(inflationTariff/100))**count
                monthly_bill.append(bill)
                yearly_bill.append(bill*12)
                count += 1
            
    return monthly_bill,yearly_bill


# for commercial...
def SavingEfficiency(savingEfficiency,inflationTariff):
    temp = []
    count = 1
    for i in range(26):
        if count == 1:
            temp.append(savingEfficiency)
            count += 1
        else:
            sf = (temp[-1]/100)*(1-(inflationTariff/100))
            temp.append(sf*100)
    return temp

# function to calculate the yearly savings and to calculate the to get the transition of value from -ve to +ve, returns list of values... 
def CashFlow(EconomyYearlyIncome,EMI,MaintenanceCost,downpayment,N):
    net_cash_flow = []
    cum_cash_flow = []
    count = 0
    for income,maintCost in zip(EconomyYearlyIncome,MaintenanceCost):
        if count == 0:
            downpayment = -downpayment
            net_cash_flow.append(downpayment)
            cum_cash_flow.append(downpayment)
            count += 1
        elif count > 0 and EMI != 0:
            if count <= N:
                net_cash = income-maintCost-EMI
                count += 1
            else:
                net_cash = income-maintCost
                
            net_cash_flow.append(net_cash)
            cum_cash = cum_cash_flow[-1]+net_cash_flow[-1]
            cum_cash_flow.append(cum_cash)
        elif count > 0 and EMI == 0:
            net_cash = income-maintCost
            net_cash_flow.append(net_cash)
            cum_cash = cum_cash_flow[-1]+net_cash_flow[-1]
            cum_cash_flow.append(cum_cash)
    return net_cash_flow,cum_cash_flow

def TotalExpense(bill_yearly,maintenanceCost,debtInterest,TaxBenefit,incomeTaxOnDep,Downpayment,EMI,Tenure):
    if debtInterest != 0 and EMI != 0 and maintenanceCost != 0:
        totalExpense1 = [bill_yearly[i]+maintenanceCost[i]+debtInterest[i] for i in range(len(debtInterest))]
        totalExpense2 = [bill_yearly[i]+maintenanceCost[i] for i in range(int(Tenure),len(bill_yearly))]
        totalExpense = totalExpense1+totalExpense2
        taxBenefitOnExpense = [i*(TaxBenefit/100) for i in totalExpense]
        totalIncomeTax = [i+j for i,j in zip(incomeTaxOnDep,taxBenefitOnExpense)]
        net_flow1 = [(Downpayment+EMI+totalExpense[i])-(debtInterest[i]+totalIncomeTax[i]) for i in range(1)]
        net_flow2 = [(EMI+totalExpense[i])-(debtInterest[i]+totalIncomeTax[i]) for i in range(1,len(debtInterest))]
        net_flow3 = [(totalExpense[i])-(totalIncomeTax[i]) for i in range(len(debtInterest),len(bill_yearly))]
        net_flow = net_flow1+net_flow2+net_flow3
    elif debtInterest == 0 and EMI == 0 and maintenanceCost != 0:
        totalExpense = [bill_yearly[i]+maintenanceCost[i] for i in range(len(bill_yearly))]
        taxBenefitOnExpense = [i*(TaxBenefit/100) for i in totalExpense]
        totalIncomeTax = [i+j for i,j in zip(incomeTaxOnDep,taxBenefitOnExpense)]
        net_flow1 = [(Downpayment+totalExpense[i])-(totalIncomeTax[i]) for i in range(1)]
        net_flow2 = [(totalExpense[i])-(totalIncomeTax[i]) for i in range(1,len(bill_yearly))]
        net_flow = net_flow1+net_flow2
    else:
        totalExpense = [i for i in bill_yearly]
        taxBenefitOnExpense = [i*(TaxBenefit/100) for i in totalExpense]
        totalIncomeTax = [i for i in taxBenefitOnExpense]
        net_flow = [i-j for i,j in zip(totalExpense,totalIncomeTax)]
    
    return totalExpense,taxBenefitOnExpense,totalIncomeTax,net_flow


# function to calculate interest for debt (commercial)...
def InterestOnDebt(Economy_cost,ROI,economyEMI,LeverageRatio):
    debtInterest = []
    closingBalance = []
    count = 1
    for i in range(26):
        if count == 1:
            LoanAmount = Economy_cost*(LeverageRatio/100)
            Interest = LoanAmount*(ROI/100)
            Principle = economyEMI - Interest 
            closingBal = LoanAmount - Principle
            debtInterest.append(Interest)
            closingBalance.append(closingBal)
            count += 1
        else:
            LoanAmount = closingBalance[-1]
            Interest = LoanAmount*(ROI/100)
            Principle = economyEMI - Interest
            closingBal = LoanAmount - Principle
            debtInterest.append(Interest)
            closingBalance.append(closingBal)
    return [i for i in debtInterest if i > 1]

# without solar, without loan...
def NormalBill(input_bill,inflationTariff,TaxBenefit,cuf_factor):
    savings = []
    bill_monthly, bill_yearly = ElectricityBill(input_bill,inflationTariff,SavingEff = None)
    EconomyMaintenanceCost = 0
    interest_on_debt = 0
    incomeTaxOnDep = 0
    EconomyDownpayment = 0
    economyEMI = 0
    Tenure = 0
    totalExpense,TaxBenefitOnExpense,TotalTaxBenefit,NetFlow = TotalExpense(bill_yearly,EconomyMaintenanceCost,interest_on_debt,TaxBenefit,incomeTaxOnDep,EconomyDownpayment,economyEMI,Tenure)
    
    return NetFlow

def CumSavings(pv_savings):
    cum_savings=[]
    count = 0
    for i in pv_savings:
        if count == 0:
            cum_savings.append(i)
            count += 1
        else:
            cum_savings.append(cum_savings[-1]+i)
    return cum_savings

# main function...
def TotalBill(df,choice,state,discom,district,input_bill,SanctionLoad,rooftopArea,struct_height,battery_backup,battery_capacity,loan):
    print("passing...")
    
    battery_capacity = float(battery_capacity)
    
    input_bill = float(input_bill)
    
    rooftopArea = float(rooftopArea)
    
    SanctionLoad = float(SanctionLoad)
    
    state_list = df['Main Cond ID'].unique().tolist()
    discom_list = df['Sub Cond ID'].unique().tolist()
    if state in state_list and discom in discom_list:
        
        print("for {} type ".format(choice))
        if state == 'Gujarat' and discom == 'Gujarat Torrent Power':
            new_df = df[(df['Cond Type'] == choice) & (df['Main Cond ID'] == state) & (df['Sub Cond ID'] == discom) & (df['Sub Cond ID2'] == district)]
        else:
            new_df = df[(df['Cond Type'] == choice) & (df['Main Cond ID'] == state) & (df['Sub Cond ID'] == discom)] 
     
        fc_charge = new_df[(new_df['Line Text'] == 'defaultFixedCharge')]
        fc_charge = float(fc_charge.at[fc_charge.index[0],'Cond Value'])
        irradiance = new_df[(new_df['Line Text'] == 'Irradiance')]
        Irradiance = float(irradiance.at[irradiance.index[0],'Cond Value'])
        CondValue = input_bill - fc_charge
        print(CondValue)
        tax = CheckTax(new_df) # function to check if tax available for the particular discom or not...
        sl_formula = CheckSanctionLoad(new_df,SanctionLoad) # function to check if sanctionload is given for a particular discom or not...
        
        if tax != None:
            CondValue = CondValue-(float(tax)*CondValue)
            print(CondValue)
            
        if sl_formula != None:
            CondValue = abs(eval(sl_formula))
            
        print(CondValue)
        monthly_billing = ConditionalFunc(CondValue,new_df)
        yearly_billing = monthly_billing*12
        energy_requirement = round(float(yearly_billing)/Irradiance,2)
        grid_tariff = round((input_bill/monthly_billing),2)
        print("monthly billing is ",monthly_billing)
        print("yearly billing is ",yearly_billing)
        print("Energy Requirement (yearly billing/irradiance) is ",energy_requirement)
        print("Grid Tariff is ",grid_tariff)
        smart_internal_SKU,smart_AC_cap,smart_unit,smart_cost = SmartRecommendation(df1,rooftopArea,struct_height,energy_requirement)
        pro_internal_SKU,pro_AC_cap,pro_unit,pro_cost = ProRecommendation(df1,rooftopArea,struct_height,energy_requirement)
        secure_internal_SKU,secure_AC_cap,secure_unit,secure_cost = PremiumRecommendation(df1,rooftopArea,struct_height,energy_requirement,battery_capacity)
        
        num_trees_saved_per_kWp = float(df[(df['Line Text'] == 'TreesSaved')]['Cond Value'].values[0])
        num_trees_saved = round((num_trees_saved_per_kWp*25)/30,2)
        CO2 = float(df[(df['Line Text'] == 'CO2')]['Cond Value'].values[0])
        
        if abs(rooftopArea-(smart_unit*100)) < abs(rooftopArea-(pro_unit*80)):
            
            Economy_unit = smart_unit
            Economy_cost = smart_cost
            Economy_SKU = smart_internal_SKU
            Economy_AC_cap = smart_AC_cap     
        else:
            
            Economy_unit = pro_unit
            Economy_cost = pro_cost
            Economy_SKU = pro_internal_SKU
            Economy_AC_cap = pro_AC_cap
            
        print(Economy_cost)
        print(Economy_unit)
        Economy_power_gen = float(Economy_unit)*Irradiance 
        Secure_power_gen = float(secure_unit)*Irradiance
        cuf_factor = float(df[(df['Line Text'] == 'CUFdegradationFactor')]['Cond Value'].values[0]) # for both Residential and commercial...
        
        if choice == 'residential': 
            tariff_escalation = float(df[(df['Line Text'] == 'TariffEscalation')]['Cond Value'].values[0])
            EconomyPowerGen, EconomyYearlyIncome = SolarDepreciationCost(Economy_power_gen,cuf_factor,grid_tariff,tariff_escalation)
            SecurePowerGen, SecureYearlyIncome = SolarDepreciationCost(Secure_power_gen,cuf_factor,grid_tariff,tariff_escalation)
            maintenance_charge = float(df[(df['Line Text'] == 'defaultMaintenanceCharge(Res)')]['Cond Value'].values[0])
            maintenance_rate = float(df[(df['Line Text'] == 'MaintenanceRate(Res)')]['Cond Value'].values[0])
            Economy_maintenance_charge = maintenance_charge*Economy_unit
            secure_maintenance_charge = maintenance_charge*secure_unit
            EconomyMaintenanceCost = MaintenanceIncrementCost(choice,Economy_maintenance_charge,maintenance_rate)
            SecureMaintenanceCost = MaintenanceIncrementCost(choice,secure_maintenance_charge,maintenance_rate)
            if loan == 'yes':
                R = float(df[(df['Line Text'] == 'TermLoanInterestRate(Res)')]['Cond Value'].values[0])
                N = float(df[(df['Line Text'] == 'TermLoanTenure(Res)')]['Cond Value'].values[0])

                LeverageRatio = float(df[(df['Line Text'] == 'LeverageRatio(Res)')]['Cond Value'].values[0])
                downpaymentFrac = (100-LeverageRatio)/100
                economyEMI,secureEMI = EMI(Economy_cost,secure_cost,R,N,downpaymentFrac)
                EconomyTermLoan = (LeverageRatio/100)*Economy_cost
                SecureTermLoan = (LeverageRatio/100)*secure_cost
                EconomyDownpayment = downpaymentFrac*Economy_cost
                SecureDownpayment = downpaymentFrac*secure_cost
                
                net_economy_cash_flow,cum_economy_cash_flow = CashFlow(EconomyYearlyIncome,economyEMI,EconomyMaintenanceCost,EconomyDownpayment,N)
                net_secure_cash_flow,cum_secure_cash_flow = CashFlow(SecureYearlyIncome,secureEMI,SecureMaintenanceCost,SecureDownpayment,N)
#                 EconPaybackPeriod = [i for i in cum_economy_cash_flow if i<=0]
#                 SecPaybackPeriod = [i for i in cum_secure_cash_flow if i<=0]

#                 EconPaybackPeriod = 1+abs(-Econ_cum_savings[1]/Econ_cum_savings[0])
#                 SecPaybackPeriod = 1+abs(-Sec_cum_savings[1]/Sec_cum_savings[0])

                EconPaybackPeriod = [i for i in cum_economy_cash_flow if i <= Economy_cost]
                SecPaybackPeriod = [i for i in cum_secure_cash_flow if i <= secure_cost]
                
                if battery_backup != 'no':
                    print("for Secure option...")
                    dataframe1 = {"MonthlyUnitConsumed":str(monthly_billing),
                                  "RecommendedDCUnit":str(secure_unit),
                                  "RecommendedACUnit":str(secure_AC_cap),
                                  "EnergyRequirement":str(energy_requirement),
                                  "RecommendedSKU":secure_internal_SKU,
                                   "CapitalCost":str(secure_cost),
                                   "TermLoan":str(SecureTermLoan),
                                  "TermLoanTenure":str(N),
                                  "TermLoanInterestRate":str(R),
                                    "mnothly_EMI":secureEMI/12,
                                     "Savings_10":cum_secure_cash_flow[10],
                                     "Savings_25":cum_secure_cash_flow[25],
                                     "PayBackPeriod":len(SecPaybackPeriod)-1,
                                     "TreesSaved":np.ceil(num_trees_saved*secure_unit),
                                     "CO2":CO2*secure_unit*25}
                    print(dataframe1)
                    return dataframe1
                else:
                    print("for Economy Option...")
                    dataframe2 = {"MonthlyUnitConsumed":str(monthly_billing),
                                  "RecommendedDCUnit":str(Economy_unit),
                                  "RecommendedACUnit":str(Economy_AC_cap),
                                  "EnergyRequirement":str(energy_requirement),
                                  "RecommendedSKU": Economy_SKU,
                                   "CapitalCost":str(Economy_cost),
                                   "TermLoan":str(EconomyTermLoan),
                                  "TermLoanTenure":str(N),
                                  "TermLoanInterestRate":str(R),
                                    "monthly_EMI":economyEMI/12,
                                     "Savings_10":cum_economy_cash_flow[10],
                                     "Savings_25":cum_economy_cash_flow[25],
                                     "PayBackPeriod":len(EconPaybackPeriod)-1,
                                     "TreesSaved":np.ceil(num_trees_saved*Economy_unit),
                                     "CO2":CO2*Economy_unit*25}
                    print(dataframe2)
                    return dataframe2
                
            elif loan == 'no':
                economyEMI = 0
                secureEMI = 0
                N = 0
                EconomyDownpayment = Economy_cost
                SecureDownpayment = secure_cost
                net_economy_cash_flow,cum_economy_cash_flow = CashFlow(EconomyYearlyIncome,economyEMI,EconomyMaintenanceCost,EconomyDownpayment,N)
                net_secure_cash_flow,cum_secure_cash_flow = CashFlow(SecureYearlyIncome,secureEMI,SecureMaintenanceCost,SecureDownpayment,N)
                
#                 EconPaybackPeriod = [i for i in cum_economy_cash_flow if i<=0]
#                 SecPaybackPeriod = [i for i in cum_secure_cash_flow if i<=0]

#                 EconPaybackPeriod = 1+abs(-Econ_cum_savings[1]/Econ_cum_savings[0])
#                 SecPaybackPeriod = 1+abs(-Sec_cum_savings[1]/Sec_cum_savings[0])

                EconPaybackPeriod = [i for i in cum_economy_cash_flow if i <= Economy_cost]
                SecPaybackPeriod = [i for i in cum_secure_cash_flow if i <= secure_cost]

                if battery_backup != 'no':
                    print('for Secure option...')
                    dataframe1 = {"MonthlyUnitConsumed":str(monthly_billing),
                                  "RecommendedDCUnit":str(secure_unit),
                                  "RecommendedACUnit":str(secure_AC_cap),
                                  "EnergyRequirement":str(energy_requirement),
                                  "RecommendedSKU":secure_internal_SKU ,
                                   "CapitalCost":str(secure_cost),
                                    "Savings_10":cum_secure_cash_flow[10],
                                     "Savings_25":cum_secure_cash_flow[25],
                                     "PayBackPeriod":len(SecPaybackPeriod)-1,
                                     "TreesSaved":np.ceil(num_trees_saved*secure_unit),
                                     "CO2":CO2*secure_unit*25}
                    print(dataframe1)
                    return dataframe1
                else:
                    print("for Economy option...")
                    dataframe2 = {"MonthlyUnitConsumed":str(monthly_billing),
                                  "RecommendedDCUnit":str(Economy_unit),
                                  "RecommendedACUnit":str(Economy_AC_cap),
                                  "EnergyRequirement":str(energy_requirement),
                                  "RecommendedSKU": Economy_SKU,
                                   "CapitalCost":str(Economy_cost),
                                    "Savings_10":cum_economy_cash_flow[10],
                                     "Savings_25":cum_economy_cash_flow[25],
                                     "PayBackPeriod":len(EconPaybackPeriod)-1,
                                     "TreesSaved":np.ceil(num_trees_saved*Economy_unit),
                                     "CO2":CO2*Economy_unit*25}
                    print(dataframe2)
                    return dataframe2
                
        elif choice == 'commercial':
            EconomyMonthlySavings = df[(df['Line Text'] == 'MonthlySavings(Econ)')]['Cond Value'].values[0]
            EconomyMonthlySavings = eval(EconomyMonthlySavings)
            SecureMonthlySavings = df[(df['Line Text'] == 'MonthlySavings(Sec)')]['Cond Value'].values[0]
            SecureMonthlySavings = eval(SecureMonthlySavings)
            depPer1,depPer2 = df[(df['Line Text'] == 'DepPer1') | (df['Line Text'] == 'DepPer2')]['Cond Value'].values
            TaxBenefit = float(df[(df['Line Text'] == 'TaxBenefit')]['Cond Value'].values[0])
            EconomyDep, EconomyTaxOnDep = DepreciationCost(Economy_cost,depPer1,depPer2,TaxBenefit)
            SecureDep, SecureTaxOnDep = DepreciationCost(secure_cost,depPer1,depPer2,TaxBenefit)
            EconomySavingEfficiency = (EconomyMonthlySavings/input_bill)*100
            SecureSavingEfficiency = (SecureMonthlySavings/input_bill)*100
            inflationTariff = float(df[(df['Line Text'] == 'InflationElectricityTariff')]['Cond Value'].values[0])
            EconSavingEff = SavingEfficiency(EconomySavingEfficiency,inflationTariff)
            SecSavingEff = SavingEfficiency(SecureSavingEfficiency,inflationTariff)
            EconBillMonthly, EconBillYearly = ElectricityBill(input_bill,inflationTariff,EconSavingEff)
            SecBillMonthly, SecBillYearly = ElectricityBill(input_bill,inflationTariff,SecSavingEff)
            repair_maintenance_rate = float(df[(df['Line Text'] == 'MaintenanceRate(Com)')]['Cond Value'].values[0])
            Economy_maintenance_cost = (repair_maintenance_rate/100)*Economy_cost
            Secure_maintenance_cost = (repair_maintenance_rate/100)*secure_cost
            EconomyMaintenanceCost = MaintenanceIncrementCost(choice,Economy_maintenance_cost,repair_maintenance_rate)
 
            SecureMaintenanceCost = MaintenanceIncrementCost(choice,Secure_maintenance_cost,repair_maintenance_rate)

            NetFlow = NormalBill(input_bill,inflationTariff,TaxBenefit,cuf_factor)
            disc_factor = [round((1-(cuf_factor/100))**years,2) for years in range(len(NetFlow))]
            
            if loan == 'yes':
                LeverageRatio = float(df[(df['Line Text'] == 'LeverageRatio(Com)')]['Cond Value'].values[0])
                EconomyTermLoan = (LeverageRatio/100)*Economy_cost
                SecureTermLoan = (LeverageRatio/100)*secure_cost
                downpaymentFrac = (100-LeverageRatio)/100
                EconomyDownpayment = downpaymentFrac*Economy_cost
                SecureDownpayment = downpaymentFrac*secure_cost
                Tenure = float(df[(df['Line Text'] == 'TermLoanTenure(Com)')]['Cond Value'].values[0])
                print(Tenure)
                ROI = float(df[(df['Line Text'] == 'TermLoanInterestRate(Com)')]['Cond Value'].values[0])
                print(ROI)
                economyEMI, secureEMI = EMI(Economy_cost,secure_cost,ROI,Tenure,downpaymentFrac)
                EconomyDebtInterest = InterestOnDebt(Economy_cost,ROI,economyEMI,LeverageRatio) # for economy option...
                SecureDebtInterest = InterestOnDebt(secure_cost,ROI,secureEMI,LeverageRatio) # for economy option...
                EconTotalExpense,EconTaxBenefitOnExpense,EconTotalTaxBenefit,EconNetFlow = TotalExpense(EconBillYearly,EconomyMaintenanceCost,EconomyDebtInterest,TaxBenefit,EconomyTaxOnDep,EconomyDownpayment,economyEMI,Tenure)
                SecTotalExpense,SecTaxBenefitOnExpense,SecTotalTaxBenefit,SecNetFlow = TotalExpense(SecBillYearly,SecureMaintenanceCost,SecureDebtInterest,TaxBenefit,SecureTaxOnDep,SecureDownpayment,secureEMI,Tenure)
                
                EconSavings = [-solarExpense+Expense for solarExpense,Expense in zip(EconNetFlow,NetFlow)]
                SecSavings = [-solarExpense+Expense for solarExpense,Expense in zip(SecNetFlow,NetFlow)]
                
                Econ_pv_savings = [i*j for i,j in zip(EconSavings,disc_factor)] 
                Sec_pv_savings = [i*j for i,j in zip(SecSavings,disc_factor)]

                Econ_cum_savings=CumSavings(Econ_pv_savings)
                Sec_cum_savings=CumSavings(Sec_pv_savings)
                
#                 EconPaybackPeriod = [i for i in Econ_cum_savings if i<=0]
#                 SecPaybackPeriod = [i for i in Sec_cum_savings if i<=0]

#                 EconPaybackPeriod = 1+abs(-Econ_cum_savings[1]/Econ_cum_savings[0])
#                 SecPaybackPeriod = 1+abs(-Sec_cum_savings[1]/Sec_cum_savings[0])

                EconPaybackPeriod = [i for i in Econ_cum_savings if i <= Economy_cost]
                SecPaybackPeriod = [i for i in Sec_cum_savings if i <= secure_cost]
            
            
                if battery_backup != 'no':
                    print("for Secure option...")
                    dataframe1= {"MonthlyUnitConsumed":str(monthly_billing),
                              "RecommendedDCUnit":str(secure_unit),
                              "RecommendedACUnit":str(secure_AC_cap),
                              "EnergyRequirement":str(energy_requirement),
                              "RecommendedSKU": secure_internal_SKU,
                               "CapitalCost":str(secure_cost),
                               "TermLoan":str(SecureTermLoan),
                               "TermLoanTenure":str(Tenure),
                                "TermLoanInterestRate":str(ROI),
                                "monthly_EMI":secureEMI/12,
                                "Savings_10":Sec_cum_savings[10],
                                "Savings_25":Sec_cum_savings[25],
                                "PayBackPeriod":len(SecPaybackPeriod),
                                "TreesSaved":np.ceil(num_trees_saved*secure_unit),
                                "CO2":CO2*secure_unit*25}
                    print(dataframe1)
                    return dataframe1
                else:
                    print("for Economy option...")
                    dataframe2 = {"MonthlyUnitConsumed":str(monthly_billing),
                                  "RecommendedDCUnit":str(Economy_unit),
                                  "RecommendedACUnit":str(Economy_AC_cap),
                                  "EnergyRequirement":str(energy_requirement),
                                  "RecommendedSKU": Economy_SKU,
                                   "CapitalCost":str(Economy_cost),
                                   "TermLoan":str(EconomyTermLoan),
                                   "TermLoanTenure":str(Tenure),
                                    "TermLoanInterestRate":str(ROI),
                                    "monthly_EMI":economyEMI/12,
                                     "Savings_10":Econ_cum_savings[10],
                                    "Savings_25":Econ_cum_savings[25],
                                     "PayBackPeriod":len(EconPaybackPeriod),
                                     "TreesSaved":np.ceil(num_trees_saved*Economy_unit),
                                     "CO2":CO2*Economy_unit*25}
                    print(dataframe2)
                    return dataframe2
            elif loan == 'no':
                economyEMI = 0
                secureEMI = 0
                Tenure = 0
                EconomyDownpayment = Economy_cost
                SecureDownpayment = secure_cost
                EconomyDebtInterest = 0
                SecureDebtInterest = 0
                EconTotalExpense,EconTaxBenefitOnExpense,EconTotalTaxBenefit,EconNetFlow = TotalExpense(EconBillYearly,EconomyMaintenanceCost,EconomyDebtInterest,TaxBenefit,EconomyTaxOnDep,EconomyDownpayment,economyEMI,Tenure)
                SecTotalExpense,SecTaxBenefitOnExpense,SecTotalTaxBenefit,SecNetFlow = TotalExpense(SecBillYearly,SecureMaintenanceCost,SecureDebtInterest,TaxBenefit,SecureTaxOnDep,SecureDownpayment,secureEMI,Tenure)
                
                EconSavings = [-solarExpense+Expense for solarExpense,Expense in zip(EconNetFlow,NetFlow)]
                SecSavings = [-solarExpense+Expense for solarExpense,Expense in zip(SecNetFlow,NetFlow)]

                Econ_pv_savings = [i*j for i,j in zip(EconSavings,disc_factor)] 
                Sec_pv_savings = [i*j for i,j in zip(SecSavings,disc_factor)]

                Econ_cum_savings=CumSavings(Econ_pv_savings)
                Sec_cum_savings=CumSavings(Sec_pv_savings)
                
#                 EconPaybackPeriod = [i for i in Econ_cum_savings if i<=0]
#                 SecPaybackPeriod = [i for i in Sec_cum_savings if i<=0]

#                 EconPaybackPeriod = 1+abs(-Econ_cum_savings[1]/Econ_cum_savings[0])
#                 SecPaybackPeriod = 1+abs(-Sec_cum_savings[1]/Sec_cum_savings[0])

                EconPaybackPeriod = [i for i in Econ_cum_savings if i <= Economy_cost]
                SecPaybackPeriod = [i for i in Sec_cum_savings if i <= secure_cost]
                
                if battery_backup != 'no':
                    print("for Secure option...")
                    dataframe1 =  {"MonthlyUnitConsumed":str(monthly_billing),
                                  "RecommendedDCUnit":str(secure_unit),
                                  "RecommendedACUnit":str(secure_AC_cap),
                                  "EnergyRequirement":str(energy_requirement),
                                  "RecommendedSKU":secure_internal_SKU ,
                                   "CapitalCost":str(secure_cost),
                                   "Savings_10":Sec_cum_savings[10],
                                   "Savings_25":Sec_cum_savings[25],
                                    "PayBackPeriod":len(SecPaybackPeriod),
                                     "TreesSaved":np.ceil(num_trees_saved*secure_unit),
                                      "CO2":CO2*secure_unit*25}
                    print(dataframe1)
                    return dataframe1
                else:
                    print("for Economy option...")
                    dataframe2 = {"MonthlyUnitConsumed":str(monthly_billing),
                                  "RecommendedDCUnit":str(Economy_unit),
                                  "RecommendedACUnit":str(Economy_AC_cap),
                                  "EnergyRequirement":str(energy_requirement),
                                  "RecommendedSKU": Economy_SKU,
                                   "CapitalCost":str(Economy_cost),
                                   "Savings_10":Econ_cum_savings[10],
                                   "Savings_25":Econ_cum_savings[25],
                                    "PayBackPeriod":len(EconPaybackPeriod),
                                     "TreesSaved":np.ceil(num_trees_saved*Economy_unit),
                                     "CO2":CO2*Economy_unit*25}
                    print(dataframe2)
                    return dataframe2
    else:
        return None,None

def lambda_handler(event, context):
    print(event)
    Option = TotalBill(df,
                    event["tarifftype"],
                    event["state"],
                    event["discom"],
                    event["district"],
                    event["monthlybill"],
                    event["sanctionload"],
                    event["rooftoparea"],
                    event["installationheight"],
                    event["batterybackup"],
                    event["batterycapacity"],
                    event["loanrequired"])
    
    # if isinstance(EconomyOption,pd.DataFrame)== False:
    #     return {"statusCode":100,
    #         "resp":"Not a valid input"}
    
    # else:
    return {'statusCode':200,
        "response":Option,
}