# Define classes
class Account:
    def __init__(self, owner_name:str, account_number:str, balance:str):
        self.owner_name = owner_name
        self.account_number = account_number
        self.balance = balance

    def depositMoney(self, deposit_amount): # TODO
        return
    
    def returnAccountDetails(self): # TODO
        return

class Bank:
    def createCheckingAccount(self): # TODO
        return
    
    def createSavingsAccount(self): # TODO
        return
    
    def createInvestmentAccount(self): # TODO
        return
    
class checkingAccount(Account):
    def __init__(self):
        self.__accounts = []  # Private list of Account objects
    
    