# function to calculate yearly EMI for both Economy and Secure,return EconomyEMI and SecureEMI...
def EMI(P1,P2,R,N,downpaymentPer):
    EMI_formula = [i for i in df['EMI'] if pd.notna(i) == True]
    EMI_formula = EMI_formula[0]
    R = (R)/(12*100)
    N = N*12
    if downpaymentPer != 0:
        temp = [P1*downpaymentPer,P2*downpaymentPer]
    else:
        temp = [P1,P2]
    # for 'Economy option...
    P = P1-temp[0]
    numerator, denominator = EMI_formula.split("/")
    EconomyEMI = (eval(numerator)/eval(denominator))*12
    print(EconomyEMI)
    # for 'secure' option...
    P = P2-temp[1]
    numerator, denominator = EMI_formula.split("/")
    secureEMI = (eval(numerator)/eval(denominator))*12
    print(secureEMI)
    return EconomyEMI,secureEMI