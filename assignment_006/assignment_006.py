class BankError(Exception):
    pass

class InvalidAmountError(Exception):
    pass

class AccountNotFoundError(Exception):
    pass

class AccountTypeError(Exception):
    pass

class WithdrawalLimitError(Exception):
    pass

class MinimumBalanceError(Exception):
    pass

class Account:
    account_type = "Basic Account"

    #encapsulation??
    account_running_count = 1

    def __init__ (self, name, balance=0.00):
        self.name = name
        self.balance = balance
        self.account_number = self.create_account_number()

    def create_account_number(self):
        number = f"ACC-{Account.account_running_count:05d}"
        Account.account_running_count += 1
        return number

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Deposit must be a positive amount.")
        
        self.balance += amount
        print(f"Deposited ${amount:.2f}. New balance: {self.balance:.2f}.")

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Withdrawal must be a positive amount.")
        
        if amount > self.balance:
            raise WithdrawalLimitError(f"You do not have enough funds to withdraw ${amount:.2f}.")
        
        self.balance -= amount
        print(f"Withdrew ${amount:.2f}. New balance: {self.balance:.2f}")
 

    def get_balance(self):
        return self.balance
    
    def display_account_details(self):
        print("------------------------------")
        print("Account Details")
        print("------------------------------")
        print(f"Account Name    : {self.name}")
        print(f"Account Number  : {self.account_number}")
        print(f"Type            : {self.account_type}")
        print(f"Balance         : ${self.balance:.2f}")
        print("------------------------------")

#inheritance
class CheckingAccount(Account):
    account_type = "Checking"

    overdraft_limit = 500.00

    def __init__ (self, name, balance = 0.00):
        super().__init__(name, balance)
    
    def create_account_number(self):
        number = f"CHK-{Account.account_running_count:05d}"
        Account.account_running_count += 1
        return number

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Withdrawal must be a positive amount.")
        
        max_withdraw_available = self.balance + self.overdraft_limit

        if amount > max_withdraw_available:
            raise WithdrawalLimitError(f"Overdraft limit exceeded. Max you can withdraw is ${max_withdraw_available:.2f}.")
        
        self.balance -= amount
        print(f"Withdrew ${amount:.2f}. New balance: {self.balance:.2f}")

    def display_account_details(self):
        print("------------------------------")
        print("Account Details")
        print("------------------------------")
        print(f"Account Name    : {self.name}")
        print(f"Account Number  : {self.account_number}")
        print(f"Type            : {self.account_type}")
        print(f"Balance         : ${self.balance:.2f}")
        print(f"Overdraft limit : ${self.overdraft_limit:.2f}")
        print("------------------------------")
    
#inheritance    
class SavingsAccount(Account):
    account_type = "Savings"

    interest_rate = 0.025
    withdrawal_limit = 3

    def __init__ (self, name, balance = 0.00):
        super().__init__(name, balance)
        self.number_of_withdrawal = 0

    def create_account_number(self):
        number = f"SAV-{Account.account_running_count:05d}"
        Account.account_running_count += 1
        return number
    
    # polymorphism
    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Withdrawal must be a positive amount.")
        
        if amount > self.balance:
            raise WithdrawalLimitError(f"You do not have enough funds to withdraw ${amount:.2f}.")
        
        if self.number_of_withdrawal >= self.withdrawal_limit:
            raise WithdrawalLimitError(f"Monthly withdrawal limit reached ({self.number_of_withdrawal}/{self.withdrawal_limit} used). Try again next month.")
        
        self.balance -= amount
        self.number_of_withdrawal += 1
        print(f"Withdrew ${amount:.2f}. New balance: {self.balance:.2f}")
        print(f"Withdrawals left: {self.withdrawal_limit - self.number_of_withdrawal}")

    def apply_interest(self):
        self.balance = self.balance + self.balance * self.interest_rate 
        print(f"Interest rate of {self.interest_rate * 100:.1f}% has been applied.")
        print(f"New balance: ${self.balance:.2f}")

    def display_account_details(self):
        print("------------------------------")
        print("Account Details")
        print("------------------------------")
        print(f"Account Name    : {self.name}")
        print(f"Account Number  : {self.account_number}")
        print(f"Type            : {self.account_type}")
        print(f"Balance         : ${self.balance:.2f}")
        print(f"Withdrawals     : {self.number_of_withdrawal}/{self.withdrawal_limit} used this month")
        print(f"Interest rate   : {self.interest_rate * 100:.1f}%")
        print("------------------------------")
    
class InvestmentAccount(Account):
    account_type = "Investment"

    minimum_balance = 500.00
    return_rate = 0.05

    def __init__(self, name, balance=0.00):
        super().__init__(name, balance)
    
    def create_account_number(self):
        number = f"INV-{Account.account_running_count:05d}"
        Account.account_running_count += 1
        return number

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Withdrawal must be a positive amount.")
        
        if amount > self.balance:
            raise WithdrawalLimitError(f"You do not have enough funds to withdraw ${amount:.2f}.")
        
        if amount > self.balance - self.minimum_balance:
            raise WithdrawalLimitError(f"You must have a minimum of ${self.minimum_balance:.2f} remaining.")
        
        self.balance -= amount
        print(f"Withdrew ${amount:.2f}. New balance: {self.balance:.2f}")

    def apply_return_rate(self, rate=None):
        if rate is None:
            rate = self.return_rate

        if rate < -1:
            raise InvalidAmountError("Return rate cannot reduce balance below zero.")

        self.balance += self.balance * rate
        print(f"Applied return rate ({rate * 100:.1f}%). New balance: ${self.balance:.2f}")

    def display_account_details(self):
        print("------------------------------")
        print("Account Details")
        print("------------------------------")
        print(f"Account Name    : {self.name}")
        print(f"Account Number  : {self.account_number}")
        print(f"Type            : {self.account_type}")
        print(f"Balance         : ${self.balance:.2f}")
        print(f"Return rate     : {self.return_rate * 100:.1f}%")
        print("------------------------------")
        
class Bank:
    def __init__(self):
        self.accounts = {}

    def open_account(self, account_type, name, balance=0.00):
        account_type = account_type.lower()

        if account_type == "checking":
            account = CheckingAccount(name, balance)
        elif account_type == "savings":
            account = SavingsAccount(name, balance)
        elif account_type == "investment":
            account = InvestmentAccount(name, balance)
        else:
            raise BankError("Unsupported bank account type.")

        self.accounts[account.account_number] = account
        return account
    
    def find_account(self, account_number):
        if account_number not in self.accounts:
            raise AccountNotFoundError(f"Account {account_number} was not found.")
        return self.accounts[account_number]
    
    def list_accounts(self):
        if not self.accounts:
            print ("No accounts have been opened yet.")
            return
        for account in self.accounts.values():
            print(f"{account.account_number} | {account.name} | {account.account_type} | ${account.balance:.2f}")

def show_main_menu():
    print()
    print("════════════════════════════════════════")
    print("   Welcome to PyBank CLI")
    print("════════════════════════════════════════")
    print("[1] Open a new account")
    print("[2] Select an account")
    print("[3] List all accounts")
    print("[4] Exit")


def show_open_account_menu():
    print()
    print("Account type:")
    print("[1] Checking")
    print("[2] Savings")
    print("[3] Investment")
    print("[4] Back")


def show_checking_menu():
    print()
    print("[1] Deposit")
    print("[2] Withdraw")
    print("[3] View Details")
    print("[4] Back to Main Menu")


def show_savings_menu():
    print()
    print("[1] Deposit")
    print("[2] Withdraw")
    print("[3] Apply Monthly Interest")
    print("[4] View Details")
    print("[5] Back to Main Menu")


def show_investment_menu():
    print()
    print("[1] Deposit")
    print("[2] Withdraw")
    print("[3] Apply Return Rate")
    print("[4] View Details")
    print("[5] Back to Main Menu")

main_menu = True
bank = Bank()

while main_menu:
    try:
        show_main_menu()
        choice = int(input("> "))

        match choice:
            case 1:
                show_open_account_menu()
                account_type = int(input("> "))

                match account_type:
                    case 1:
                        name = input("Owner name: ").strip()
                        balance = float(input("Opening balance: $"))
                        account = bank.open_account("checking", name, balance)
                        print(f"Checking account opened for {account.name}. Account #: {account.account_number} | Balance: ${account.balance:.2f}")

                    case 2:
                        name = input("Owner name: ").strip()
                        balance = float(input("Opening balance: $"))
                        account = bank.open_account("savings", name, balance)
                        print(f"Savings account opened for {account.name}. Account #: {account.account_number} | Balance: ${account.balance:.2f}")

                    case 3:
                        name = input("Owner name: ").strip()
                        balance = float(input("Opening balance: $"))
                        account = bank.open_account("investment", name, balance)
                        print(f"Investment account opened for {account.name}. Account #: {account.account_number} | Balance: ${account.balance:.2f}")

                    case 4:
                        continue

                    case _:
                        print("Invalid account type selection.")

            case 2:
                account_number = input("Enter account number: ").strip()
                selected_account = bank.find_account(account_number)
                print(f"Account selected: {selected_account.name} ({selected_account.account_number})")

                while True:
                    try:
                        if selected_account.account_type == "Checking":
                            show_checking_menu()
                            decision = int(input("> "))

                            match decision:
                                case 1:
                                    amount = float(input("Deposit amount: $"))
                                    selected_account.deposit(amount)
                                case 2:
                                    amount = float(input("Withdraw amount: $"))
                                    selected_account.withdraw(amount)
                                case 3:
                                    selected_account.display_account_details()
                                case 4:
                                    break
                                case _:
                                    print("Invalid selection.")

                        elif selected_account.account_type == "Savings":
                            show_savings_menu()
                            decision = int(input("> "))

                            match decision:
                                case 1:
                                    amount = float(input("Deposit amount: $"))
                                    selected_account.deposit(amount)
                                case 2:
                                    amount = float(input("Withdraw amount: $"))
                                    selected_account.withdraw(amount)
                                case 3:
                                    selected_account.apply_interest()
                                case 4:
                                    selected_account.display_account_details()
                                case 5:
                                    break
                                case _:
                                    print("Invalid selection.")

                        elif selected_account.account_type == "Investment":
                            show_investment_menu()
                            decision = int(input("> "))

                            match decision:
                                case 1:
                                    amount = float(input("Deposit amount: $"))
                                    selected_account.deposit(amount)
                                case 2:
                                    amount = float(input("Withdraw amount: $"))
                                    selected_account.withdraw(amount)
                                case 3:
                                    rate = float(input("Enter return rate (%): ")) / 100
                                    selected_account.apply_return_rate(rate)
                                case 4:
                                    selected_account.display_account_details()
                                case 5:
                                    break
                                case _:
                                    print("Invalid selection.")

                    except (InvalidAmountError, WithdrawalLimitError, MinimumBalanceError, ValueError) as e:
                        print(f"Error: {e}")

            case 3:
                bank.list_accounts()

            case 4:
                print("Goodbye!")
                break

            case _:
                print("Invalid menu option.")

    except (ValueError, AccountNotFoundError, BankError) as e:
        print(f"Error: {e}")