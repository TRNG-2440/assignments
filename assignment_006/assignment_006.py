# Assignment 6 by Ariyan Shaikh
from typing import Type, Optional, Dict

# This is the parent class
class Account:
    def __init__(self, owner_name: str, account_number: str, balance: float = 0.0):
        self.owner_name = owner_name
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount: float) -> None:
        """Adds funds to the account if the amount is positive."""
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}")
        else:
            print("Deposit amount must be positive.")

    def display_details(self) -> None:
        """Prints the current details of the account."""
        print(f"--- Account Details ---")
        print(f"Owner: {self.owner_name}")
        print(f"Account Number: {self.account_number}")
        print(f"Balance: ${self.balance:.2f}")

class CheckingAccount(Account):
    def __init__(self, owner_name: str, account_number: str, balance: float = 0.0, overdraft_limit: float = 500.0):
        # Initialize parent class attributes
        super().__init__(owner_name, account_number, balance)
        # Set the unique overdraft buffer limit
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float) -> bool:
        """Withdraws funds, allowing the balance to go negative up to the overdraft limit."""
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
            
        # Calculate maximum available money (actual balance + overdraft buffer)
        total_available = self.balance + self.overdraft_limit
        
        if amount <= total_available:
            self.balance -= amount
            print(f"Withdrew ${amount:.2f}. Current balance: ${self.balance:.2f}")
            return True
        else:
            print(f"Transaction declined: Exceeds overdraft limit of ${self.overdraft_limit:.2f}.")
            return False

    def display_details(self) -> None:
        """Displays regular account details along with the overdraft limit."""
        super().display_details()
        print(f"Overdraft Limit: ${self.overdraft_limit:.2f}")

class SavingsAccount(Account):
    def __init__(self, owner_name: str, account_number: str, balance: float = 0.0, interest_rate: float = 0.01, max_withdrawals: int = 3):
        # Initialize parent class attributes
        super().__init__(owner_name, account_number, balance)
        # Unique attributes for savings account
        self.interest_rate = interest_rate          # e.g., 0.01 for 1%
        self.max_withdrawals = max_withdrawals
        self.withdrawal_count = 0                   # Tracks current month's withdrawals

    def withdraw(self, amount: float) -> bool:
        """Withdraws funds if within balance limits and monthly transaction cap."""
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
            
        # 1. Check monthly transaction limit
        if self.withdrawal_count >= self.max_withdrawals:
            print(f"Transaction declined: Monthly withdrawal limit of {self.max_withdrawals} reached.")
            return False
            
        # 2. Check standard available balance
        if amount > self.balance:
            print(f"Transaction declined: Insufficient funds. Balance is ${self.balance:.2f}.")
            return False
            
        # Deduct funds and advance counter
        self.balance -= amount
        self.withdrawal_count += 1
        print(f"Withdrew ${amount:.2f} ({self.withdrawal_count}/{self.max_withdrawals} used). Balance: ${self.balance:.2f}")
        return True

    def apply_monthly_interest(self) -> None:
        """Calculates and adds monthly interest to the balance."""
        interest_earned = self.balance * self.interest_rate
        self.balance += interest_earned
        print(f"Applied monthly interest of ${interest_earned:.2f}. New balance: ${self.balance:.2f}")

    def reset_monthly_limits(self) -> None:
        """Resets the withdrawal counter for a new month."""
        self.withdrawal_count = 0
        print("Monthly limits have been reset.")

    def display_details(self) -> None:
        """Displays regular account details alongside savings metrics."""
        super().display_details()
        print(f"Interest Rate: {self.interest_rate * 100:.1f}%")
        print(f"Withdrawals This Month: {self.withdrawal_count}/{self.max_withdrawals}")

class InvestmentAccount(Account):
    def __init__(self, owner_name: str, account_number: str, balance: float = 0.0, minimum_balance: float = 1000.0):
        # Initialize parent class attributes
        super().__init__(owner_name, account_number, balance)
        # Set the unique investment constraints
        self.minimum_balance = minimum_balance
        
        # Ensure initial balance respects the minimum requirement
        if self.balance < self.minimum_balance:
            print(f"Warning: Initial balance (${self.balance:.2f}) is below the required minimum (${self.minimum_balance:.2f}).")

    def withdraw(self, amount: float) -> bool:
        """Withdraws funds only if the remaining balance stays above the minimum threshold."""
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
            
        # Calculate what the balance would look like after withdrawal
        projected_balance = self.balance - amount
        
        if projected_balance >= self.minimum_balance:
            self.balance -= amount
            print(f"Withdrew ${amount:.2f}. Current balance: ${self.balance:.2f}")
            return True
        else:
            print(f"Transaction declined: Balance cannot drop below the minimum requirement of ${self.minimum_balance:.2f}.")
            return False

    def apply_market_return(self, return_rate: float) -> None:
        """Simulates market performance by applying a variable rate (can be positive or negative)."""
        change = self.balance * return_rate
        self.balance += change
        
        if change >= 0:
            print(f"Market growth: Gained ${change:.2f} ({return_rate * 100:+.2f}%). New balance: ${self.balance:.2f}")
        else:
            print(f"Market downturn: Lost ${abs(change):.2f} ({return_rate * 100:+.2f}%). New balance: ${self.balance:.2f}")

    def display_details(self) -> None:
        """Displays regular account details alongside investment boundaries."""
        super().display_details()
        print(f"Required Minimum Balance: ${self.minimum_balance:.2f}")

class Bank:
    """
    Bank class used to manage bank accounts
    """
    def __init__(self, bank_name: str):
        self.bank_name = bank_name
        # Store accounts in a dictionary with account_number as the key
        self.accounts: Dict[str, Account] = {}

    def open_account(self, account_class: Type[Account], *args, **kwargs) -> Optional[Account]:
        """Creates and stores a new account of any specified class type."""
        # Instantiate the provided account class using standard or keyword arguments
        try:
            new_account = account_class(*args, **kwargs)
        except TypeError as e:
            print(f"Failed to open account: Invalid arguments provided. ({e})")
            return None

        # Ensure the account number is unique within our system
        if new_account.account_number in self.accounts:
            print(f"Failed to open account: Number {new_account.account_number} already exists.")
            return None

        # Add to the bank collection
        self.accounts[new_account.account_number] = new_account
        print(f"Successfully opened a new {account_class.__name__} for {new_account.owner_name}.")
        return new_account

    def lookup_account(self, account_number: str) -> Optional[Account]:
        """Finds and returns an account object by its unique account number."""
        account = self.accounts.get(account_number)
        if not account:
            print(f"Error: Account number {account_number} not found.")
        return account

    def list_accounts(self) -> None:
        """Iterates over all stored accounts and lists their current balances."""
        print(f"\n==========================================")
        print(f"        {self.bank_name.upper()} ACCOUNTS LIST        ")
        print(f"==========================================")
        
        if not self.accounts:
            print("No active accounts found in the bank.")
            return

        for acc in self.accounts.values():
            # Dynamically reads the specific class name of each object
            account_type = acc.__class__.__name__
            print(f"[{account_type}] #{acc.account_number} | Owner: {acc.owner_name} | Balance: ${acc.balance:.2f}")
        print(f"==========================================\n")


def get_selection(num_selections: int) -> int:
    """
    Collects and validates users's Selection.
    Requires the number of selections passed as an int paramater
    """
    while True:
        try:
            selection = int(input("Select an option: "))        
            if selection > num_selections or selection < 1:
                raise Exception("Invalid input detected")
        except Exception as ex:
            print("\nThat is not a valid input. Please try again\n")
            return get_selection(num_selections)
        return selection

def open_account() -> None:
    print("Account type:")
    print("[1] Checking")
    print("[2] Savings")
    print("[3] Investment")
    account_type = get_selection(3)
    match account_type:
        case 1:
            name = input("Owner name: ")
            account_number = input("Enter the account number you want: ")
            opening_balance = int(input("Opening balance: "))
            cli_bank.open_account(CheckingAccount,account_number,opening_balance)
            print()
            return
        case 2:
            name = input("Owner name: ")
            account_number = input("Enter the account number you want: ")
            opening_balance = int(input("Opening balance: "))
            cli_bank.open_account(SavingsAccount,account_number,opening_balance)
            print()
            return
        case 3:
            name = input("Owner name: ")
            account_number = input("Enter the account number you want: ")
            opening_balance = int(input("Opening balance: "))
            cli_bank.open_account(InvestmentAccount,account_number,opening_balance)
            print()
            return

def manage_account_submenu(account: Account) -> None:
    """Submenu triggered when a specific account is selected."""
    while True:
        print(f"\n--- Managing Account #{account.account_number} ({account.owner_name}) ---")
        print("[1] Check Details/Balance")
        print("[2] Deposit Funds")
        print("[3] Withdraw Funds")
        
        # Add dynamic class-specific menu choices contextually
        extra_options = []
        if isinstance(account, SavingsAccount):
            print("[4] Apply Monthly Interest")
            extra_options = [4]
        elif isinstance(account, InvestmentAccount):
            print("[4] Simulate Market Return (+5%)")
            print("[5] Simulate Market Dip (-3%)")
            extra_options = [4, 5]
            
        print(f"[{len(extra_options) + 4}] Return to Main Menu")
        
        choice = get_selection(len(extra_options) + 4)
        
        if choice == 1:
            account.display_details()
        elif choice == 2:
            amt = float(input("Enter deposit amount: $"))
            account.deposit(amt)
        elif choice == 3:
            if hasattr(account, 'withdraw'):
                amt = float(input("Enter withdrawal amount: $"))
                account.withdraw(amt)
            else:
                print("This account type does not natively support withdrawals.")
        elif choice in extra_options:
            if isinstance(account, SavingsAccount) and choice == 4:
                account.apply_monthly_interest()
            elif isinstance(account, InvestmentAccount):
                if choice == 4: account.apply_market_return(0.05)
                if choice == 5: account.apply_market_return(-0.03)
        else:
            break

if __name__ == "__main__":
    cli_bank = Bank("PyBank")
    print("=" * 40)
    print(f'{"Welcome to PyBank CLI":^40}')
    print("=" * 40)

    print("\n[1] Open a new account")
    print("[2] Select an account")
    print("[3] List all accounts")
    print("[4] Quit")

    while True:
        selection = get_selection(4)
        match selection:
            case 1:
                print("=" * 40)
                open_account()
                print("=" * 40)
            case 2:
               acct_num = input("Enter Account Number to lookup: ")
               target_account = cli_bank.lookup_account(acct_num)
               if target_account:
                   manage_account_submenu(target_account)
               else:
                   print("No matching account found.")
            case 3:
                print("=" * 40)
                cli_bank.list_accounts()
                print("=" * 40)
            case 4:
                print("Goodbye")
                break