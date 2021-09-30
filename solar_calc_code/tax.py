# to check if tax is available for the particular discom else return none...
def CheckTax(new_df,df):
    try:
        index7 = new_df.index
        condition4 = new_df['Line Text'] == 'Tax'
        index4 = index7[condition4]
        tax = df.at[index4[0],'Cond Value']
        return tax
    except Exception as e:
        return None