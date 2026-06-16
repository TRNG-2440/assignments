import random


class Account:
    def __init__(self,account_name, account_number, balance=0):
        self.account_name = account_name
        self.account_number = account_number
        self.balance = balance
        
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        self.balance += amount
        print(f"Deposited ${amount}. New balance: ${self.balance}")
    
    def account_details(self, account_type = "GEN"):
        print(f"Account Name: {self.account_name}")
        print(f"Account Number: {account_type}-{self.account_number}")
        print(f"Balance: ${self.balance}")
        
class CheckingAccount(Account):
    
    def __init__(self, account_name, account_number, balance=0):
        super().__init__(account_name, account_number, balance)
        
    def withdraw(self, amount):
        
        if amount > self.balance + 50:
            raise ValueError("Insufficient funds.")
        else:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")
            
    def account_details(self):
        super().account_details("CHK")

class SavingsAccount(Account):
    def __init__(self, account_name, account_number, balance=0):
        super().__init__(account_name, account_number, balance)
        self.withdraw_counter = 0
    
    def monthly_interest(self):
        interest_rate = .03
        interest = self.balance * interest_rate
        self.balance = self.balance + interest
        print(f"Monthly interest added: ${interest}. New balance: ${self.balance}")
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        elif self.withdraw_counter >= 3:
            raise ValueError("Maximum number of withdrawals exceeded.")
        else:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")
            self.withdraw_counter += 1
    
    def account_details(self):
        super().account_details("SAV")
        print(f"Number of withdrawals: {self.withdraw_counter}")
        

class InvestmentAccount(Account):
    def __init__(self, account_name, account_number, balance=1000):
        super().__init__(account_name, account_number, balance)
        self.min_balance = 1000
        
    def account_details(self):
        super().account_details("INV")
    
    def withdraw(self, amount):
        if self.balance - amount < self.min_balance:
            raise ValueError("Insufficient funds.")
        else:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")
            
    def interest(self):
        interest_rate = random.uniform(0.01, 0.10)
        interest = self.balance * interest_rate
        self.balance = self.balance + interest
        print(f"Interest added: ${interest}. New balance: ${self.balance}")
        
class Bank():
    
    account_number = 0;
    def __init__(self):
        self.accounts = []
        
    def addAccount(self, account_type):
        
        account_name = input("Enter account name: ")
        balance = float(input("Enter initial balance: "))
        if account_type == "SAV":
            account = SavingsAccount(account_name, self.account_number, balance)
            self.account_number += 1
        elif account_type == "CHK":
            account = CheckingAccount(account_name, self.account_number, balance)
            self.account_number += 1
        elif account_type == "INV":
            if balance < 1000:
                raise ValueError("Initial balance must be at least $1000.")
                return
            account = InvestmentAccount(account_name, self.account_number, balance)
            self.account_number += 1
        else:
            print("Invalid account type.")
            return
        self.accounts.append(account)
        
    def lookupAccount(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        print("Account not found.")
        
    def displayAccounts(self):
        for account in self.accounts:
            print(f"Name: {account.account_name}, Balance: ${account.balance}")
            
        
bank = Bank()
while True:
    
    print("*" * 20)
    print(" "*3 + "Isauro Banking" + " "*3)
    print("*" * 20)
    
    print("1. Open an account")
    print("2. Select an account")
    print("3. Display all accounts")
    print("4. Exit")
    
    choice = input("Enter your choice: ")
    
    match choice:
        case "1":
            print(" Select an account type:")
            print("1. Checking Account")
            print("2. Savings Account")
            print("3. Investment Account")
            account_type = input("Enter your type: ")
            
            if account_type == "1":
                account = bank.addAccount("CHK")
            elif account_type == "2":
                account = bank.addAccount("SAV")
            elif account_type == "3":
                account = bank.addAccount("INV")
            else:
                print("Invalid account type.")
        case "2":
            try:
                account_number = int(input("Enter account number: "))
                account = bank.lookupAccount(account_number)
                if account:
                    while True:
                        print("1. Deposit")
                        print("2. Withdraw")
                        print("3. View Details")
                        print("4. Monthly Interest / Apply Return")
                        print("0. Exit")
                        
                        selection = input("Enter your choice: ")
                        if(selection == "1"):
                            amount = float(input("Enter amount to deposit: "))
                            try:
                                account.deposit(amount)
                            except ValueError as e:
                                print(e)
                        elif(selection == "2"):
                            amount = float(input("Enter amount to withdraw: "))
                            try:
                                account.withdraw(amount)
                            except ValueError as e:
                                print(e)
                        elif(selection == "3"):
                            account.account_details()
                        elif(selection == "4"):
                            if isinstance(account, SavingsAccount):
                                account.monthly_interest()
                            elif isinstance(account, InvestmentAccount):
                                account.interest()
                        elif(selection == "0"):
                            print("Exiting...")
                            break
                        else:
                            print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")

        case "3":
            bank.displayAccounts()
        case "4":
            print("Exiting...")
            break