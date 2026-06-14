"""

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

# Random number library
from random import randint

# -------------------------------------------------------------------------------------

# Parent class
class Account:

  # Constructor
  def __init__(self, ownerName, checkingAccountNumber, savingsAccountNumber, investmentAccountNumber, balance):

    self.ownerName = ownerName
    self.checkingAccountNumber = checkingAccountNumber
    self.savingsAccountNumber = savingsAccountNumber
    self.investmentAccountNumber = investmentAccountNumber
    self.balance = balance
  
  # Deposit funds in checking account
  def Deposit(self, amount):

    if(amount < 0):
      raise ValueError('\nError - Amount must be over $0.00.  Please re-enter\n\n')
    
    else:
      self.balance += amount

  # Display bank account details
  def Display(self):
    
    # Display criteria
    print(f'\n------- {self.ownerName} -------\n')
    print(f'Checking Account Number: {self.checkingAccountNumber}')
    print(f'Savings Account Number: {self.savingsAccountNumber}')
    print(f'Investment Account Number: {self.investmentAccountNumber}')
    print(f'Balance: ${self.balance}')


# -------------------------------------------------------------------------------------

# Child class - checking account
class CheckingAccount(Account):
  
  # Constructor
  def __init__(self, ownerName, checkingAccountNumber, balance, overDraftLimit):

    # Implement parent class constructor  
    super().__init__(ownerName, checkingAccountNumber, None, None, balance)

    self.overDraftLimit = overDraftLimit
    self.isOverDraft = False

  def Withdraw(self, amount):
    if(amount > (self.balance + self.overDraftLimit)):
      raise ValueError(f'\nError - value exceeds balance\n\nUser may only withdraw up to ${self.balance + self.overDraftLimit}\n\nPlease withdraw different amount.\n\n')
    
    elif amount <= self.balance:
      self.balance -= amount

      
      # Display checking account information
      print(f'\n------- Checking Account -------\n')

      print(f'Owner Name: {self.ownerName}')

      print(f'Chcking Account Number: ${self.checkingAccountNumber}')

      print(f'Savings Account Number: ${self.savingsAccountNumber}')

      print(f'Investment Account Number: ${self.investmentAccountNumber}')

      print(f'Balance: ${self.balance:.2f}')
    
    elif amount > self.balance and amount <= (self.balance + self.overDraftLimit):
      overDraftUsed = (amount - self.balance)
      self.balance -= amount
      self.overDraftLimit -= overDraftUsed
      self.isOverDraft = True
    
# -------------------------------------------------------------------------------------

# Child class - savings account 
class SavingsAccount(Account):

  # Constructor
  def __init__(self, ownerName, savingsAccountNumber, balance, interestRate = 0.1, maxWithdrawals = 3):

    # Implement parent class constructor
    super().__init__(ownerName, None, savingsAccountNumber, None, balance)
    self.interestRate = interestRate
    self.maxWithdrawals = maxWithdrawals
    self.interest = (self.balance * self.interestRate)
    self.withdrawAttempts = 3

  # Withdraw from savings account
  def Withdraw(self, amount):

    if(amount > self.balance):
      raise ValueError(f'\n\nError - amount exceeds balance\n\n')
    
    else:
      if self.withdrawAttempts > 0: 
        self.withdrawAttempts -= 1
        self.balance -= amount

        # Display savings account information
        print(f'\n------- Savings Account -------\n')

        print(f'Owner Name: {self.ownerName}')

        print(f'Chcking Account Number: ${self.checkingAccountNumber}')

        print(f'Savings Account Number: ${self.savingsAccountNumber}')

        print(f'Investment Account Number: ${self.investmentAccountNumber}')

        print(f'Withdraw attempts: {self.withdrawAttempts}')

      else:
        raise ValueError(f'\n\nError - user has exceeded withdraw attempts\n\n')

  # Assign interest
  def ExecuteInterest(self):

    self.balance += self.interest

    print(f'\n------- Savings Account -------\n')
    print(f'Balance: {self.balance:.2f}')
    print(f'Interest: {self.balance:.2f}')

# -------------------------------------------------------------------------------------

# Child class - investment account 
class InvestmentAccount(Account):

  # Constructor 
  def __init__(self, ownerName, investmentAccountNumber, balance, minimumBalance = 300):
        
        # Implement parent class constructor
        super().__init__(ownerName, None, None, investmentAccountNumber, balance)
        self.minimumBalance = minimumBalance

  # Withdraw from investment account
  def Withdraw(self, amount):
    
    if(self.balance - amount < self.minimumBalance):
      raise ValueError(f'\nError - Withdraw failed\n\nbalance must exceed minimum balance requirement of ${self.minimumBalance}\n\nPlease withdraw a lower amount.\n\n')
    
    else:

      self.balance -= amount

      print(f'\n------- Investment Account -------\n')

      # Display information
      print(f'Owner Name: {self.ownerName}')

      print(f'Chcking Account Number: ${self.checkingAccountNumber}')

      print(f'Savings Account Number: ${self.savingsAccountNumber}')

      print(f'Investment Account Number: ${self.investmentAccountNumber}')

      print(f'Balance: ${self.balance:.2f}')

  # Generate client's return rate
  def ReturnRate(self, interest):

    # Apply return to user
    self.balance += (self.balance * interest)

    # Display information   
    print(f'\n------- Investment Account -------\n')

    print(f'Owner Name: {self.ownerName}')

    print(f'Chcking Account Number: ${self.checkingAccountNumber}')

    print(f'Savings Account Number: ${self.savingsAccountNumber}')

    print(f'Investment Account Number: ${self.investmentAccountNumber}')

    print(f'Balance: ${self.balance:.2f}')

    print(f'Return Rate: ${(self.balance * interest):.2f}')

# -------------------------------------------------------------------------------------
# Class used to store bank accounts
class Bank():

  # Constructor 
  def __init__(self):

    self.firstName = ""

    self.lastName = ""

    # Store accounts
    self.accountList = []

# ------------------------------------------------------------------------------------  

  # User menu
  def AccountTypeMenu(self) -> str:

    print("\n     Account Type:"\
    "\n----------------------------"\
    '\n[1] Checking Account'\
    '\n[2] Savings Account'\
    '\n[3] Investment'\
    '\n[4] Exit')
      
    return input('\n> ')
  

# ------------------------------------------------------------------------------------  
# Account menu - provides various account options
  def AccountMenuHelper(self) -> str:

    print("\n     Account Type:"\
    "\n----------------------------"\
    '\n[1] Deposit'\
    '\n[2] Withdraw'\
    '\n[3] Apply Monthly Interest'\
    '\n[4] View Details'\
    '\n[5] Exit')
      
    return input('\n> ')

# ------------------------------------------------------------------------------------  
# Account menu helper - Contributes to AccountMenu(self,account)
  def AccountMenu(self,account):

    while(True):
    
      match(self.AccountMenuHelper()):

        case "1": 
        
          amount = float(input('Input deposit amount $'))

          if not amount:
            raise ValueError('\nError - amount cannot be empty, please re-enter\n')
        
          elif amount < 0:
            raise ValueError('\nError - amount cannot be negative, please re-enter\n')
        
          account.Deposit(amount)

        case "2": 

          amount = float(input('Input withdraw amount $'))

          account.Withdraw(amount)

          print(f'\nAmount of ${amount} successfully withdrawn\n')

        case "3": 

          # Execute if account number is a savings account
          if(isinstance(account, SavingsAccount)):
            account.ExecuteInterest()
        
          # Execute if account number is an investment account
          elif(isinstance(account, InvestmentAccount)):
            account.ReturnRate(0.3)

        case "4": 

          account.Display()

        case "5": 

          print('\nExiting menu')

          break

        case _:

          # Alert user that invalid entry was enter
         print('\nInvalid entry - please re-enter option')

# ------------------------------------------------------------------------------------  
# Search for a specific account
  def SearchAccount(self, accountNumber):

    # Search through accounts
    for account in self.accountList:

      if str(account.checkingAccountNumber) == accountNumber:
        return account
      
      elif str(account.savingsAccountNumber) == accountNumber:
        return account
      
      elif str(account.investmentAccountNumber) == accountNumber:
        return account
      
    return None
  
# ------------------------------------------------------------------------------------  

  # List of all accounts
  def ListAccounts(self) -> None:

    # Declare checking account object
    checkingAcct = None

    # Declare savings account object
    savingsAcct = None

    # Declare investment account object
    investmentAcct = None

    # Traverse through accountList data strcuture 
    for account in self.accountList:
        
        # Execute condition if subscript contains CheckingAccount instance
        if isinstance(account, CheckingAccount):
            checkingAcct = account

        # Execute condition if subscript contains SavingsAccount instance
        elif isinstance(account, SavingsAccount):
            savingsAcct = account

        # Execute condition if subscript contains Inventory instance
        elif isinstance(account, InvestmentAccount):
            investmentAcct = account

    # Display Criteria
    print(f"\n------- {self.firstName} {self.lastName} -------\n")
      
    if checkingAcct is not None: 
      print(f"Checking Account Number: {checkingAcct.checkingAccountNumber}")
      print(f"\nChecking account Balance: ${checkingAcct.balance}")

    if savingsAcct is not None:   
      print(f"\nSavings Account Number: {savingsAcct.savingsAccountNumber}")
      print(f"\nSavings account Balance: ${savingsAcct.balance}")
      
    if investmentAcct is not None:
      print(f"\nInvestment Account Number: {investmentAcct.investmentAccountNumber}")
      print(f"\nInventory account Balance: ${investmentAcct.balance}")

# ------------------------------------------------------------------------------------  
  # Allow client to open an account of their choice
  def OpenAccount(self):
    
    while(True):
      
      match(self.AccountTypeMenu()):

        case "1":

          # Header
          print(f'\n------- Checking Account -------\n')

          # Prompt for owner first name if firstName is not in the system
          if not self.firstName:
            self.firstName = input('Please enter first name: ')

          if not self.firstName:
            raise ValueError('\nError - first name cannot be empty, please re-enter\n')

          # Prompt for owner last name if lastName is not in the system
          if not self.lastName:
            self.lastName = input('\nPlease enter last name: ')

          if not self.lastName:
            raise ValueError('\nError - last name cannot be empty, please re-enter\n')
          
          
          self.balance = float(input('\nOpening Balance: '))

          if not self.balance:
            raise ValueError('\nError - balance cannot be empty, please re-enter\n')
          
          self.checkingAccountNumber = randint(10000000, 99999999999999999)

          self.accountList.append(CheckingAccount(
          self.firstName + " " + self.lastName,
          self.checkingAccountNumber,
          self.balance,
          50))

          print(f'\nChecking account opened for {self.firstName + ' ' + self.lastName}')
          print(f'Account #: {self.checkingAccountNumber} | ${self.balance:.2f}\n\n')

        case "2":

          # Header
          print(f'\n------- Savings Account -------\n')

          # Prompt for owner name if firstName is not in the system
          if not self.firstName:
            self.firstName = input('\nPlease enter first name: ').strip()

          if not self.firstName:
            raise ValueError('\nError - first name cannot be empty, please re-enter\n')

          # Prompt for owner last name if lastName is not in the system
          if not self.lastName:
            self.lastName = input('\nPlease enter last name: ').strip()

          if not self.lastName:
            raise ValueError('\nError - last name cannot be empty, please re-enter\n')
          
          self.balance = float(input('Opening Balance: '))

          if not self.balance:
            raise ValueError('\nError - balance cannot be empty, please re-enter\n')

          self.savingsAccountNumber = randint(10000000, 99999999999999999)

          self.accountList.append(SavingsAccount(
          self.firstName + " " + self.lastName,
          self.savingsAccountNumber,
          self.balance,
          0.1,
          3))

          print(f'Savings account opened for {self.firstName }  {self.lastName}\n')
          print(f'Account #: {self.savingsAccountNumber} | ${self.balance}\n\n')

        case "3":

          # Header
          print(f'\n------- Investment Account -------\n')

          # Prompt for owner first name if firstName is not in the system
          if not self.firstName:
            self.firstName = input('Please enter first name: ')

          if not self.firstName:
            raise ValueError('\nError - first name cannot be empty, please re-enter\n').strip()

          # Prompt for owner last name if lastName is not in the system
          if not self.lastName:
            self.lastName = input('\nPlease enter last name: ')

          if not self.lastName:
            raise ValueError('\nError - last name cannot be empty, please re-enter\n').strip()
          
          self.balance = float(input('Opening Balance: '))

          if not self.balance:
            raise ValueError('\nError - balance cannot be empty, please re-enter\n')

          self.investmentAccountNumber = randint(10000000, 99999999999999999)

          self.accountList.append(InvestmentAccount(
          self.firstName + " " + self.lastName,
          self.investmentAccountNumber,
          self.balance,
          300))

          print(f'Investment account opened for {self.firstName } {self.lastName}\n')

          print(f'Account #: {self.investmentAccountNumber} | ${self.balance}\n\n')

        case "4":

          print('\nExiting program\n\n')
          break

        case _:

          # Alert user that invalid entry was enter
          print('\nInvalid entry - please re-enter option')

# -------------------------------------------------------------------------------------
# Display bank menu
def BankMenu() -> str:
  print('=== BANK MENU ===')
  print('[1] Open a new account')
  print('[2] Select an account')
  print('[3] List all accounts')
  print('[4] Quit')

  return input('> ')

# Main function
def main():

  try:
   
   bank = Bank()

   while(True):
     
    # Display bank menu
    print(BankMenu())

    match(input('Input option: ')):

      case "1":

        bank.OpenAccount()

      case "2":
 
        # Determine if bank account exists
        if bank.accountList:

          # Retreive selected bank account
          account = bank.SearchAccount(input('\nEnter Account Number: '))
        
        else:
          
          raise ValueError('\nError - No account exists\n')


        if(account):
          bank.AccountMenu(account)

        else:
          raise ValueError('\nAccount not found\n')

      case "3":

        bank.ListAccounts()

      case "4":
        break

      case _:

        # Alert user that invalid entry was enter
        print('\nInvalid entry - please re-enter option')

  except ValueError as error:
    print(error)

if __name__=="__main__":
  main()

  # -------------------------------------------------------------------------------------