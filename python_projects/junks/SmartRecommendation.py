# function for Economy recommendation (Smart and Pro), returns DC unit, cost for low and high structure height 
# (for both Smart and Pro option )...
def SmartRecommendation(rooftopArea,struct_height,energyReq):
    try:
        # for 'Smart' option (for high and low values)...
        dc_capacity = df1[(df1['Option'] == 'Smart') & (df1['Structure Height'] == struct_height)]['DC Capacity (kWp)']
        dc_capacity = dc_capacity.tolist()
        min_rooftoparea = dc_capacity[0]*100
        if rooftopArea >= min_rooftoparea and energyReq >= min_rooftoparea/100:
            smart_unit = []
            for i in range(len(dc_capacity)):
                if (energyReq > dc_capacity[i] and energyReq < dc_capacity[i+1]) or (rooftopArea/100 > dc_capacity[i] and rooftopArea/100 < dc_capacity[i+1]):
                    final_units = dc_capacity[i]
                    smart_unit.append(final_units)
                elif energyReq == dc_capacity[i] or ((rooftopArea/100) == dc_capacity[i]):
                    final_units = dc_capacity[i]
                    smart_unit.append(final_units)
            print("Recommended unit (Smart option) for the given input (based on rooftop area given) is ",smart_unit[0])
            smart_cost = df1[(df1['Option'] == 'Smart') & (df1['Structure Height'] == struct_height) & (df1['DC Capacity (kWp)'] == smart_unit[0])]
            smart_cost = smart_cost.at[smart_cost.index[0],'Sale Price(With GST)']
            print("Price for the recommended unit is (for {}) is {}".format(struct_height,smart_cost))
            return smart_unit[0],smart_cost
        else:
            print("Minimun rooftop area should be ",min_rooftoparea," and Minimum Energy requirement is ",min_rooftoparea/100)
            return 0,0
    except Exception as e:
        print("Please Enter a valid input")
        return 0,0