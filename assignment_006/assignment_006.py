# depedencies
import random
import string

# exception classes for account methods
class InsufficientFundsError(Exception):
    pass

class WithdrawsUsedError(Exception):
    pass

class InsufficientBalanceError(Exception):
    pass

class MinimumBalanceError(Exception):
    pass

# generate account number
# ------------------------
# TODO: ADD FUNCTIONALITY FOR CHECKING ACCOUNT NUMBER IS UNIQUE

def generate_account_number(prefix: str, length: int = 6) -> str:
    digits = ''.join(random.choices(string.digits, k = length))
    return f"{prefix}-{digits}"

# ------------------------    

# base Account class
class Account:
    def __init__(self, name: str, number: str, balance: float) -> None:
        self.name = name
        self.number = number
        self.balance = balance
    
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be at least 0.01")
        self.balance += amount
    
    def details(self):
        print("-" * 25)
        print("Account Details")
        print("-" * 25)
        print(f"Owner: {self.name}")
        print(f"Account #: {self.number}")
        print(f"Balance: ${self.balance:.2f}")

# checking subclass
class CheckingAccount(Account):
    def __init__(self, name: str, number: str, balance: float, overdraft_limit: float = 500):
        super().__init__(name, number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float): 
        if amount <= 0:
            raise ValueError("Withdrawl amount must be positive.")
        elif amount - self.balance > self.overdraft_limit:
            raise InsufficientFundsError("Withdraw would exceed the overdraft limit.")
        self.balance -= amount

    def details(self):
        super().details()
        print(f"Overdraft Limit: ${self.overdraft_limit:.2f}")
        print("-" * 25)

# Savings subclass
class SavingsAccount(Account):
    def __init__(self, name: str, number: str, balance: float,
    interest_rate: float, withdraws_limit: int, withdraws_used: int = 0):
        super().__init__(name, number, balance)
        self.interest_rate = interest_rate
        self.withdraws_limit = withdraws_limit
        self.withdraws_used = withdraws_used
    
    def withdraw(self, amount: float):
        if amount < 0:
            raise ValueError("Withdraw amount must be at least $0.01")
        elif self.withdraws_used >= self.withdraws_limit:
            raise WithdrawsUsedError("Monthly withdraws limit reached.") 
        elif amount > self.balance:
            raise InsufficientBalanceError("Error: Insufficient balance.")
        else:
            self.balance -= amount
            self.withdraws_used += 1
    
    def apply_interest(self):
        self.balance *= (1 + self.interest_rate)

    def details(self):
        super().details()
        print(f"Interest Rate: {self.interest_rate * 100}%")
        print(f"Monthly Withdraw Limit: {self.withdraws_limit}")
        print(f"Monthly Withdraws Used: {self.withdraws_used}")
        print("-" * 25)

class InvestmentAccount(Account):
    def __init__(self, name: str, number: str, balance: float, minimum_balance: float) -> None:
        super().__init__(name, number, balance)
        self.minimum_balance = minimum_balance

    def withdraw(self, amount: float):
        if amount < 0:
            raise ValueError("Withdraw amount must be at least $0.01")
        elif self.balance - amount < self.minimum_balance:
            raise MinimumBalanceError("New balance would be below minimum balance")
        else:
            self.balance -= amount

    def apply_rate(self, return_rate: float):
        self.balance *= (1 + return_rate)
    
    def details(self):
        super().details()
        print(f"Minimum Balance: ${self.minimum_balance:.2f}")
        print("-" * 25)

# Bank class
class Bank:
    def __init__(self) -> None:
        self.accounts = []
        # unique id numbers starting at 1 and increasing by 1
        self.checking_number = 1
        self.savings_number = 1
        self.investment_number = 1

    def open_checking_account(self, name: str, balance: float, overdraft_limit: float = 500):
        number = f"CHK-{self.checking_number:05d}"
        account = CheckingAccount(name, number, balance, overdraft_limit)
        self.accounts.append(account)
        self.checking_number += 1
        return account
    
    def open_savings_account(self, name: str, balance: float, interest_rate: float = 0.025, withdraws_limit: int = 3,
    withdraws_used: int = 0):
        number = f"SAV-{self.savings_number:05d}"
        account = SavingsAccount(name, number, balance, interest_rate, withdraws_limit, withdraws_used)
        self.accounts.append(account)
        self.savings_number += 1
        return account
    
    def open_investment_account(self, name: str, balance: float, minimum_balance: float):
        number = f"INV-{self.investment_number:05d}"
        account = InvestmentAccount(name, number, balance, minimum_balance)
        self.accounts.append(account)
        self.investment_number += 1
        return account

    def find_account(self, number: str):
        for account in self.accounts:
            if account.number == number:
                return account
        return None

# outer loop for main menu
bank = Bank()

while True:
    print("=" * 25)
    print("   Welcome to PyBank CLI")
    print("=" * 25, "\n")
    print("[1] Open a new account")
    print("[2] Select an acccoutn")
    print("[3] List all accounts")
    print("[4] Quit")

    while True:
        try:    
            option = int(input("Select: "))
            if 1 <= option <= 4:
                break
            else:
                print("Invalid input. Try again.")
        except ValueError:
            print("Invalid input. Try again.") 

    match option:
        case 1: # add account
            print("Account type:")
            print("[1] Checking")
            print("[2] Savings")
            print("[3] Investment")

            while True:
                try:    
                    option = int(input("Select: "))
                    if 1 <= option <= 3:
                        break
                    else:
                        print("Invalid input. Try again.")
                except ValueError:
                    print("Invalid input. Try again.") 

            match option:
                case 1: # checking 
                    name = input("Owner name: ")
                    while True:
                        try:
                            balance = float(input("Opening balance: "))
                            if balance < 0:
                                print("Please enter at least $0.01")
                            else:
                                break
                        except ValueError:
                            print("Invalid amount. Try again.") 
                    c_account: CheckingAccount = bank.open_checking_account(name, balance)
                    print(f"Checking account opened for {c_account.name}.")
                    print(f"   Account #: {c_account.number}  |  Balance: ${c_account.balance:.2f}")

                case 2: # savings
                    name = input("Owner name: ")
                    while True:
                        try:
                            balance = float(input("Opening balance: "))
                            if balance < 0:
                                print("Please enter at least $0.01")
                            else:
                                break
                        except ValueError:
                            print("Invalid amount. Try again.") 
                    s_account: SavingsAccount = bank.open_savings_account(name, balance)
                    print(f"Savings account opened for {s_account.name}.")
                    print(f"   Account #: {s_account.number}  |  Balance: ${s_account.balance:.2f}")
                
                case 3: # investment
                    name = input("Owner name: ")
                    while True:
                        try:
                            minimum_balance = float(input("Minimum balance: "))
                            if minimum_balance < 0:
                                print("Please enter at least $0.01")
                            else:
                                break
                        except ValueError:
                            print("Invalid amount. Try again.")
                    while True:
                        try:
                            balance = float(input("Opening Balance: "))
                            if balance < minimum_balance:
                                print(f"Please enter at least ${minimum_balance:.2f}")
                            else:
                                break
                        except ValueError:
                            print("Invalid entry.")
                    i_account: InvestmentAccount = bank.open_investment_account(name, balance, minimum_balance)
                    print(f"Investment account opened for {i_account.name}.")
                    print(f"   Account #: {i_account.number}  |  Balance: ${i_account.balance:.2f}")
        
        case 2: # select account
            number = input("Enter account number (ex: ABC-12345): ")
            account= bank.find_account(number)
            if account:
                print(f"Account selected: {account.name} ({account.number})")
                match account:
                    case CheckingAccount():
                        while True:
                            print("[1] Deposit")
                            print("[2] Withdraw")
                            print("[3] View Details")
                            print("[4] Back to Main Menu")

                            while True:
                                try:
                                    option = int(input("Select: "))
                                    if 1 <= option <= 4:
                                        break
                                    else:
                                        print("Invalid option.")
                                except ValueError:
                                    print("Invalid option.")
                            
                            match option:
                                case 1: # deposit
                                    while True:
                                        try:
                                            amount = float(input("Deposit amount: "))
                                        except ValueError:
                                            print("Invalid amount. Try again.")
                                            continue
                                        try:
                                            account.deposit(amount)
                                            print(f"Deposited ${amount:.2f}. New balance: ${account.balance:.2f}")
                                            break
                                        except ValueError as e:
                                            print(f"Error: {e}")

                                case 2: # withdraw
                                    while True:
                                        try:
                                            amount = float(input("Withdrawal amount: "))
                                        except ValueError:
                                            print("Invalid amount. Try again.")
                                            continue
                                        try:
                                            account.withdraw(amount)
                                            print(f"Withdrew ${amount:.2f}. New balance: ${account.balance:.2f}")
                                            break
                                        except (ValueError, InsufficientFundsError) as e:
                                            print(f"Error: {e}")
                                            break

                                case 3: # view details
                                    account.details()

                                case 4: # back to main menu
                                    break

                    case SavingsAccount():
                        while True:
                            print("[1] Deposit")
                            print("[2] Withdraw")
                            print("[3] Apply Monthly Interest")
                            print("[4] View Details")
                            print("[5] Back to Main Menu")

                            while True:
                                try:
                                    option = int(input("Select: "))
                                    if 1 <= option <= 5:
                                        break
                                    else:
                                        print("Invalid option.")
                                except ValueError:
                                    print("Invalid option.")

                            match option:
                                case 1: # deposit
                                    while True:
                                        try:
                                            amount = float(input("Deposit amount: "))
                                        except ValueError:
                                            print("Invalid amount. Try again.")
                                            continue
                                        try:
                                            account.deposit(amount)
                                            print(f"Deposited ${amount:.2f}. New balance: ${account.balance:.2f}")
                                            break
                                        except ValueError as e:
                                            print(f"Error: {e}")

                                case 2: # withdraw
                                    while True:
                                        try:
                                            amount = float(input("Withdrawal amount: "))
                                        except ValueError:
                                            print("Invalid amount. Try again.")
                                            continue
                                        try:
                                            account.withdraw(amount)
                                            print(f"Withdrew ${amount:.2f}. New balance: ${account.balance:.2f}")
                                            break
                                        except (ValueError, WithdrawsUsedError, InsufficientBalanceError) as e:
                                            print(f"Error: {e}")
                                            break

                                case 3: # apply monthly interest
                                    account.apply_interest()
                                    print(f"Applied monthly interest ({account.interest_rate * 100}%). New balance: ${account.balance:.2f}")

                                case 4: # view details
                                    account.details()

                                case 5: # back to main menu
                                    break

                    case InvestmentAccount():
                        while True:
                            print("[1] Deposit")
                            print("[2] Withdraw")
                            print("[3] Apply Return Rate")
                            print("[4] View Details")
                            print("[5] Back to Main Menu")

                            while True:
                                try:
                                    option = int(input("Select: "))
                                    if 1 <= option <= 5:
                                        break
                                    else:
                                        print("Invalid option.")
                                except ValueError:
                                    print("Invalid option.")

                            match option:
                                case 1: # deposit
                                    while True:
                                        try:
                                            amount = float(input("Deposit amount: "))
                                        except ValueError:
                                            print("Invalid amount. Try again.")
                                            continue
                                        try:
                                            account.deposit(amount)
                                            print(f"Deposited ${amount:.2f}. New balance: ${account.balance:.2f}")
                                            break
                                        except ValueError as e:
                                            print(f"Error: {e}")

                                case 2: # withdraw
                                    while True:
                                        try:
                                            amount = float(input("Withdrawal amount: "))
                                        except ValueError:
                                            print("Invalid amount. Try again.")
                                            continue
                                        try:
                                            account.withdraw(amount)
                                            print(f"Withdrew ${amount:.2f}. New balance: ${account.balance:.2f}")
                                            break
                                        except (ValueError, MinimumBalanceError) as e:
                                            print(f"Error: {e}")
                                            break

                                case 3: # apply return rate
                                    while True:
                                        try:
                                            return_rate = float(input("Return rate (ex: 0.05 for 5%): "))
                                            break
                                        except ValueError:
                                            print("Invalid rate. Try again.")
                                    account.apply_rate(return_rate)
                                    print(f"Applied return rate ({return_rate * 100}%). New balance: ${account.balance:.2f}")

                                case 4: # view details
                                    account.details()

                                case 5: # back to main menu
                                    break

            else:
                print(f"No account with number: {number}")
        
        case 3: # list all accounts
            if not bank.accounts:
                print("No accounts have been opened yet.")
            else:
                print("=" * 25)
                print(f"   All Accounts ({len(bank.accounts)})")
                for account in bank.accounts:
                    account.details()

        case 4: 
            print("Goodbye!")
            break
