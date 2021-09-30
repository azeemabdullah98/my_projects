# to check if sanction load is present for the discom provided and return none if no sanction load is present...
def CheckSanctionLoad(new_df,df,SanctionLoad):
    index7 = new_df.index
    condition4 = new_df['Line Text'] == 'SanctionLoad'
    condition5 = new_df['Line Text'] == 'SanctionLoad<=5'
    condition6 = new_df['Line Text'] == 'SanctionLoad>5'
    index4 = index7[condition4]
    index5 = index7[condition5]
    index6 = index7[condition6]
    print(index4)
    print(index5)
    print(index6)
    if len(index4) > 0 and len(index5) + len(index6) == 0:
        sl_formula = df.at[index4[0],'Cond Value']
        print(sl_formula)
        return sl_formula
    if len(index4) == 0 and len(index5) + len(index6) > 0:
        if SanctionLoad <=5:
            sl_formula = df.at[index5[0],'Cond Value']
            print(sl_formula)
            return sl_formula
        elif SanctionLoad > 5:
            sl_formula = df.at[index6[0],'Cond Value']
            print(sl_formula)
            return sl_formula
    else:
        return None