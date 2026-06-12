
class Account:
    def __init__(self, owner_name, balance, account_number, type, withdrawals=0, deposits=0):
        self.owner_name = owner_name
        self.balance = balance
        self.account_number = account_number
        self.type = type
        self.withdrawals = withdrawals 
        self.deposits = deposits        

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self.balance += amount
        self.deposits += amount
        print(f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}")
        
    def display(self):
        print("-" * 30)
        print("Account Details")
        print("-" * 30)
        print(f"Owner       : {self.owner_name}")
        print(f"Account #   : {self.account_number}")
        print(f"Type        : {self.type}")
        print(f"Balance     : ${self.balance:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        
        if amount > self.balance:

            raise ValueError("You do not have enough funds for this withdrawal.")
        
        self.balance -= amount
        self.withdrawals += 1
        print(f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")


class CheckingAccount(Account):
    def __init__(self, owner_name, balance, account_number, type="Checking", withdrawals=0, deposits=0, buffer=750.00):
        super().__init__(owner_name, balance, account_number, type, withdrawals, deposits)

        self.buffer = buffer  
        
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount > self.balance + self.buffer:
            raise PermissionError(f"Transaction Rejected: Overdraft exceeded. Maximum allowable withdrawal is ${self.balance + self.buffer:.2f}.")
        
        self.balance -= amount
        self.withdrawals += 1
        print(f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")

    def display(self):
        super().display()
        print(f"Overdraft   : Up to ${self.buffer:.2f} buffer")
        print("-" * 30)


class SavingsAccount(Account):
    def __init__(self, owner_name, balance, account_number, type="Savings", withdrawals=0, deposits=0, interest_rate=0.035):

        super().__init__(owner_name, balance, account_number, type, withdrawals, deposits)
        self.interest_rate = interest_rate
        self.limit = 3  

    def apply_interest(self):

        interest = self.balance * self.interest_rate
        self.balance += interest 
        print(f"Applied monthly interest ({self.interest_rate * 100}%). New balance: ${self.balance:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("You have to enter a positive amount to withdraw.")
        
        if self.withdrawals >= self.limit:
            raise PermissionError(f"Error: Monthly withdrawal limit reached ({self.withdrawals}/{self.limit} used).")
        
        if amount > self.balance:
            raise ValueError("You do not have enough funds for this withdrawal.")

        self.balance -= amount
        self.withdrawals += 1
        print(f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")

    def display(self):
        super().display()
        print(f"Withdrawals : {self.withdrawals}/{self.limit} used this month")

        print(f"Interest    : {self.interest_rate * 100}% monthly")
        print("-" * 30)


class InvestmentAccount(Account):
    def __init__(self, owner_name, balance, account_number, type="Investment", withdrawals=0, deposits=0, min_balance=5000.00):
        super().__init__(owner_name, balance, account_number, type, withdrawals, deposits)
        self.min_balance = min_balance

    def apply_growth(self, growth_rate):
        growth = self.balance * growth_rate

        self.balance += growth
        print(f"Applied growth: ${growth:.2f}. New balance: ${self.balance:.2f}")

    def withdraw(self, amount):

        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        
        if self.balance - amount < self.min_balance:
            raise PermissionError(f"Transaction Rejected: Withdrawal would drop balance below the minimum required balance of ${self.min_balance:.2f}.")
        
        super().withdraw(amount)

    def display(self):
        super().display()

        print(f"Min Balance : ${self.min_balance:.2f}")
        print("-" * 30)


class Bank:
    def __init__(self):
        self.accounts = {}  

    def open_account(self, account):
        if account.account_number in self.accounts:

            print("Error: An account with this number already exists.")
            return False
        
        self.accounts[account.account_number] = account
        print(f"\n{account.type} account opened for {account.owner_name}.")

        print(f"Account #: {account.account_number}  |  Balance: ${account.balance:.2f}")
        return True

    def lookup_account(self, account_number):

        return self.accounts.get(account_number, None)

    def list_accounts(self):
        if not self.accounts:
            print("\nNo accounts have been registered in the system.")
            return
        
        print("\n" + "-" * 30)
        print("   CURRENT SYSTEM ACCOUNTS")
        print("-" * 30)
        for num, acc in self.accounts.items():
            print(f"Owner: {acc.owner_name}")
            print(f"Account #: {num}")
            print(f"Type: {acc.type}")
            print(f"Balance: ${acc.balance:.2f}")
            print("-" * 30) 
        print("=" * 30)


def run_account_submenu(account):
    while True:
        print(f"\nAccount selected: {account.owner_name} ({account.account_number})")
        print("[1] Deposit")
        print("[2] Withdraw")
        
        if isinstance(account, SavingsAccount):
            print("[3] Apply Monthly Interest\n[4] View Details\n[5] Back to Main Menu")
        elif isinstance(account, InvestmentAccount):
            print("[3] Apply Investment Growth\n[4] View Details\n[5] Back to Main Menu")
        else:  
            print("[3] View Details\n[4] Back to Main Menu")

        choice = input("\n> ").strip()

        try:
            match choice:
                case '1':
                    amount = float(input("Deposit amount: "))
                    account.deposit(amount)

                case '2':
                    amount = float(input("Withdrawal amount: "))
                    account.withdraw(amount)
                case '3':
                    match account:
                        case _ if isinstance(account, SavingsAccount):

                            account.apply_interest()
                        case _ if isinstance(account, InvestmentAccount):


                            rate = float(input("Enter investment rate: "))
                            account.apply_growth(rate)
                        case _:
                            account.display()
                case '4':
                    match account:
                        case _ if isinstance(account, SavingsAccount) or isinstance(account, InvestmentAccount):
                            account.display()
                        case _:
                            break 

                case '5' if isinstance(account, SavingsAccount) or isinstance(account, InvestmentAccount):
                    break
                case _:
                    print("Invalid option. Please try again.")
                    
        except ValueError as e:
            if "could not convert string to float" in str(e):
                print("Error: Enter a valid number for amount.")

            else:
                print(f"Error: {e}")
        except PermissionError as e:
            print(f"{e}")


def main():
    bank = Bank()
    print("-" * 30)

    print("   Welcome to PyBank CLI")
    print("-" * 30)

    while True:
        print("\n[1] Open a new account")
        print("[2] Select an account")
        print("[3] List all accounts")
        print("[4] Quit")
        
        choice = input("\n> ").strip()

        match choice:
            case '1':
                print("\nAccount type:")
                print("[1] Checking")
                print("[2] Savings")
                print("[3] Investment")
                type_choice = input("> ").strip()

                if type_choice not in ['1', '2', '3']:
                    print("Select a valid account type.")
                    continue

                owner = input("Owner name: ").strip()
                if not owner:
                    print("Error: Owner name cannot be left blank.")
                    continue

                acc_num = input("Enter unique account number: ").strip()
                if not acc_num:

                    print("Error: Account number cannot be left blank.")
                    continue

                try:
                    opening_balance = float(input("Opening balance: "))
                    if opening_balance < 0:
                        print("Error: Balance cannot start negative.")
                        continue
                except ValueError:
                    print("Error: Opening balance must be a valid number.")
                    continue

                match type_choice:

                    case '1':
                        new_acc = CheckingAccount(owner, opening_balance, acc_num)
                    case '2':
                        new_acc = SavingsAccount(owner, opening_balance, acc_num)
                    case '3':
                        if opening_balance < 5000:
                            print("Error: Investment accounts require a minimum starting balance of $5000.00.")
                            continue
                        new_acc = InvestmentAccount(owner, opening_balance, acc_num)

                bank.open_account(new_acc)
                print("-" * 30)

            case '2':
                acc_num = input("Enter account number: ").strip()
                print("-" * 30)
                account = bank.lookup_account(acc_num)
                if account:
                    run_account_submenu(account)
                else:
                    print("Error: Account not found.")

            case '3':
                bank.list_accounts()

            case '4':
                print("\nGoodbye!")
                break
            case _:
                print("Please select a valid option.")


if __name__ == "__main__":
    main()