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