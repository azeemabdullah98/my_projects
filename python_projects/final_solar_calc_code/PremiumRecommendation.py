# function for Premium Recommendation (Secure)
def PremiumRecommendation(rooftopArea,struct_height,energyReq,battery_backup):
    try: 
        battery_value = df1[(df1['Option'] == 'Secure') & (df1['Structure Height'] == struct_height)]['Battery Backup'].unique().tolist()
        if battery_backup not in battery_value or battery_backup == None:
            battery_backup = battery_value[-1]
        dc_capacity = df1[(df1['Option'] == 'Secure') & (df1['Structure Height'] == struct_height) & (df1['Battery Backup'] == battery_backup)]['DC Capacity (kWp)']
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
            secure_cost = df1[(df1['Option'] == 'Secure') & (df1['Structure Height'] == struct_height) & (df1['DC Capacity (kWp)'] == secure_unit[0])]
            secure_cost = secure_cost.at[secure_cost.index[0],'Sale Price(With GST)']
            print("Price for the recommended unit is (for {}) is {}".format(struct_height,secure_cost))
            return secure_unit[0],secure_cost
        else:
            print("Minimun rooftop area should be ",min_rooftoparea," and Minimum Energy requirement is ",min_rooftoparea/100," should be available for Premium setup")
            return 0,0
    except Exception as e:
        print("Can't do for Premium Type. Value not available in the table")
        return 0,0