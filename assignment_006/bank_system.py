# custom exception classes for banking-related erros
class BankError(Exception):
    pass


class InsufficientFundsError(BankError):
    pass


class WithdrawalLimitError(BankError):
    pass


class MinimumBalanceError(BankError):
    pass

# base account class shared by all account types
class Account:
    def __init__(self, owner, account_number, balance):
        self._owner = owner
        self._account_number = account_number
        self._balance = balance

    # add money to account 
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")

        self._balance += amount
        print(f"Deposited ${amount:.2f}. New balance: ${self._balance:.2f}")

    # display account info 
    def display_details(self):
        print("Account Details")
        print(f"Owner      : {self._owner}")
        print(f"Account #  : {self._account_number}")
        print(f"Balance    : ${self._balance:.2f}")


# checking account w/ overdarft limit
class CheckingAccount(Account):
    def __init__(self, owner, account_number, balance, overdraft_limit=200):
        super().__init__(owner, account_number, balance)
        self._overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")

        if amount > self._balance + self._overdraft_limit:
            raise InsufficientFundsError(
                f"Overdraft exceeded. Maximum available: ${self._balance + self._overdraft_limit:.2f}"
            )

        self._balance -= amount
        print(f"Withdrew ${amount:.2f}. New balance: ${self._balance:.2f}")

    def display_details(self):
        print("Checking Account")
        print(f"Owner            : {self._owner}")
        print(f"Account #        : {self._account_number}")
        print(f"Balance          : ${self._balance:.2f}")
        print(f"Overdraft Limit  : ${self._overdraft_limit:.2f}")


# savings account w/ interest and withdrawal limits
class SavingsAccount(Account):
    def __init__(
        self,
        owner,
        account_number,
        balance,
        interest_rate=0.025,
        withdrawal_limit=3,
    ):
        super().__init__(owner, account_number, balance)

        self._interest_rate = interest_rate
        self._withdrawal_limit = withdrawal_limit
        self._withdrawals_used = 0

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")

        if self._withdrawals_used >= self._withdrawal_limit:
            raise WithdrawalLimitError(
                f"Monthly withdrawal limit reached "
                f"({self._withdrawals_used}/{self._withdrawal_limit} used)."
            )

        if amount > self._balance:
            raise InsufficientFundsError("Insufficient funds.")

        self._balance -= amount
        self._withdrawals_used += 1

        print(f"Withdrew ${amount:.2f}. New balance: ${self._balance:.2f}")

    def apply_interest(self):
        interest = self._balance * self._interest_rate
        self._balance += interest

        print(
            f"Applied monthly interest ({self._interest_rate * 100:.1f}%). "
            f"New balance: ${self._balance:.2f}"
        )

    def display_details(self):
        print("Savings Account")
        print(f"Owner        : {self._owner}")
        print(f"Account #    : {self._account_number}")
        print(f"Balance      : ${self._balance:.2f}")
        print(
            f"Withdrawals  : {self._withdrawals_used}/{self._withdrawal_limit}"
        )
        print(f"Interest     : {self._interest_rate * 100:.1f}% monthly")


# investment account that requires a minimum balance 
class InvestmentAccount(Account):
    def __init__(
        self,
        owner,
        account_number,
        balance,
        minimum_balance=1000,
    ):
        super().__init__(owner, account_number, balance)

        self._minimum_balance = minimum_balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")

        if self._balance - amount < self._minimum_balance:
            raise MinimumBalanceError(
                f"Cannot withdraw. Balance must stay above "
                f"${self._minimum_balance:.2f}"
            )

        self._balance -= amount

        print(f"Withdrew ${amount:.2f}. New balance: ${self._balance:.2f}")

    def apply_return(self, rate):
        growth = self._balance * rate
        self._balance += growth

        print(
            f"Applied return rate of {rate * 100:.1f}%. "
            f"New balance: ${self._balance:.2f}"
        )

    def display_details(self):
        print("Investment Account")
        print(f"Owner            : {self._owner}")
        print(f"Account #        : {self._account_number}")
        print(f"Balance          : ${self._balance:.2f}")
        print(f"Minimum Balance  : ${self._minimum_balance:.2f}")


# bank class manages all accounts
class Bank:
    def __init__(self):
        self.accounts = {}
        self.next_id = 1

    def generate_account_number(self, prefix):
        account_number = f"{prefix}-{self.next_id:05d}"
        self.next_id += 1
        return account_number

    def open_account(self, account_type, owner, balance):

        if account_type == "checking":
            account_number = self.generate_account_number("CHK")
            account = CheckingAccount(owner, account_number, balance)

        elif account_type == "savings":
            account_number = self.generate_account_number("SAV")
            account = SavingsAccount(owner, account_number, balance)

        elif account_type == "investment":
            account_number = self.generate_account_number("INV")
            account = InvestmentAccount(owner, account_number, balance)

        else:
            raise ValueError("Invalid account type.")

        self.accounts[account_number] = account
        return account

    def find_account(self, account_number):
        if account_number not in self.accounts:
            raise ValueError("Account not found.")

        return self.accounts[account_number]

    def list_accounts(self):
        if not self.accounts:
            print("No accounts available.")
            return

        print("\nAll Accounts")
        for account in self.accounts.values():
            print(
                f"{account._account_number} | "
                f"{account._owner} | "
                f"${account._balance:.2f}"
            )


# Main menu loop for banking system 
bank = Bank()

while True:

    print("     Welcome to PyBank CLI")
    print("[1] Open a new account")
    print("[2] Select an account")
    print("[3] List all accounts")
    print("[4] Quit")

    choice = input("\n> ")

    # open a new account 
    if choice == "1":

        print("\nAccount type:")
        print("[1] Checking")
        print("[2] Savings")
        print("[3] Investment")

        account_choice = input("> ")

        owner = input("Owner name: ")

        try:
            balance = float(input("Opening balance: "))

            if account_choice == "1":
                account = bank.open_account(
                    "checking", owner, balance
                )

            elif account_choice == "2":
                account = bank.open_account(
                    "savings", owner, balance
                )

            elif account_choice == "3":
                account = bank.open_account(
                    "investment", owner, balance
                )

            else:
                print("Invalid account type.")
                continue

            print(
                f"\nAccount opened successfully!"
            )
            print(
                f"Account #: {account._account_number}"
            )

        except ValueError:
            print("Please enter a valid number.")

    # select and manage an existing account
    elif choice == "2":

        account_number = input("Enter account number: ")

        try:
            account = bank.find_account(account_number)

            while True:

                print(
                    f"\nAccount Selected: "
                    f"{account._owner} "
                    f"({account._account_number})"
                )

                print("[1] Deposit")
                print("[2] Withdraw")
                print("[3] View Details")

                option_four = None

                if isinstance(account, SavingsAccount):
                    print("[4] Apply Monthly Interest")
                    option_four = "interest"

                elif isinstance(account, InvestmentAccount):
                    print("[4] Apply Investment Return")
                    option_four = "return"

                print("[0] Back")

                sub_choice = input("> ")

                try:

                    if sub_choice == "1":
                        amount = float(input("Deposit amount: "))
                        account.deposit(amount)

                    elif sub_choice == "2":
                        amount = float(input("Withdrawal amount: "))
                        account.withdraw(amount)

                    elif sub_choice == "3":
                        account.display_details()

                    elif (
                        sub_choice == "4"
                        and option_four == "interest"
                    ):
                        account.apply_interest()

                    elif (
                        sub_choice == "4"
                        and option_four == "return"
                    ):
                        rate = float(
                            input(
                                "Enter return rate "
                                "(0.10 = 10%): "
                            )
                        )

                        account.apply_return(rate)

                    elif sub_choice == "0":
                        break

                    else:
                        print("Invalid menu choice.")

                except (
                    ValueError,
                    BankError,
                ) as error:
                    print(f"Error: {error}")

        except ValueError as error:
            print(f"Error: {error}")

    # display all accounts currently stored in bank
    elif choice == "3":
        bank.list_accounts()

    # exits program 
    elif choice == "4":
        print("Thank you for using PyBank!")
        break

    else:
        print("Invalid menu option.")