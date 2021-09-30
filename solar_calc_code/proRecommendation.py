def ProRecommendation(rooftopArea,struct_height,energyReq):
    try:
     # for 'Pro' option (for high and low values)...
        dc_capacity1 = df1[(df1['Option'] == 'Pro') & (df1['Structure Height'] == 'Low(0.3m)')]['DC Capacity (kWp)']
        dc_capacity1 = dc_capacity1.tolist()
        min_rooftoparea1 = dc_capacity1[0]*80
        if rooftopArea >= min_rooftoparea1 and energyReq >= min_rooftoparea1/80:
            pro_unit = []
            for i in range(len(dc_capacity1)):
                if (energyReq > dc_capacity1[i] and energyReq < dc_capacity1[i+1]) or (rooftopArea/100 > dc_capacity1[i] and rooftopArea/100 < dc_capacity1[i+1]):
                    final_units = dc_capacity1[i]
                    pro_unit.append(final_units)
                elif energyReq == dc_capacity1[i] or ((rooftopArea/100) == dc_capacity1[i]):
                    final_units = dc_capacity1[i]
                    pro_unit.append(final_units)
            print("Recommended unit (Pro option) for the given input (based on rooftop area given) is ",pro_unit[0])
            if struct_height == 'low' or struct_height == 0.3:
                pro_low_cost = df1[(df1['Option'] == 'Pro') & (df1['Structure Height'] == 'Low(0.3m)') & (df1['DC Capacity (kWp)'] == pro_unit[0])]['Sale Price(With GST)'].tolist()[0]
                print("Price for the recommended unit is (for low struct height(0.3m))",pro_low_cost)
                return pro_unit[0],pro_low_cost
            elif struct_height == 'high' or struct_height == 2.5:
                pro_high_cost = df1[(df1['Option'] == 'Pro') & (df1['Structure Height'] == 'High(2.5m)') & (df1['DC Capacity (kWp)'] == pro_unit[0])]['Sale Price(With GST)'].tolist()[0]
                print("Price for the recommended unit is (for high struct height(2.5m))",pro_high_cost)
                return pro_unit[0],pro_high_cost
        else:
            print("Minimun rooftop area should be ",min_rooftoparea1," and Minimum Energy requirement is ",min_rooftoparea1/80)
    except Exception as e:
        print(e)
        return None