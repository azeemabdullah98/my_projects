from datetime import datetime

from savingsAccount import SavingsAccount
from currentAccount import CurrentAccount


cusName = str(input("Please enter your name:\n"))
timeOfDay = datetime.now().time().hour
if(timeOfDay > 6 and timeOfDay < 12):
    print("Good Morning!! {}.".format(cusName.capitalize()))
elif (timeOfDay > 12 and timeOfDay < 18):
    print("Good Afternoon!! {}.".format(cusName.capitalize()))
elif (timeOfDay > 18):
    print("Hello!! {}.".format(cusName.capitalize()))

print("Welcome to XYZ Bank")
while(True):
    print("\nPlease choose from option below(press 1 or 2 or 3):\n1.Savings Account\n2.Current Account\n3.exit")
    accountSelected = int(input())
    if (accountSelected == 1):
        saveAccount = SavingsAccount()
        saveAccount.mainMethod()
    elif (accountSelected == 2):
        currAccount = CurrentAccount()
        currAccount.mainMethod()
    elif (accountSelected == 3):
        print("\nThank you for banking with us\n")
        break
    else:
        print("Try Again.")