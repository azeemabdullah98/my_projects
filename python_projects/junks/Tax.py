# to check if tax is available for the particular discom else return none...
def CheckTax(new_df):
    try:
        tax = new_df[(new_df['Line Text'] == 'Tax')]
        tax = new_df.at[tax.index[0],'Cond Value']
        return tax
    except Exception as e:
        return None