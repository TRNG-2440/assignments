import json
from datetime import datetime


class Account:
    def __init__(self, owner, account_number, balance, username, password):
        self.owner = owner
        self.account_number = account_number
        self._balance = balance
        self.username = username
        self.password = password
        self.transaction_history = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        self._balance += amount
        self.add_transaction(f"Deposited ${amount}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        if amount > self._balance:
            raise ValueError("Insufficient funds.")

        self._balance -= amount
        self.add_transaction(f"Withdrew ${amount}")

    def get_balance(self):
        return self._balance

    def add_transaction(self, message):
        date_time = datetime.now()
        transaction = f"{date_time}: {message}"
        self.transaction_history.append(transaction)

    def show_history(self):
        if not self.transaction_history:
            print("No transaction history.")
        else:
            for transaction in self.transaction_history:
                print(transaction)

    def get_account_type(self):
        return "Account"

    def show_details(self):
        print(f"Owner: {self.owner}")
        print(f"Account Number: {self.account_number}")
        print(f"Account Type: {self.get_account_type()}")
        print(f"Balance: ${self._balance}")

    def monthly_reset(self):
        self.add_transaction("Monthly reset completed.")

    def to_dict(self):
        return {
            "type": self.get_account_type(),
            "owner": self.owner,
            "account_number": self.account_number,
            "balance": self._balance,
            "username": self.username,
            "password": self.password,
            "transaction_history": self.transaction_history
        }


class CheckingAccount(Account):
    def __init__(self, owner, account_number, balance, username, password, overdraft_limit=100):
        super().__init__(owner, account_number, balance, username, password)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        if amount > self._balance + self.overdraft_limit:
            raise ValueError("Overdraft limit reached.")

        self._balance -= amount
        self.add_transaction(f"Withdrew ${amount}")

    def get_account_type(self):
        return "Checking"

    def show_details(self):
        super().show_details()
        print(f"Overdraft Limit: ${self.overdraft_limit}")

    def to_dict(self):
        data = super().to_dict()
        data["overdraft_limit"] = self.overdraft_limit
        return data


class SavingsAccount(Account):
    def __init__(self, owner, account_number, balance, username, password, withdraw_limit=500, monthly_limit=3):
        super().__init__(owner, account_number, balance, username, password)
        self.withdraw_limit = withdraw_limit
        self.monthly_limit = monthly_limit
        self.withdrawals_this_month = 0

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        if amount > self.withdraw_limit:
            raise ValueError("Withdraw limit exceeded.")

        if self.withdrawals_this_month >= self.monthly_limit:
            raise ValueError("Monthly withdrawal limit reached.")

        if amount > self._balance:
            raise ValueError("Insufficient funds.")

        self._balance -= amount
        self.withdrawals_this_month += 1
        self.add_transaction(f"Withdrew ${amount}")

    def apply_interest(self, rate):
        if rate <= 0:
            raise ValueError("Rate must be greater than 0.")

        interest = self._balance * rate
        self._balance += interest
        self.add_transaction(f"Added interest ${interest}")

    def monthly_reset(self):
        self.withdrawals_this_month = 0
        self.add_transaction("Monthly withdrawal count reset.")

    def get_account_type(self):
        return "Savings"

    def show_details(self):
        super().show_details()
        print(f"Withdraw Limit: ${self.withdraw_limit}")
        print(f"Withdrawals This Month: {self.withdrawals_this_month}/{self.monthly_limit}")

    def to_dict(self):
        data = super().to_dict()
        data["withdraw_limit"] = self.withdraw_limit
        data["monthly_limit"] = self.monthly_limit
        data["withdrawals_this_month"] = self.withdrawals_this_month
        return data


class InvestmentAccount(Account):
    def __init__(self, owner, account_number, balance, username, password, minimum_balance=100):
        super().__init__(owner, account_number, balance, username, password)
        self.minimum_balance = minimum_balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        if self._balance - amount < self.minimum_balance:
            raise ValueError("Minimum balance required.")

        self._balance -= amount
        self.add_transaction(f"Withdrew ${amount}")

    def apply_return(self, rate):
        if rate <= 0:
            raise ValueError("Rate must be greater than 0.")

        return_amount = self._balance * rate
        self._balance += return_amount
        self.add_transaction(f"Added investment return ${return_amount}")

    def get_account_type(self):
        return "Investment"

    def show_details(self):
        super().show_details()
        print(f"Minimum Balance: ${self.minimum_balance}")

    def to_dict(self):
        data = super().to_dict()
        data["minimum_balance"] = self.minimum_balance
        return data


class Bank:
    def __init__(self):
        self.accounts = []
        self.next_account_number = 1

    def generate_account_number(self):
        account_number = f"ACC-{self.next_account_number}"
        self.next_account_number += 1
        return account_number

    def username_exists(self, username):
        for account in self.accounts:
            if account.username == username:
                return True
        return False

    def create_account(self, account_type, owner, balance, username, password):
        if balance < 0:
            raise ValueError("Starting balance cannot be negative.")

        if self.username_exists(username):
            raise ValueError("Username already exists.")

        account_number = self.generate_account_number()

        if account_type == "1":
            account = CheckingAccount(owner, account_number, balance, username, password)
        elif account_type == "2":
            account = SavingsAccount(owner, account_number, balance, username, password)
        elif account_type == "3":
            account = InvestmentAccount(owner, account_number, balance, username, password)
        else:
            raise ValueError("Invalid account type.")

        account.add_transaction("Account created.")
        self.accounts.append(account)
        return account

    def login(self, username, password):
        for account in self.accounts:
            if account.username == username and account.password == password:
                return account
        return None

    def find_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None

    def list_accounts(self):
        if not self.accounts:
            print("No accounts found.")
        else:
            for account in self.accounts:
                print(f"{account.account_number} | {account.owner} | {account.get_account_type()} | ${account.get_balance()}")

    def transfer(self, from_account, to_account_number, amount):
        to_account = self.find_account(to_account_number)

        if to_account is None:
            raise ValueError("Destination account not found.")

        if from_account.account_number == to_account.account_number:
            raise ValueError("Cannot transfer to the same account.")

        from_account.withdraw(amount)
        to_account.deposit(amount)

        from_account.add_transaction(f"Transferred ${amount} to {to_account.account_number}")
        to_account.add_transaction(f"Received ${amount} from {from_account.account_number}")

    def monthly_reset_all(self):
        for account in self.accounts:
            if isinstance(account, SavingsAccount):
                account.apply_interest(0.025)
                account.monthly_reset()
            elif isinstance(account, InvestmentAccount):
                account.apply_return(0.05)
                account.monthly_reset()
            else:
                account.monthly_reset()

    def save_accounts(self):
        data = {
            "next_account_number": self.next_account_number,
            "accounts": []
        }

        for account in self.accounts:
            data["accounts"].append(account.to_dict())

        with open("accounts.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_accounts(self):
        try:
            with open("accounts.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return

        self.next_account_number = data["next_account_number"]

        for item in data["accounts"]:
            if item["type"] == "Checking":
                account = CheckingAccount(
                    item["owner"],
                    item["account_number"],
                    item["balance"],
                    item["username"],
                    item["password"],
                    item["overdraft_limit"]
                )

            elif item["type"] == "Savings":
                account = SavingsAccount(
                    item["owner"],
                    item["account_number"],
                    item["balance"],
                    item["username"],
                    item["password"],
                    item["withdraw_limit"],
                    item["monthly_limit"]
                )
                account.withdrawals_this_month = item["withdrawals_this_month"]

            elif item["type"] == "Investment":
                account = InvestmentAccount(
                    item["owner"],
                    item["account_number"],
                    item["balance"],
                    item["username"],
                    item["password"],
                    item["minimum_balance"]
                )

            account.transaction_history = item["transaction_history"]
            self.accounts.append(account)


def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Enter a valid number.")


def create_account(bank):
    print("\n1. Checking")
    print("2. Savings")
    print("3. Investment")

    account_type = input("Choose account type: ")
    owner = input("Owner name: ")
    username = input("Create username: ")
    password = input("Create password: ")
    balance = get_float("Starting balance: ")

    try:
        account = bank.create_account(account_type, owner, balance, username, password)
        bank.save_accounts()
        print("Account created!")
        print(f"Account number: {account.account_number}")
    except ValueError as error:
        print(error)


def login(bank):
    username = input("Username: ")
    password = input("Password: ")

    account = bank.login(username, password)

    if account is None:
        print("Invalid login.")
    else:
        print(f"Welcome {account.owner}!")
        account_menu(bank, account)


def main_menu_transfer(bank):
    username = input("Username: ")
    password = input("Password: ")

    from_account = bank.login(username, password)

    if from_account is None:
        print("Invalid login.")
        return

    to_account = input("Account number to transfer to: ")
    amount = get_float("Transfer amount: ")

    try:
        bank.transfer(from_account, to_account, amount)
        bank.save_accounts()
        print("Transfer complete.")
    except ValueError as error:
        print(error)


def account_menu(bank, account):
    while True:
        print("\n1. View details")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. View history")

        if isinstance(account, SavingsAccount):
            print("6. Apply interest")
        elif isinstance(account, InvestmentAccount):
            print("6. Apply investment return")
        elif isinstance(account, CheckingAccount):
            print("6. View overdraft limit")
        else:
            print("6. Special account action")

        print("7. Monthly reset")
        print("0. Logout")

        choice = input("Choose an option: ")

        try:
            if choice == "1":
                account.show_details()

            elif choice == "2":
                amount = get_float("Deposit amount: ")
                account.deposit(amount)
                bank.save_accounts()
                print("Deposit complete.")

            elif choice == "3":
                amount = get_float("Withdraw amount: ")
                account.withdraw(amount)
                bank.save_accounts()
                print("Withdraw complete.")

            elif choice == "4":
                to_account = input("Account number to transfer to: ")
                amount = get_float("Transfer amount: ")
                bank.transfer(account, to_account, amount)
                bank.save_accounts()
                print("Transfer complete.")

            elif choice == "5":
                account.show_history()

            elif choice == "6":
                special_action(account)
                bank.save_accounts()

            elif choice == "7":
                account.monthly_reset()
                bank.save_accounts()
                print("Monthly reset complete.")

            elif choice == "0":
                print("Logged out.")
                break

            else:
                print("Invalid choice.")

        except ValueError as error:
            print(error)


def special_action(account):
    if isinstance(account, SavingsAccount):
        rate = get_float("Interest rate, like 0.05 for 5%: ")
        account.apply_interest(rate)
        print("Interest added.")

    elif isinstance(account, InvestmentAccount):
        rate = get_float("Return rate, like 0.08 for 8%: ")
        account.apply_return(rate)
        print("Return added.")

    elif isinstance(account, CheckingAccount):
        print(f"Overdraft limit: ${account.overdraft_limit}")

    else:
        print("No special action.")


def main():
    bank = Bank()
    bank.load_accounts()

    while True:
        print("\n===== Bank System =====")
        print("1. Create Account")
        print("2. Login")
        print("3. List All Accounts")
        print("4. Transfer")
        print("5. Monthly Reset Simulation")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_account(bank)

        elif choice == "2":
            login(bank)

        elif choice == "3":
            bank.list_accounts()

        elif choice == "4":
            main_menu_transfer(bank)

        elif choice == "5":
            bank.monthly_reset_all()
            bank.save_accounts()
            print("Monthly reset simulation complete.")

        elif choice == "0":
            bank.save_accounts()
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


main()
