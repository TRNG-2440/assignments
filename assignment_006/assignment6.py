"""
Assignment 6
# Python Coding Activity 6 - Bank Account System

## Objective

In this activity, you will design and implement a class hierarchy to simulate a simple banking system. You will practice core OOP concepts including:

- Class design and instantiation
- Inheritance and method overriding
- Encapsulation (using private/protected attributes)
- Polymorphism (shared interfaces with unique behaviors per account type)
- Exception handling for invalid operations
- Basic CLI interaction via a menu-driven loop

---

## Instructions

You will build a banking system that supports three types of accounts: **Checking**, **Savings**, and **Investment**. All account types share a common base, but each enforces its own rules and behaviors.

1. Create a base `Account` class that holds common attributes such as owner name, account number, and balance. It should support depositing funds and displaying account details.

2. Create a `CheckingAccount` subclass with the following unique behavior:
   - Supports overdraft protection up to a set limit — withdrawals that would exceed the balance may draw from the overdraft buffer, but not beyond it.

3. Create a `SavingsAccount` subclass with the following unique behavior:
   - Applies a monthly interest rate to the balance when triggered.
   - Enforces a maximum number of withdrawals per month; attempts beyond the limit should be rejected. Note: the example indicates a limit of 3, but you are free to set any reasonable value you wish

4. Create an `InvestmentAccount` subclass with the following unique behavior:
   - Has a minimum balance requirement — withdrawals that would drop the balance below the minimum should be rejected.
   - Supports a method to apply a variable return rate to simulate investment growth.

5. Create a `Bank` class that manages a collection of accounts. It should support:
   - Opening a new account of any supported type
   - Looking up an account by account number
   - Listing all accounts and their current balances

6. Build a CLI menu loop that allows the user to interact with the bank. The menu should support at minimum: opening an account, selecting an account, depositing, withdrawing and viewing account details. Any unique functionality for a type of account should show menu options for those unique features only when viewing certain account types (i.e. "apply interest" only appears for Savings Accounts).

7. All invalid operations (overdraft exceeded, withdrawal limit hit, below minimum balance) must raise and handle appropriate exceptions with clear, descriptive error messages — do not use bare `if/else` returns for these cases.

---

## Example Interaction

```
==============================
   Welcome to PyBank CLI
==============================

[1] Open a new account
[2] Select an account
[3] List all accounts
[4] Quit

> 1

Account type:
[1] Checking
[2] Savings
[3] Investment
> 2

Owner name: Alice Johnson
Opening balance: 500

Savings account opened for Alice Johnson.
   Account #: SAV-00423  |  Balance: $500.00

------------------------------

> 2
Enter account number: SAV-00423

Account selected: Alice Johnson (SAV-00423)

[1] Deposit
[2] Withdraw
[3] Apply Monthly Interest
[4] View Details
[5] Back to Main Menu

> 1
Deposit amount: 250
Deposited $250.00. New balance: $750.00

> 2
Withdrawal amount: 100
Withdrew $100.00. New balance: $650.00

> 2
Withdrawal amount: 100
Withdrew $100.00. New balance: $550.00

> 2
Withdrawal amount: 100
Withdrew $100.00. New balance: $450.00

> 2
Withdrawal amount: 50
Error: Monthly withdrawal limit reached (3/3 used). Try again next month.

> 3
Applied monthly interest (2.5%). New balance: $461.25

> 4
------------------------------
Account Details
------------------------------
Owner       : Alice Johnson
Account #   : SAV-00423
Type        : Savings
Balance     : $461.25
Withdrawals : 3/3 used this month
Interest    : 2.5% monthly
------------------------------
```

---

## Requirements Checklist

- [ ] A base `Account` class exists with shared attributes and a deposit method
- [ ] `CheckingAccount` correctly allows overdraft up to its defined limit and rejects amounts beyond it
- [ ] `SavingsAccount` tracks monthly withdrawals and enforces the withdrawal limit
- [ ] `SavingsAccount` correctly applies interest to the current balance
- [ ] `InvestmentAccount` enforces a minimum balance on withdrawals
- [ ] `InvestmentAccount` correctly applies a variable return rate
- [ ] Each subclass overrides a method for displaying account details
- [ ] A `Bank` class manages multiple accounts and supports lookup by account number
- [ ] Account numbers are auto-generated and unique
- [ ] All invalid operations raise exceptions with descriptive messages
- [ ] The CLI menu loop handles bad input (non-numeric amounts, invalid menu options) gracefully without crashing
- [ ] Depositing a negative or zero amount is rejected
- [ ] Selecting a non-existent account number displays an appropriate error

---

## Stretch Goals

- **Account Management & Authentication** - The top-level menu allows users to open a new account or login before accessing their existing account details. Login is protected via username/password combination matching.

- **Transaction History** - Each account maintains a log of all transactions (type, amount, timestamp). Add a "View History" option to the account menu that prints a formatted ledger.

- **Persistence** - Save and load all account data to/from a JSON file so that account state is preserved between sessions.

- **Account Transfers** - Add a transfer option from the main menu that moves funds from one account to another, respecting both accounts' withdrawal and balance rules.

- **Monthly Reset Simulation** - Add a main menu option that simulates the end of a month: applies interest/returns to all eligible accounts and resets withdrawal counters on all Savings accounts.
"""
import random
from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Optional, Callable

from assignments.shared.menu import Menu


class AccountType(StrEnum):
    CHECKING = "Checking"
    SAVINGS = "Savings"
    INVESTMENT = "Investment"

class Account(ABC):
    """
    Base account object
    """
    def __init__(self, name: str, account_number: str, balance: float):
        self._name: str = name
        self._account_number: str = account_number
        self._balance: float = balance


    def get_name(self) -> str:
        """

        :return:
        """
        return self._name


    def get_account_number(self) -> str:
        """

        :return:
        """
        return self._account_number


    def get_balance(self) -> float:
        """

        :return:
        """
        return self._balance


    def deposit(self, amount: float) -> None:
        """

        :param amount:
        :raise ValueError:
        """
        if amount <= 0:
            raise ValueError(f"Deposit amount cannot be less than or equal to $0 (was {amount:,.2f}")
        self._balance += amount


    @abstractmethod
    def get_type(self) -> AccountType:
        raise NotImplemented()

    @abstractmethod
    def withdraw(self, amount: float) -> float:
        """

        """
        raise NotImplemented()

    def short_account_info(self) -> str:
        return f"{self._account_number}: ${self._balance:,.2f}"

    def __str__(self):
        return (f"Account ({self.get_type()}:\n"
                f"\tName: {self._name}\n"
                f"\tAccount Number: {self._account_number}\n"
                f"\tBalance: ${self._balance:,.2f}")


class CheckingAccount(Account):

    def __init__(self, name: str, account_number: str, balance: float, overdraft: float, max_overdraft: float = None):
        super().__init__(name, account_number, balance)
        self._overdraft = overdraft
        self._max_overdraft = max_overdraft if max_overdraft is not None else overdraft

    def get_type(self) -> AccountType:
        return AccountType.CHECKING

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError(f"Withdrawal amount cannot be less than or equal to $0 (was {amount:,.2f}")

        to_withdraw: float = amount
        remainder: float = self._balance - amount
        if remainder < 0:
            self.balance = 0
            to_withdraw += remainder
            overdraft_remainder: float = self._overdraft - to_withdraw
            if overdraft_remainder < 0:
                raise InsuffcientFundsError(f"Not enough funds to withdraw ${amount:,.2f} (overdraft: ${self._overdraft:,.2f})")
            self._overdraft = overdraft_remainder
        else:
            self.balance = remainder
        return to_withdraw

    def deposit(self, amount: float) -> None:
        #first, replenish overdraft
        if amount <= 0:
            raise ValueError(f"Deposit amount cannot be less than or equal to $0 (was {amount:,.2f}")
        needed_overdraft: float = self._max_overdraft - self._overdraft
        if needed_overdraft > 0:
            to_overdraft: float = needed_overdraft - amount
            amount -= to_overdraft
            self._overdraft += to_overdraft
        if amount > 0:
            super().deposit(amount)

    def __str__(self):
        return super().__str__() + (f"\n\tOverdraft Limit: ${self._overdraft:,.2f}\n"
                             f"\tMax Overdraft Limit: ${self._max_overdraft:,.2f}")

class SavingsAccount(Account):

    def __init__(self, name: str, account_number: str, balance: float, monthly_interest: float, remaining_withdrawals: int, max_withdrawals: int = None):
        super().__init__(name, account_number, balance)
        self._monthly_interest: float = monthly_interest
        self._remaining_withdrawals: int = remaining_withdrawals
        self._max_withdrawals: int = max_withdrawals if max_withdrawals is not None else remaining_withdrawals

    def get_type(self) -> AccountType:
        return AccountType.SAVINGS

    def apply_monthly_interest(self):
        self._balance *= 1 + self._monthly_interest

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError(f"Withdrawal amount cannot be less than or equal to $0 (was {amount:,.2f}")
        if self._remaining_withdrawals <= 0:
            raise InsufficientWithdrawalsError("No remaining withdrawals")

        self._remaining_withdrawals -= 1

        to_withdraw: float = amount
        remainder: float = self._balance - amount
        if remainder < 0:
            raise InsuffcientFundsError(f"Not enough funds to withdraw ${amount:,.2f} (balance: ${self._balance:,.2f})")

        self._balance -= to_withdraw

        return to_withdraw

    def __str__(self):
        return super().__str__() + (f"\n\tRemaining Withdrawals: {self._remaining_withdrawals}\n"
                         f"\tMax Withdrawals: {self._max_withdrawals}"
                         f"\tMonthly Interest: {self._monthly_interest}%")


class InvestmentAccount(Account):
    def __init__(self, name: str, account_number: str, balance: float, minimum_balance: float):
        super().__init__(name, account_number, balance)
        self._minimum_balance = minimum_balance

    def get_type(self) -> AccountType:
        return AccountType.INVESTMENT

    def apply_variable_return(self, return_rate: float) -> None:
        self._balance *= return_rate

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError(f"Withdrawal amount cannot be less than or equal to $0 (was {amount:,.2f}")

        if self._balance < self._minimum_balance:
            raise InsuffcientFundsError(f"Cannot withdraw, balance ${self._balance:,.2f} is below minimum balance ${self._minimum_balance:,.2f}")

        to_withdraw: float = amount
        remainder: float = self._balance - self._minimum_balance - amount
        if remainder < 0:
            raise InsuffcientFundsError(f"Not enough funds to withdraw ${amount:,.2f} (balance: ${self._balance:,.2f})")

        return to_withdraw


    def __str__(self):
        return super().__str__() + (f"\n\tMinimum Balance: {self._minimum_balance}\n")


class Bank:
    max_overdraft: float = 250
    max_withdrawals: int = 5
    monthly_interest: float = 0.025
    minimum_balance: float = 500
    def __init__(self):
        self._accounts: dict[str, Account] = {}

    def create_account(self, type: AccountType, name: str, balance: float) -> Account:
        """
        Creates the account
        :param type:
        :param name:
        :param balance:
        """
        new_account: Account
        new_id: str = self.generate_account_id()
        match type:
            case AccountType.CHECKING:
                new_account = CheckingAccount(name, new_id, balance, self.max_overdraft, self.max_overdraft)
            case AccountType.SAVINGS:
                new_account = SavingsAccount(name, new_id, balance, self.monthly_interest, self.max_withdrawals, self.max_withdrawals)
            case AccountType.INVESTMENT:
                new_account = InvestmentAccount(name, new_id, balance, self.minimum_balance)

        self._accounts[new_id] = new_account

        return new_account

    def generate_account_id(self):
        return "ACC_" + str(len(self._accounts)) + "_" + str(random.randint(1, 64))

    def lookup_account(self, account_id: str) -> Optional[Account]:
        if account_id not in self._accounts:
            return None

        return self._accounts[account_id]

    def list_accounts(self) -> str:
        return "\n".join([account.short_account_info() for account in self._accounts.values()])

    def get_accounts(self) -> dict[str, Account]:
        return self._accounts


class InsuffcientFundsError(Exception):
    pass

class InsufficientWithdrawalsError(Exception):
    pass


class BankMenu(Menu):
    def __init__(self, bank: Bank):
        super().__init__({
            "Open a new Account": self.open_account,
            "Select an account": self.select_an_account,
            "List all accounts": self.list_accounts,
        },
        add_quit=True)
        self._bank = bank

    def header(self) -> str:
        return "Bank CLI"

    def open_account(self):
        CreateAccountMenu(self._bank).do_selection()

    def select_an_account(self):
        account_id: str = input("Enter account number: ")
        account: Optional[Account] = self._bank.lookup_account(account_id)
        if account is None:
            print(f"No account with the number: {account_id}")
        SelectedAccountMenu(account).show_menu()


    def list_accounts(self):
        if len(self._bank.get_accounts()) == 0:
            print("There are currently no accounts")
        print(self._bank.list_accounts())

class CreateAccountMenu(Menu):

    def __init__(self, bank: Bank):
        super().__init__({
            "Checking": lambda: self.create_account(AccountType.CHECKING),
            "Savings": lambda: self.create_account(AccountType.SAVINGS),
            "Investment": lambda: self.create_account(AccountType.INVESTMENT),
        })
        self._bank = bank

    def create_account(self, type: AccountType):
        print("")
        print(f"Account: {type}")
        name: str = input("Owner Name: ")
        balance: float
        while True:
            try:
                balance: float = float(input("Opening Balance: ").strip("$"))
                if balance < 0:
                    raise ValueError
                break
            except ValueError:
                print("Balance must be greater than or equal to $0 and a float")

        new_account: Account = self._bank.create_account(type, name, balance)
        print(f"{str(type)} account opened for {name}.")
        print(new_account)
        print("")


class SelectedAccountMenu(Menu):

    def __init__(self, account: Account):
        super().__init__({
            "Deposit": self.deposit,
            "Withdraw": self.withdraw,
            "Apply Monthly Interest": self.apply_monthly_interest,
            "View Details": self.view_details,
            "Back to Main Menu": self.back_to_main_menu,
        })
        self.account = account

    def deposit(self):
        while True:
            amount: float
            try:
                amount: float = float(input("Deposit amount: ").strip("$"))
            except ValueError:
                print("Amount must be a float and greater than $0")
                continue
            try:
                self.account.deposit(amount)
                print(f"Deposited ${amount:,.2f}. New balance: ${self.account.get_balance():,.2f}")
                break
            except ValueError as e:
                print(e.args[0])

    def withdraw(self):
        while True:
            amount: float
            try:
                amount: float = float(input("Withdraw amount: ").strip("$"))
            except ValueError:
                print("Amount must be a float and greater than $0")
                continue
            try:
                self.account.deposit(amount)
                print(f"Withdrew ${amount:,.2f}. New balance: ${self.account.get_balance():,.2f}")
                break
            except ValueError | InsuffcientFundsError | InsufficientWithdrawalsError as e:
                print(e.args[0])

    def apply_monthly_interest(self):
        if not isinstance(self.account, SavingsAccount):
            print("Invalid type: Account is not a Savings Account")
            return

        savings_account: SavingsAccount = self.account
        savings_account.apply_monthly_interest()
        print(f"Applied monthly interest. Balance is now ${savings_account.get_balance():,.2f}")

    def view_details(self):
        print(self.account)

    def back_to_main_menu(self):
        raise KeyboardInterrupt


if __name__ == "__main__":
    BankMenu(Bank()).start()
