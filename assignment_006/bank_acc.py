# bank_acc.py
from time import sleep

# create an account class
class Account:
    def __init__(self, owner, account_number, balance=0):
        self.owner = owner
        self.account_number = account_number
        self._balance = balance     # encapsulation --> internal var and cannot change. only way to change is by depositing and withdrawing money

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive!")
        self._balance += amount

    def get_balance(self):
        return self._balance

    def display(self):
        print(f"Account Owner       = {self.owner}")
        print(f"Account Number      = {self.account_number}")
        print(f"Balance             = {self._balance:.2f}")



class CheckingAccount(Account):
    def __init__(self, owner, account_number, balance=0, overdraft_limit=100):
        super().__init__(owner, account_number, balance)
        self.overdraft_limit = overdraft_limit
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal much be positive!")
        if amount > self._balance + self.overdraft_limit:
            raise InsufficientFundsError(f"Exceeds overdraft limit of ${self.overdraft_limit:.2f}.")
        self._balance -= amount



class InvestmentAccount(Account):
    def __init__(self, owner, account_number, balance=0, minimum_balance=1000, return_rate=0.05):
        super().__init__(owner, account_number, balance)
        self.minimum_balance = minimum_balance
        self.return_rate = return_rate
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal much be positive!")
        
        if self._balance - amount < self.minimum_balance:
            raise InsufficientFundsError(f"Insufficient funds. Balance is ${self._balance:.2f}.")
        
        self._balance -= amount
    
    def apply_return(self, rate=None):
        rate = rate if rate is not None else self.return_rate
        self._balance += self._balance * rate
        
            

class SavingsAccount(Account):
    def __init__(self, owner, account_number, balance=0, interest_rate=0.025, withdrawal_limit=3):
        super().__init__(owner, account_number, balance)
        self.interest_rate = interest_rate
        self.withdrawal_limit = withdrawal_limit
        self.withdrawal_count = 0       # to count the number of withdrawals made so far
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal much be positive!")

        if self.withdrawal_count >= self.withdrawal_limit:
            raise WithdrawalLimitError(f"Cannot process... You are at your withdrawal limit of {self.withdrawal_limit} this month.")
        
        if amount > self._balance:
            raise InsufficientFundsError(f"Insufficient funds. Balance is ${self._balance:.2f}.")

        
        self._balance -= amount
        self.withdrawal_count += 1
    
    def apply_interest(self):
        self._balance += self._balance * self.interest_rate



class BankError(Exception):
    # parent class for banking error
    pass

class InsufficientFundsError(BankError):
    pass

class WithdrawalLimitError(BankError):
    pass

class MinimumBalanceError(BankError):
    pass

class Bank:
    def __init__(self):
        self.accounts = {}
        self._counter = 0

    def open_account(self, acc_type, owner, balance=0):
        self._counter += 1
        pre = {"checking" : "CHK", "savings" : "SAV", "investment" : "INV"}[acc_type]
        number = f"{pre}-{self._counter:05d}"
        
        if acc_type == "checking":
            account = CheckingAccount(owner, number, balance)
        elif acc_type == "savings":
            account = SavingsAccount(owner, number, balance)
        else:
            account = InvestmentAccount(owner, number, balance)
        
        self.accounts[number] = account

        return account

    def find_acc(self, number):
        return self.accounts.get(number)
    
    def list_accs(self):
        if not self.accounts:
            print("No open accounts yet.")
            return
        
        for number, account in self.accounts.items():
            print(f"{number}  |  {account.owner}  |  ${account.get_balance():.2f}")



def clear_console():
    print("\033[2J\033[H", end="", flush=True)



def main():
    bank = Bank()

    while True:
        clear_console()
        print("_____________________")
        print("Welcome to the Bank")
        print("_____________________")

        print("[1] Open New Account")
        print("[2] Select An Account")
        print("[3] List All Accounts")
        print("[4] Quit")

        print("Please select an option from above.")

        try:
            user_choice = int(input("> "))
        except ValueError:
            print("Please enter a number.")
            continue

        if user_choice == 1:
            while True: 
                clear_console()
                print("Account Type:")
                print("[1] Checking")
                print("[2] Savings")
                print("[3] Investment")
                print("[4] Back")

                print("Please select an option from above.")

                try:
                    user_acc = int(input("> "))
                except ValueError:
                    print("Please enter a number.")
                    continue

                type_map = {1: "checking", 2: "savings", 3: "investment"}
                if user_acc == 4:
                    break
                
                elif user_acc in type_map:
                    owner = input("Owner Name: ")

                    try:
                        balance = float(input("Opening balance: "))
                    except ValueError:
                        print("Balance must be a number.")
                        continue
                    
                    account = bank.open_account(type_map[user_acc], owner, balance)
                    print(f"\nOpened {account.account_number} for {owner}!")
                    sleep(2)
                    break
                else:
                    print("Invalid opton.")


        elif user_choice == 2:
            clear_console()
            print("What's the account number you are tyring to look up? ")
            acc_number = input("> ").strip().upper()
            account = bank.find_acc(acc_number)

            if account is None:
                print("No account found with that number.")
                sleep(2)
                continue

            while True:
                clear_console()
                print(f"Selected: {account.owner} ({account.account_number})\n")
                print("[1] Deposit")
                print("[2] Withdraw")
                print("[3] View Details")

                if isinstance(account, SavingsAccount):
                    print("[4] Apply Monthly Interest")
                elif isinstance(account, InvestmentAccount):
                    print("[4] Apply Return")
                print("[5] Back to Main Menu")

                try:
                    sub = int(input("> "))
                except ValueError:
                    print("Please enter a valid number.")
                    continue

                
                if sub == 1:
                    try:
                        amount = float(input("Deposit amount: "))
                        account.deposit(amount)
                        print(f"Deposited ${amount:.2f}. New balance: ${account.get_balance():.2f}")
                    except ValueError:
                        print("Please enter a valid floating point number.")
                    except BankError as e:
                        print(f"Error: {e}")
                    sleep(2)

                elif sub == 2:
                    try:
                        amount = float(input("Withdrawal amount: "))
                        account.withdraw(amount)
                        print(f"Withdrew ${amount:.2f}. New balance: ${account.get_balance():.2f}")
                    except ValueError:
                        print("Please enter a valid floating point number.")
                    except BankError as e:
                        print(f"Error: {e}")
                    sleep(2)

                elif sub == 3:
                    clear_console()
                    account.display()
                    input("\nPress Enter to go back to the menu...")
                
                elif sub == 4 and isinstance(account, SavingsAccount):
                    account.apply_interest()
                    print(f"Interest applied. New balance: ${account.get_balance():.2f}")
                elif sub == 4 and isinstance(account, InvestmentAccount):
                    account.apply_return()
                    print(f"Return applied. New balance: ${account.get_balance():.2f}")
                elif sub == 5:
                    break

                else:
                    print("Please enter a valid input")
            
            
        elif user_choice == 3:
            clear_console()
            bank.list_accs()


        elif user_choice == 4:
            clear_console()
            print("Bye! Thanks for visiting :)")
            break

        else:
            print("Sorry, I couldn't recognize that choide. Please enter a valid input")


if __name__ == "__main__":
    main()
