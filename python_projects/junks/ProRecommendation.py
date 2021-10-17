def ProRecommendation(rooftopArea,struct_height,energyReq):
    try:
     # for 'Pro' option (for high and low values)...
        dc_capacity1 = df1[(df1['Option'] == 'Pro') & (df1['Structure Height'] == struct_height)]['DC Capacity (kWp)']
        dc_capacity1 = dc_capacity1.tolist()
        min_rooftoparea1 = dc_capacity1[0]*80
        if rooftopArea >= min_rooftoparea1 and energyReq >= min_rooftoparea1/80:
            pro_unit = []
            for i in range(len(dc_capacity1)):
                if (energyReq > dc_capacity1[i] and energyReq < dc_capacity1[i+1]) or (rooftopArea/80 > dc_capacity1[i] and rooftopArea/80 < dc_capacity1[i+1]):
                    final_units = dc_capacity1[i]
                    pro_unit.append(final_units)
                elif energyReq == dc_capacity1[i] or ((rooftopArea/80) == dc_capacity1[i]):
                    final_units = dc_capacity1[i]
                    pro_unit.append(final_units)
            print("Recommended unit (Pro option) for the given input (based on rooftop area given) is ",pro_unit[0])
            pro_cost = df1[(df1['Option'] == 'Pro') & (df1['Structure Height'] == struct_height) & (df1['DC Capacity (kWp)'] == pro_unit[0])]
            pro_cost = pro_cost.at[pro_cost.index[0],'Sale Price(With GST)']
            print("Price for the recommended unit is (for {}) is {}".format(struct_height,pro_cost))
            return pro_unit[0],pro_cost
        else:
            print("Minimun rooftop area should be ",min_rooftoparea1," and Minimum Energy requirement is ",min_rooftoparea1/80)
            return 0,0
    except Exception as e:
        print("Please Enter a valid input")
        return 0,0