
from typing import override
import random

class Account:
    """'Account' class that holds common attributes 
    such as owner name, account number, and balance. Supports depositing
    funds and displaying account details."""
    def __init__(self,owner_name,bal, random_id):
        self.__owner_name = owner_name
        self.__acct_num = random_id
        self.__bal = bal
    
    #takes any int
    def deposit(self,val):
        #only supports depositing
        try:
            deposit = abs(val) #Possibly throws TypeError for non int/float
            self.__bal += deposit
            print(f"Deposited: {deposit:<10,.2f}. New Balance: {self.__bal:<10,.2f}")
           
        except:
            raise #propagating exception to deal with is later. 

            
    def display(self):
        print("______________________________")
        print(f" {'Owner Name':<18} {':'} {self.__owner_name:<20}")
        print(f" {'Account Number':<18} {':'} {self.__acct_num:<20}")
        print(f" {'Balance':<18} {':'} ${self.__bal:<20,.2f}")
        print("______________________________")

    


class CheckingAccount(Account):
    """'CheckingAccount' subclass with the following unique behavior:
    - Supports overdraft protection up to a set limit — withdrawals that would exceed 
    the balance may draw from the overdraft buffer, but not beyond it."""
   
    def __init__(self, owner_name, bal, overdraft = 100):
        super().__init__(owner_name,bal)
        self.__overdraft = overdraft
        

    def withdraw(self, amnt):
        withdrawal = self.__bal -amnt
        if withdrawal + self.__overdraft < (0):
            #self.__bal -= amnt
            raise ValueError("Overdraft Exceeded! Cannot withdraw ${amnt}") 
        else:
            self.__bal -= amnt
            print(f"Withdrawing: {amnt:<10,.2f}. New Balance: {self.__bal:<10,.2f}")


class SavingsAccount(Account):
    """Create a `SavingsAccount` subclass with the following unique behavior:
    - Applies a monthly interest rate to the balance when triggered.
      Note: the example indicates a limit of 3, but you are free to set any reasonable value you wish"""
    MAX_WITHDRAWALS = 3
    INTEREST = 2.5

    def __init__(self, owner_name, bal ):
        super().__init__(owner_name, bal)
        self.__max_wd = self.MAX_WITHDRAWALS


    def apply_interest(self):
       """Applies monthly interest rate to balance"""
       interest_amnt = self.__bal * self.INTEREST
       self.__bal -= interest_amnt
       print("Applied monthly interest ({self.INTEREST}%). New balance: ${self.__bal:,.2f}")
       
    @override
    def withdraw(self, amnt):
        """Enforces a maximum number of withdrawals per month; attempts beyond the
        limit should be rejected."""
        if self.__max_wd >0:
            if self.__bal - amnt <0:
               raise ValueError("Withdrawal will result in overdraft! Current Balance = ${self.__bal:,.2f}")
            else:
                self.__max_wd -= 1
                self.__bal -= amnt

        else:
            raise ValueError("Withdrawal Limit Hit! Balance = ${self.__bal:,.2f}") 
            
class InvestmentAccount(Account):
    MINIMUM_BAL = 40
   
    @override
    def withdraw(self, amnt):
        """Enforces a maximum number of withdrawals per month; attempts beyond the
        limit should be rejected."""
        if self.__bal - amnt < self.MINIMUM_BAL:
             raise ValueError("Minimum Balance must be ${self.MINIMUM_BAL:,.2f}! Current Balance = ${self.__bal:,.2f}")
        else:
            self.__bal -= amnt

    def invest(self):
        """method to apply a variable return rate to simulate investment growth."""
        rate = random_float(.07,.10)  #generate a variable return rate 
        new_bal = self.__bal + (self.__bal * rate)
        self.__bal = new_bal
        rate  = rate  * 10
        print("Applied variable return rate ({rate:.1f}%). New balance: ${self.__bal:,.2f}")

class Bank:
    """" 
   - Opening a new account of any supported type
   - Looking up an account by account number
   - Listing all accounts and their current balances
   """
    

    def __init__(self):
        self.__account_dict = {}

    def open_acct(self,type):
        pass
        

    def accnt_lookup(self, acct_num):
        pass

    def displayAll(self):
        pass




    


def random_id():
    return random.randint(100000,999999)

    

    


def random_float(a,b):
    return random.uniform(a,b)


            


    
    
  
        





def main():
    #for testing
    this_acct = Account("me",30.00,000000)
    this_acct.deposit()
    this_acct.display()


if __name__ == "__main__":
    main()




