from abc import ABC, abstractmethod #abstract module used for declaring abstract class...

class Account(ABC):
    balance = 0
    depositChoice = ""
    
    @classmethod
    @abstractmethod
    def checkBalance(cls):
        pass
    
    @classmethod
    def amountToWithdraw(cls):
        print("\nEnter the Amount to Withdraw.\n")
        withdrawAmount = int(input())
        if(withdrawAmount > cls.balance or cls.balance == 0):
            print("Insifficient Fund!!")
            print("\nWould you like to deposit Money?(y or n)")
            cls.depositChoice = str(input())
            if(cls.depositChoice == 'y'):
                cls.amountToDeposit()
        else:
            cls.balance -= withdrawAmount
            print("Amount withdrawn successfully!!")

    @classmethod
    def amountToDeposit(cls):
        while(cls.depositChoice == 'y'):
            print("\nEnter the Amount to Deposit.\n")
            depositAmount = int(input())
            if(depositAmount > 0):
                cls.balance += depositAmount
                print("Amount deposited successfully!!")
                cls.depositChoice = 'n'
            else:
                print("Amount deposit unsuccessful!!.")
                print("Would you like to try again (y or n)")
                cls.depositChoice = str(input())
    @classmethod
    def mainMethod(cls):
        while(True):
            print("\nPlease choose from option below(press 1 or 2 or 3):\n1.Withdraw Money\n2.Deposit Money\n3.Check Balance\n4.Return to Main Menu")
            actionSelected = int(input())
            if(actionSelected == 1):
                cls.amountToWithdraw()
            elif(actionSelected == 2):
                cls.depositChoice = "y"
                cls.amountToDeposit()
            elif(actionSelected == 3):
                cls.checkBalance()
            elif(actionSelected == 4):
                break
            else:
                print("\nTry Again\n.")
    

