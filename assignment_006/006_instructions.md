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

- [x] A base `Account` class exists with shared attributes and a deposit method
- [x] `CheckingAccount` correctly allows overdraft up to its defined limit and rejects amounts beyond it
- [x] `SavingsAccount` tracks monthly withdrawals and enforces the withdrawal limit
- [x] `SavingsAccount` correctly applies interest to the current balance
- [x] `InvestmentAccount` enforces a minimum balance on withdrawals
- [x] `InvestmentAccount` correctly applies a variable return rate
- [x] Each subclass overrides a method for displaying account details
- [x] A `Bank` class manages multiple accounts and supports lookup by account number
- [x] Account numbers are auto-generated and unique
- [x] All invalid operations raise exceptions with descriptive messages
- [x] The CLI menu loop handles bad input (non-numeric amounts, invalid menu options) gracefully without crashing
- [x] Depositing a negative or zero amount is rejected
- [x] Selecting a non-existent account number displays an appropriate error

---

## Stretch Goals

<!-- - **Account Management & Authentication** - The top-level menu allows users to open a new account or login before accessing their existing account details. Login is protected via username/password combination matching. -->

<!-- - **Transaction History** - Each account maintains a log of all transactions (type, amount, timestamp). Add a "View History" option to the account menu that prints a formatted ledger. -->

<!-- - **Persistence** - Save and load all account data to/from a JSON file so that account state is preserved between sessions. -->

<!-- - **Account Transfers** - Add a transfer option from the main menu that moves funds from one account to another, respecting both accounts' withdrawal and balance rules. -->

<!-- - **Monthly Reset Simulation** - Add a main menu option that simulates the end of a month: applies interest/returns to all eligible accounts and resets withdrawal counters on all Savings accounts. -->