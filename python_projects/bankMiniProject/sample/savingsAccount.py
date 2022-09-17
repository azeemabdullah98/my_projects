from account import Account

class SavingsAccount(Account):
    @classmethod
    def checkBalance(cls):
        print("\nThe Balance in your Savings Account is {}\n".format(cls.balance))