# main function...
def TotalBill(choice,discom,input_bill,SanctionLoad,rooftopArea,struct_height,battery_backup,loan,default=True):
    discom_list = df['Main Cond ID'].unique().tolist()
    if discom in discom_list:
        print("for {} type ".format(choice))
        new_df = df[(df['Cond Type'] == choice) & (df['Sub Cond ID'] == discom)]
        fc_charge = new_df[(new_df['Line Text'] == 'defaultFixedCharge')]
        fc_charge = fc_charge.at[fc_charge.index[0],'Cond Value']
        irradiance = new_df[(new_df['Line Text'] == 'Irradiance')]
        Irradiance = float(irradiance.at[irradiance.index[0],'Cond Value'])
        CondValue = input_bill - int(fc_charge)
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
        smart_unit,smart_cost = SmartRecommendation(rooftopArea,struct_height,energy_requirement)
        pro_unit,pro_cost = ProRecommendation(rooftopArea,struct_height,energy_requirement)
        secure_unit,secure_cost = PremiumRecommendation(rooftopArea,struct_height,energy_requirement,battery_backup)
        if abs(rooftopArea-(smart_unit*100)) < abs(rooftopArea-(pro_unit*80)):
            Economy_unit = smart_unit
            Economy_cost = smart_cost
        else:
            Economy_unit = pro_unit
            Economy_cost = pro_cost
        print(Economy_cost)
        print(Economy_unit)
        costPerkWp = [i for i in df['CostPerkWp'] if pd.notna(i) == True][0]
        Economy_power_gen = float(Economy_unit)*Irradiance # solar power generation...
        Secure_power_gen = float(secure_unit)*Irradiance # solar power generation...
        cuf_factor = [i for i in df['CUFdegradationFactor'] if pd.notna(i) == True][0]
        EconomyPowerGen, EconomyYearlyIncome = SolarDepreciationCost(Economy_power_gen,cuf_factor,grid_tariff)

        SecurePowerGen, SecureYearlyIncome = SolarDepreciationCost(Secure_power_gen,cuf_factor,grid_tariff)
        

        maintenance_charge = [i for i in df['defaultMaintenanceCharge'] if pd.notna(i) == True][0]
        maintenance_rate = [j for j in df['MaintenanceRate'] if pd.notna(j) == True][0]
        util_factor = [i for i in df['solarCapacityUtilFactor'] if pd.notna(i) == True][0]
        Economy_maintenance_charge = maintenance_charge*Economy_unit
        secure_maintenance_charge = maintenance_charge*secure_unit
        MaintenanceCost = MaintenanceIncrementCost(Economy_maintenance_charge,maintenance_rate)
        if loan == 'yes' and default == True:
#             pro_maintenance_charge = maintenance_charge*pro_unit
            R = [i for i in df['TermLoanInterestRate'] if pd.notna(i) == True][0]
            N = [i for i in df['TermLoanTenure'] if pd.notna(i) == True][0]
            LeverageRatio = [i for i in df['LeverageRatio'] if pd.notna(i) == True][0]
            downpaymentPer = (100-LeverageRatio)/100
            CapitalCost = costPerkWp*Economy_unit
            TermLoan = (LeverageRatio/100)*CapitalCost
            economyEMI,secureEMI = EMI(Economy_cost,secure_cost,R,N,downpaymentPer)
            downpayment = downpaymentPer*CapitalCost
            net_cash_flow,cum_cash_flow = CashFlow(EconomyYearlyIncome,economyEMI,MaintenanceCost,downpayment)
            dataframe = pd.Series({"UnitConsumedPerMonth(kWh)":monthly_billing,
                           "Irradiance(kWh)":Irradiance,
                           "solarPVplantCapacity(Economy)(kWp)":Economy_unit,
                           "CostperkWp(Rs/kWp)":costPerkWp,
                           "CapitalCost":CapitalCost,
                           "LeverageRatio":LeverageRatio,
                           "TermLoan":TermLoan,
                          "TermLoanTenure":N,
                          "TermLoanInterestRate":R,
                          "CurrentElectricityCharge":grid_tariff,
                          "TariffEscalation":downpaymentPer*100,
                          "EquityInvestment":downpayment,
                          "ExpectedSolarUtilizationFactor":eval(util_factor)*100,
                          "AnnualSolarCUFdegradationFactor":cuf_factor,
                            "AnnualMaintenanceCostperkWp":maintenance_charge,
                            "MaintenanceRate":maintenance_rate,
                            "GridTariffPaidtoCustomer":grid_tariff,
                            "SolarPowerGeneration":EconomyPowerGen,
                            "YearlyIncome":EconomyYearlyIncome,
                            "DebtServicing/EMI(Yearly)":economyEMI,
                            "MaintenanceCost":MaintenanceCost,
                            "NetCashFlow":net_cash_flow,
                            "CumulativeCashFlow":cum_cash_flow})
            print(dataframe)
#             with open("c:/python_projects/solar_calculator/sample_output.json",'a+') as f:
#                 json.dump(dataframe,f,indent=2)
#         dataframe1 = pd.DataFrame(data = ['GridTariffPaidtoCustomer',
#                                           'SolarPowerGeneration',
#                                          'YearlyIncome',
#                                          'MaintenanceCost'])