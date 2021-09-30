# function for Premium Recommendation (Secure)
def PremiumRecommendation(rooftopArea,struct_height,energyReq,battery_backup):
    try:
        dc_capacity = df1[(df1['Option'] == 'Secure') & (df1['Structure Height'] == 'Low(0.3m)') & (df1['Battery Backup'] == battery_backup)]['DC Capacity (kWp)']
        dc_capacity = dc_capacity.tolist()
        min_rooftoparea = dc_capacity[0]*100
        if rooftopArea >= min_rooftoparea and energyReq >= min_rooftoparea/100:
            secure_unit = []
            for i in range(len(dc_capacity)):
                if (energyReq > dc_capacity[i] and energyReq < dc_capacity[i+1]) or (rooftopArea/100 > dc_capacity[i] and rooftopArea/100 < dc_capacity[i+1]):
                    final_units = dc_capacity[i]
                    secure_unit.append(final_units)
                elif energyReq == dc_capacity[i] or ((rooftopArea/100) == dc_capacity[i]):
                    final_units = dc_capacity[i]
                    secure_unit.append(final_units)
            print("For a Given battery backup ",battery_backup)
            print("Recommended unit (Secure option) for the given input (based on rooftop area given) is ",secure_unit[0])
            if struct_height == 'low' or struct_height == 0.3:
                secure_low_cost = df1[(df1['Option'] == 'Secure') & (df1['Structure Height'] == 'Low(0.3m)') & (df1['Battery Backup'] == battery_backup) & (df1['DC Capacity (kWp)'] == secure_unit[0])]['Sale Price(With GST)'].tolist()[0]
                print("Price for the recommended unit is (for low struct height(0.3m))",secure_low_cost)
                return secure_unit[0],secure_low_cost
            elif struct_height == 'high' or struct_height == 2.5:
                secure_high_cost = df1[(df1['Option'] == 'Secure') & (df1['Structure Height'] == 'High(2.5m)') & (df1['Battery Backup'] == battery_backup) & (df1['DC Capacity (kWp)'] == secure_unit[0])]['Sale Price(With GST)'].tolist()[0]
                print("Price for the recommended unit is (for high struct height(2.5m))",secure_high_cost)
                return secure_unit[0],secure_high_cost
        else:
            print("Minimun rooftop area should be ",min_rooftoparea1," and Minimum Energy requirement is ",min_rooftoparea1/80)
    except Exception as e:
        print(e)
        return None