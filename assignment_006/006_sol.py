#Solution to  assignment 6

#PyBank Bank Account System
#Alex Tran


#Create errror classes
class BankingError(Exception):
    pass


class InvalidAmountError(Exception):
    pass


#Create account class from which the other accounts will inherit from it
class Account:
    def __init__(self, owner, account_number, balance = 0):
        if balance < 0:
            raise InvalidAmountError("Opening balance cannot be less than 0.")
        
        self.owner = owner
        self.account_number = account_number
        self._balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be greater than zero.")
        
        self.balance += amount
        print(f"You deposited {amount:.2f}.")
        print(f"New Balance: ${self._balance:.2f}")

    def withdraw(self, amount):
        if amount <=0:
            raise InvalidAmountError("Opening balance cannot be less than 0.")
        if amount > self._balance:
            raise BankingError("Insufficient funds.")
        self._balance -= amount
        print(f"Withdrew ${amount:.2f}")
        print(f"Current balance: {self._balance:.2f}")

    def display_details(self):
        print("*" * 20)
        print("Account Details")
        print("*" * 20)
        print(f"Owner   : {self.owner} ")
        print(f"Account #   : {self.account_number} ")
        print(f"Type   : General ")
        print(f"Balance   : ${self._balance} ")
        print("*" * 20)

#create class for checking account
class CheckingAccount(Account):
    def __init__(self, owner, account_number, balance=0, overdraft_limit = 200):
        super().__init__(owner, account_number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <=0:
            raise InvalidAmountError("Opening balance cannot be less than 0.")
        
        if amount > self.balance + self.overdraft_limit:
            raise BankingError("Overdraft limit exceeded")
        
        self._balance -= amount
        print(f"Withdrew ${amount:.2f}")
        print(f"Current balance: {self._balance:.2f}")
    
    def display_details(self):
        print("*" * 20)
        print("Account Details")
        print("*" * 20)
        print(f"Owner   : {self.owner} ")
        print(f"Account #   : {self.account_number} ")
        print(f"Type   : Checking ")
        print(f"Balance   : ${self._balance} ")
        print("*" * 20)

class SavingsAccount(Account):
    def __init__(self, owner, account_number, balance=0, interest_rate = 0.03, withdrawal_limit = 3):
        super().__init__(owner, account_number, balance)
        self.interest_rate = interest_rate
        self.withdrawal_limit = withdrawal_limit
        self.withdrawals = 0
    
    def withdraw(self, amount):
        
        if self.withdrawals >= self.withdrawal_limit:
            raise BankingError(
                f"Monthly withdrawal limit reached"
                f"({self.withdrawals}/{self.withdrawal_limit} used.)"
            )
        
        super().withdraw(amount)
        self.withdrawals +=1

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self._balance += interest
        print(
            f"Applied monthly interest ({self.interest_rate * 100:.1f}%). "
            f"New balance: ${self._balance:.2f}"
        )
    

    def display_details(self):
        print("*" * 20)
        print("Account Details")
        print("*" * 20)
        print(f"Owner   : {self.owner} ")
        print(f"Account #   : {self.account_number} ")
        print(f"Type   : Savings ")
        print(f"Balance   : ${self._balance} ")
        print("*" * 20)



class InvestmentAccount(Account):
    def __init__(self, owner, account_number, balance=0, minimum_balance=500):
        super().__init__(owner, account_number, balance)
        self.minimum_balance = minimum_balance

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be greater than zero.")

        if self._balance - amount < self.minimum_balance:
            raise MinimumBalanceError(
                f"Withdrawal rejected. Balance cannot fall below "
                f"${self.minimum_balance:.2f}."
            )

        self._balance -= amount
        print(f"Withdrew ${amount:.2f}." 
              f"New balance: ${self._balance:.2f}")

    def apply_return(self, rate):
        self._balance += self._balance * rate
        print(
            f"Applied investment return ({rate * 100:.1f}%). "
            f"New balance: ${self._balance:.2f}"
        )



#Bank class which is interfaced to create accounts
class Bank:
    def __init__(self):
        self.accounts = {}
        self.next_number = 1

    def generate_account_number(self, prefix):
        account_number = f"{prefix}-{self.next_number:05d}"
        self.next_number += 1
        return account_number

    def open_account(self, account_type, owner, balance):
        if account_type == "1":
            account_number = self.generate_account_number("CHK")
            account = CheckingAccount(owner, account_number, balance)

        elif account_type == "2":
            account_number = self.generate_account_number("SAV")
            account = SavingsAccount(owner, account_number, balance)

        elif account_type == "3":
            account_number = self.generate_account_number("INV")
            account = InvestmentAccount(owner, account_number, balance)

        else:
            raise BankingError("Invalid account type.")

        self.accounts[account_number] = account
        print(f"\nAccount opened for {owner}.")
        print(f"Account #: {account_number} | Balance: ${balance:.2f}")

    def find_account(self, account_number):
        if account_number not in self.accounts:
            raise BankingError("Account not found.")

        return self.accounts[account_number]

    def list_accounts(self):
        if not self.accounts:
            print("No accounts found.")
            return

        for account in self.accounts.values():
            print(
                f"{account.account_number} | "
                f"{account.owner} | "
                f"${account._balance:.2f}"
            )

    
    def display_details(self):
        print("*" * 20)
        print("Account Details")
        print("*" * 20)
        print(f"Owner           : {self.owner}")
        print(f"Account #       : {self.account_number}")
        print(f"Type            : Investment")
        print(f"Balance         : ${self._balance:.2f}")
        print(f"Minimum Balance : ${self.minimum_balance:.2f}")
        print("*" * 20)



def get_amount(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        raise InvalidAmountError("Please enter a valid numeric amount.")


def account_menu(account):
    while True:
        print("\n[1] Deposit")
        print("[2] Withdraw")

        option_number = 3

        if isinstance(account, SavingsAccount):
            print(f"[{option_number}] Apply Monthly Interest")
            interest_option = str(option_number)
            option_number += 1
        else:
            interest_option = None

        if isinstance(account, InvestmentAccount):
            print(f"[{option_number}] Apply Investment Return")
            return_option = str(option_number)
            option_number += 1
        else:
            return_option = None

        print(f"[{option_number}] View Details")
        details_option = str(option_number)

        print(f"[{option_number + 1}] Back to Main Menu")
        back_option = str(option_number + 1)

        choice = input("> ")

        try:
            if choice == "1":
                amount = get_amount("Deposit amount: ")
                account.deposit(amount)

            elif choice == "2":
                amount = get_amount("Withdrawal amount: ")
                account.withdraw(amount)

            elif choice == interest_option:
                account.apply_interest()

            elif choice == return_option:
                rate = get_amount("Return rate as decimal, example 0.05 for 5%: ")
                account.apply_return(rate)

            elif choice == details_option:
                account.display_details()

            elif choice == back_option:
                break

            else:
                print("Invalid menu option.")

        except BankingError as error:
            print(f"Error: {error}")

def get_amount(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        raise InvalidAmountError("Please enter a valid numeric amount.")


def account_menu(account):
    while True:
        print("\n[1] Deposit")
        print("[2] Withdraw")

        option_number = 3

        if isinstance(account, SavingsAccount):
            print(f"[{option_number}] Apply Monthly Interest")
            interest_option = str(option_number)
            option_number += 1
        else:
            interest_option = None

        if isinstance(account, InvestmentAccount):
            print(f"[{option_number}] Apply Investment Return")
            return_option = str(option_number)
            option_number += 1
        else:
            return_option = None

        print(f"[{option_number}] View Details")
        details_option = str(option_number)

        print(f"[{option_number + 1}] Back to Main Menu")
        back_option = str(option_number + 1)

        choice = input("> ")

        try:
            if choice == "1":
                amount = get_amount("Deposit amount: ")
                account.deposit(amount)

            elif choice == "2":
                amount = get_amount("Withdrawal amount: ")
                account.withdraw(amount)

            elif choice == interest_option:
                account.apply_interest()

            elif choice == return_option:
                rate = get_amount("Return rate as decimal, example 0.05 for 5%: ")
                account.apply_return(rate)

            elif choice == details_option:
                account.display_details()

            elif choice == back_option:
                break

            else:
                print("Invalid menu option.")

        except BankingError as error:
            print(f"Error: {error}")


def main():
    bank = Bank()

    while True:
        print("\n==============================")
        print("   Welcome to PyBank CLI")
        print("==============================")
        print("[1] Open a new account")
        print("[2] Select an account")
        print("[3] List all accounts")
        print("[4] Quit")

        choice = input("> ")

        try:
            if choice == "1":
                print("\nAccount type:")
                print("[1] Checking")
                print("[2] Savings")
                print("[3] Investment")

                account_type = input("> ")
                owner = input("Owner name: ")
                balance = get_amount("Opening balance: ")

                bank.open_account(account_type, owner, balance)

            elif choice == "2":
                account_number = input("Enter account number: ")
                account = bank.find_account(account_number)

                print(f"\nAccount selected: {account.owner} ({account.account_number})")
                account_menu(account)

            elif choice == "3":
                bank.list_accounts()

            elif choice == "4":
                print("Thank you for using PyBank CLI.")
                break

            else:
                print("Invalid menu option.")

        except BankingError as error:
            print(f"Error: {error}")


main()