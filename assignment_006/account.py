
from typing import override
import random

class Account:
    """'Account' class that holds common attributes 
    such as owner name, account number, and balance. Supports depositing
    funds and displaying account details."""

    def __init__(self,owner_name,bal,id):
        self._owner_name = owner_name
        self._acct_num = id
        self._bal = bal

    #takes any int
    def deposit(self,val):
        #only supports depositing
        try:
            deposit = abs(val) #Possibly throws TypeError for non int/float
            self._bal += deposit
            print(f"Deposited: {deposit:<10,.2f}. New Balance: {self._bal:<10,.2f}")
           
        except:
            raise #propagating exception to deal with it later. 

            
    def display(self):
        print("______________________________")
        print(f" {'Owner Name':<18} {':'} {self._owner_name:<20}")
        print(f" {'Account Number':<18} {':'} {self._acct_num:<20}")
        print(f" {'Balance':<18} {':'} ${self._bal:<20,.2f}")
        print("______________________________")

    


class CheckingAccount(Account):
    """'CheckingAccount' subclass with the following unique behavior:
    - Supports overdraft protection up to a set limit — withdrawals that would exceed 
    the balance may draw from the overdraft buffer, but not beyond it."""
    OVERDRAFT_LIMIT = 100
    TYPE = "Checking"

    def __init__(self, owner_name, bal, id):
        super().__init__(owner_name,bal,id)
        self._overdraft = self.OVERDRAFT_LIMIT
       
        

    def withdraw(self, amnt):
        withdrawal = self._bal -amnt
        if withdrawal + self.OVERDRAFT_LIMIT < (0):
            #self._bal -= amnt
            raise ValueError(f"Overdraft Exceeded! Cannot withdraw ${amnt}")
        else:
            self._bal -= amnt
            print(f"Withdrawing: {amnt:<10,.2f}. New Balance: {self._bal:<10,.2f}")

    @override
    def display(self):
        print("______________________________")
        print(f" {'Owner Name':<18} {':'} {self._owner_name:<20}")
        print(f" {'Account type':<18} {':'} ${'Checking':<20}")
        print(f" {'Account Number':<18} {':'} {self._acct_num:<20}")
        print(f" {'Balance':<18} {':'} ${self._bal:<20,.2f}")
        print(f" {'Overdraft Limit':<18} {':'} ${self.OVERDRAFT_LIMIT:<20,.2f}")
        print("______________________________")


class SavingsAccount(Account):
    """Create a `SavingsAccount` subclass with the following unique behavior:
    - Applies a monthly interest rate to the balance when triggered.
      Note: the example indicates a limit of 3, but you are free to set any reasonable value you wish"""
    MAX_WITHDRAWALS = 3
    INTEREST = 2.5
    TYPE = "Savings"

    def __init__(self, owner_name, bal,id ):
        super().__init__(owner_name, bal,id)
        self._max_wd = self.MAX_WITHDRAWALS


    def apply_interest(self):
       """Applies monthly interest rate to balance"""
       interest_amnt = self._bal * self.INTEREST
       self._bal -= interest_amnt
       print("Applied monthly interest ({self.INTEREST}%). New balance: ${self._bal:,.2f}")
       
    
    def withdraw(self, amnt):
        """Enforces a maximum number of withdrawals per month; attempts beyond the
        limit should be rejected."""
        if self._max_wd >0:
            if self._bal - amnt <0:
               raise ValueError("Withdrawal will result in overdraft! Current Balance = ${self._bal:,.2f}")
            else:
                self._max_wd -= 1
                self._bal -= amnt
                self.display()

        else:
            raise ValueError("Withdrawal Limit Hit! Balance = ${self._bal:,.2f}") 
        
    @override
    def display(self):
        withdrawals_left = (f"{self._max_wd}/{self.MAX_WITHDRAWALS}")
        print("______________________________")
        print(f" {'Owner Name':<18} {':'} {self._owner_name:<20}")
        print(f" {'Account Number':<18} {':'} {self._acct_num:<20}")
        print(f" {'Account type':<18} {':'} ${'Savings':<20}")
        print(f" {'Balance':<18} {':'} ${self._bal:<20,.2f}")
        print(f" {'Withdrawals':<18} {':'} {withdrawals_left: <20}")
        print(f" {'Interest Rate':<18} {':'} {self.INTEREST:.1f}%")
        print("______________________________")

            
class InvestmentAccount(Account):
    MINIMUM_BAL = 40
    TYPE = "Investment"

    def __init__(self, owner_name, bal,id):
        super().__init__(owner_name, bal,id)
        self._rate = random.uniform(0.03, 0.07) #variable return rate between 3% and 7%

    def withdraw(self, amnt):
        """Enforces a maximum number of withdrawals per month; attempts beyond the
        limit should be rejected."""
        if self._bal - amnt < self.MINIMUM_BAL:
             raise ValueError("Minimum Balance must be ${self.MINIMUM_BAL:,.2f}! Current Balance = ${self._bal:,.2f}")
        else:
            self._bal -= amnt

    def get_rate(self):
        return self._rate

    def invest(self):
        """method to apply a variable return rate to simulate investment growth."""
        new_bal = self._bal + (self._bal * self._rate)
        self._bal = new_bal
        return_rate = self._rate * 100
        print(f"Applied investment return ({return_rate:.1f}%). New balance: ${self._bal:,.2f}")
    

    @override
    def display(self):

        print("______________________________")
        print(f" {'Owner Name':<18} {':'} {self._owner_name:<20}")
        print(f" {'Account Number':<18} {':'} {self._acct_num:<20}")
        print(f" {'Account type':<18} {':'} ${'Investment':<20}")
        print(f" {'Balance':<18} {':'} ${self._bal:<20,.2f}")
        print(f" {'Investment Rate':<18} {':'} {self._rate * 100:.1f}%")
        print(f" {'Minimum Balance':<18} {':'} ${self.MINIMUM_BAL:,.2f}")
        print("______________________________")




