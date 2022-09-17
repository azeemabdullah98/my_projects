from account import Account

class CurrentAccount(Account):
    @classmethod
    def checkBalance(cls):
        print("\nThe Balance in your Current Account is {}\n".format(cls.balance))