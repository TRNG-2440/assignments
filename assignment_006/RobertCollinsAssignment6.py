class BankingError(Exception):
    pass

class InsufficientFundsError(BankingError):
    pass

class WithdrawalLimitError(BankingError):
    pass

class MinimumBalanceError(BankingError):
    pass

class Account:

    def __init__(self, owner, account_number, balance):
        self._owner = owner
        self._account_number = account_number
        self._balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
    
    def display_details(self):
        print(f"Owner: {self._owner}")
        print(f"Account #: {self._account_number}")
        print(f"Balance: ${self._balance:.2f}")

    
class CheckingAccount(Account):
    def __init__(self, owner, account_number, balance, overdraft_limit=500):
        super().__init__(owner, account_number, balance)
        self._overdraft_limit = overdraft_limit
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive.")
        elif self._balance - amount < -self._overdraft_limit:
            raise InsufficientFundsError("Overdraft limit exceeded.")
        else:
            self._balance -= amount
    
    def display_details(self):
        super().display_details()
        print(f"Overdraft Limit: ${self._overdraft_limit:.2f}")
        
class SavingsAccount(Account):

    def __init__(self, owner, account_number, balance, interest_rate, withdrawal_limit, withdrawals_used=0):
        super().__init__(owner, account_number, balance)
        self._interest_rate = interest_rate
        self._withdrawal_limit = withdrawal_limit
        self._withdrawals_used = withdrawals_used

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive.")
        elif self._withdrawals_used >= self._withdrawal_limit:
            raise WithdrawalLimitError("Monthly withdrawal limit reached.")
        elif amount > self._balance:
            raise InsufficientFundsError("Insufficient funds.")
        else:
            self._balance -= amount
            self._withdrawals_used += 1
    
    def apply_interest(self):
        self._balance *= (1 + self._interest_rate)

    def display_details(self):
        super().display_details()
        print(f"Interest Rate: {self._interest_rate * 100:.2f}%")
        print(f"Withdrawals Used: "f"{self._withdrawals_used}/{self._withdrawal_limit}")

class InvestmentAccount(Account):

    def __init__(self, owner, account_number, balance, minimum_balance):
        super().__init__(owner, account_number, balance)
        self._minimum_balance = minimum_balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive.")
        elif self._balance - amount < self._minimum_balance:
            raise MinimumBalanceError("Minimum balance requirement violated.")
        else:        
            self._balance -= amount

    def apply_return(self, rate):
        self._balance *= (1 + rate)

    def display_details(self):
        super().display_details()
        print(f"Minimum Balance: ${self._minimum_balance:.2f}")

class Bank:

    def __init__(self):
        self._accounts = []
        self._checking_count = 1
        self._savings_count = 1
        self._investment_count = 1

    def generate_checking_number(self):
        account_number = (f"CHK-{self._checking_count:05d}")
        self._checking_count += 1
        return account_number
    
    def open_checking_account(self,owner,balance):
        account_number = (self.generate_checking_number())
        account = CheckingAccount(owner,account_number,balance)
        self.add_account(account)
        return account

    def generate_savings_number(self):
        account_number = (f"SAV-{self._savings_count:05d}")
        self._savings_count += 1
        return account_number
    
    def open_savings_account(self, owner, balance):
        account_number = (self.generate_savings_number())
        account = SavingsAccount(owner,account_number,balance,0.025,3)
        self.add_account(account)
        return account
    
    def generate_investment_number(self):
        account_number = (f"INV-{self._investment_count:05d}")
        self._investment_count += 1
        return account_number

    def open_investment_account(self,owner,balance):
        account_number = (self.generate_investment_number())
        account = InvestmentAccount(owner,account_number,balance,100)
        self.add_account(account)
        return account

    def add_account(self, account):
        self._accounts.append(account)
    
    def find_account(self, account_number):
        for account in self._accounts:
            if str.lower(account._account_number) == str.lower(account_number):
                return account

        return None
    
    def list_accounts(self):
        for account in self._accounts:
            print(f"{account._account_number}"f" - ${account._balance:.2f}")

bank = Bank()

while True:

    print(f"\n{"===" * 10}\n\tPyBank\n{"===" * 10}\n1. Open Account\n2. Select Account\n3.List Accounts\n4. Quit")
    user_input = input("Select an option: \n")

    match user_input:
        case '1':
            print("What kind of account do you want to open?")
            account_type = int(input("1. Checking\n2. Savings\n3. Investment\n"))
            match account_type:
                case 1:
                    while True:
                        try:
                            owner = input("Owner name: ")
                            balance = float(input("Opening balance: \n"))
                            bank.open_checking_account(owner, balance)
                            print(f"Checking account opened for {owner}.")
                            break
                        except Exception:
                            print("Please enter a valid number for your opening balance.")

                case 2:
                    while True:
                        try:
                            owner = input("Owner name: ")
                            balance = float(input("Opening balance: \n"))
                            bank.open_savings_account(owner, balance)
                            print(f"Savings account opened for {owner}.")
                            break
                        except Exception:
                            print("Please enter a valid number for your opening balance.")

                case 3:
                    while True:
                        try:
                            owner = input("Owner name: ")
                            balance = float(input("Opening balance: \n"))
                            bank.open_investment_account(owner, balance)
                            print(f"Investment account opened for {owner}.")
                            break
                        except Exception:
                            print("Please enter a valid number for your opening balance.")

                case _:
                    print("Please input a valid account type.")

        case '2':
            account_number = input("Enter account number: \n")
            account = bank.find_account(account_number)
            if account is None:
                print("No account with that number found!")
            else:
                print(f"Account selected: {account._owner} {account._account_number}\n")
            
        case '3':
            bank.list_accounts()
        case '4':
            print("Thank you for banking with us!\n")
            break
        case _:
            print("User input must be an integer, please re-try.\n\n")
    
#test cases to make sure everything is running as expected before CLI Implementation
"""checking = bank.open_checking_account("Bob", 500)
savings = bank.open_savings_account("Alice", 1000)
investment = bank.open_investment_account("Charlie", 2500)

bank.list_accounts()

print()

checking.display_details()
print()
checking.withdraw(2000)

savings.display_details()
savings.withdraw(100)
savings.withdraw(100)
savings.withdraw(100)
savings.withdraw(100)
print()

investment.display_details()
investment.withdraw(2450)"""