def TotalBill(discom,input_bill,SanctionLoad):
    discom_list = df['Main Cond ID'].unique().tolist()
    if discom in discom_list:
        index = df.index
        condition = df['Main Cond ID'] == discom
        index = index[condition] # to get the index of the rows containing the particular discom...
        new_df = df.iloc[index[0]:index[-1]+1,:] # new dataframe that contains rows for a particular discom...
        new_df_index = new_df.index
        condition1 = new_df['Line Text'] == 'defaultFixedCharge'
        index1 = new_df_index[condition1] # index for the particular discom give by the user (for getting the fixed charge value)...
        condition3 = new_df['Line Text'] == 'Irradiance'
        index3 = new_df_index[condition3] # index for the particular discom given by the user (for getting the irradiance value)...
        fc_charge = df.at[index1[0],'Cond Value']
        irradiance = df.at[index3[0],'Cond Value'] # irradiance for a particular discom...
        CondValue = input_bill - int(fc_charge)
        print(CondValue)
        tax = CheckTax(new_df,df) # function to check if tax available for the particular discom or not...
        sl_formula = CheckSanctionLoad(new_df,df,SanctionLoad) # function to check if sanctionload is given for a particular discom or not...
        if tax != None:
            CondValue = CondValue-(float(tax)*CondValue)
            print(CondValue)
        if sl_formula != None:
            CondValue = abs(eval(sl_formula))
            print(CondValue)
        print(CondValue)
        lowerValue = [lv for lv in new_df['LowerValue'] if pd.notna(lv) == True] # lower range...
        upperValue = [uv for uv in new_df['UpperValue'] if pd.notna(uv) == True] # upper range...
        for low,up in zip(lowerValue,upperValue):
            if CondValue in range(int(low),int(up+1)):
                condition2 = new_df['LowerValue'] == low
                index2 = new_df_index[condition2]
                print(index2)
            elif low==up and CondValue > up:
                condition2 = new_df['LowerValue'] == low 
                index2 = new_df_index[condition2]
                print(index2)  
        lineText = df.at[index2[0],'Cond Value'] # indexing to get the formula for monthly saving...
        monthly_billing = eval(lineText)
        yearly_billing = monthly_billing*12
        energy_requirement = float(yearly_billing)/float(irradiance)
        grid_tariff = input_bill/monthly_billing
        print("monthly billing is ",monthly_billing)
        print("yearly billing is ",yearly_billing)
        print("Energy Requirement (yearly billing/irradiance) is ",energy_requirement)
        print("Grid Tariff is ",grid_tariff)
    return grid_tariff