# to check if sanction load is present for the discom provided and return none if no sanction load is present...
def CheckSanctionLoad(new_df,SanctionLoad):
    try:
        regex = re.compile(r'SanctionLoad.*')
        sLoad = regex.findall(new_df['Line Text'].to_string())
        if len(sLoad) == 1:
            sl_formula = new_df[(new_df['Line Text'] == sLoad[0])]
            sl_formula = sl_formula.at[sl_formula.index[0],'Cond Value']
        if len(sLoad) == 2:
            if SanctionLoad <=5 or SanctionLoad <= 10 or SanctionLoad <=20:
                sl_formula = new_df[(new_df['Line Text'] == sLoad[0])]
                sl_formula = sl_formula.at[sl_formula.index[0],'Cond Value']
            elif SanctionLoad > 5 or SanctionLoad >10 or SanctionLoad >20:
                sl_formula = new_df[(new_df['Line Text'] == sLoad[1])]
                sl_formula = sl_formula.at[sl_formula.index[0],'Cond Value']
        if len(sLoad) == 3:
            if SanctionLoad <= 20:
                sl_formula = new_df[(new_df['Line Text'] == sLoad[0])]
                sl_formula = sl_formula.at[sl_formula.index[0],'Cond Value']
            elif SanctionLoad > 20 and SanctionLoad <= 50:
                sl_formula = new_df[(new_df['Line Text'] == sLoad[1])]
                sl_formula = sl_formula.at[sl_formula.index[0],'Cond Value']
            elif SanctionLoad > 50:
                sl_formula = new_df[(new_df['Line Text'] == sLoad[2])]
                sl_formula = sl_formula.at[sl_formula.index[0],'Cond Value']
        return sl_formula
    except Exception as e:
        print(e)
        return None