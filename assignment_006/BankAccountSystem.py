class Account:
    
    def __init__(self, name, account_number, balance):
        if balance < 0:
            raise Exception ("Must start with a positive balance.")
        self.name = name
        self.account_number = account_number
        self.balance = balance
        print(f"Account Successfully created. Account Number: {self.account_number:05d}")

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited ${amount:.2f}. New balance: ${self.balance:,.2f}")
        
    def display_details(self):
        return (f"Name on account: {self.name}\nAccount Number: {self.account_number:05d}\n" \
                f"Balance: ${self.balance:,.2f}\n")


class CheckingAccount(Account):
    
    overdraft = 100

    def withdraw(self, amount):
        if self.balance + self.overdraft < amount:
            raise Exception ("Cannot withdraw. Overdraft limit exceeded")
        
        self.balance -= amount
        print (f"Withdrawal successful. New balance: ${self.balance:,.2f}")

    def display_details(self):
        print (f"{super().display_details()}Overdraft Limit: ${self.overdraft:,.2f}\n")
    
    def options(self):
        while True:
            print("1. Deposit\n2. Withdraw\n3. View Details\n4. Main Menu")
            choice = input("Choose an option: ")

            match choice:
                case "1":
                    amount = float(input("Enter the amount you want to deposit: "))
                    self.deposit(amount)

                case "2":
                    amount = float(input("Enter the amount you want to withdraw: "))
                    self.withdraw(amount)

                case "3":
                    self.display_details()

                case "4":
                    break

class SavingsAccount(Account):
    interest_rate = 0.025
    withdraw_count = 0
    withdraw_limit = 2

    def apply_interest(self):
        self.balance += self.balance * self.interest_rate
        print(f"Monthly interest applied. New balance: ${self.balance:,.2f}")

    def withdraw(self, amount):
        if self.withdraw_count >= self.withdraw_limit:
            raise Exception ("Withdrawal limit reached for this month.")
        if self.balance < amount:
            raise Exception ("Cannot withdraw: not enough funds in account.")
        self.balance -= amount
        self.withdraw_count += 1
        print(f"New balance: ${self.balance:,.2f}")

    def display_details(self):
        print (f"{super().display_details()}Type: Savings\nWithdrawals: {self.withdraw_count}/{self.withdraw_limit}\n"\
                f"Interest: {self.interest_rate * 100.0}%\n")
    
    def options(self):
        while True:
            print("1. Deposit\n2. Apply Interest\n3. Withdraw\n4. View Details\n5. Main Menu")
            choice = input("Choose an option: ")

            match choice:
                case "1":
                    amount = float(input("Enter the amount you want to deposit: "))
                    self.deposit(amount)

                case "2":
                    self.apply_interest()

                case "3":
                    amount = float(input("Enter the amount you want to withdraw: ")) 
                    self.withdraw(amount)

                case "4":
                    self.display_details()

                case "5":
                    break


class InvestmentAccount(Account):
    minimum_balance = 100

    def __init__(self, name, account_number, balance):
        if (balance < self.minimum_balance):
            raise Exception ("Starting balance less than minimum balance.")
        super().__init__(name, account_number, balance)

    def withdraw(self, amount):
        if self.balance - self.minimum_balance < amount:
            raise Exception ("Cannot withdraw: not enough funds in your account.")
    
        self.balance -= amount
        print (f"Withdrawal successful. New balance: ${self.balance:,.2f}")

    def apply_return_rate(self, rate):
        self.balance += self.balance * rate
        print(f"New balance: ${self.balance:,.2f}")

    def display_details(self):
        print (f"{super().display_details()}Type: Investment\n")
    
    def options(self):
        while True:
            print("1. Deposit\n2. Apply Return\n3. Withdraw\n4. View Details\n5. Main Menu")
            choice = input("Choose an option: ")
            
            match choice:
                case "1":
                    amount = float(input("Enter the amount you want to deposit: "))
                    self.deposit(amount)

                case "2":
                    rate = float(input("Input your return rate: "))
                    self.apply_return_rate(rate)
                
                case "3":
                    amount = float(input("Enter the amount you want to withdraw: "))
                    self.withdraw(amount)

                case "4":
                    self.display_details()
                
                case "5":
                    break


class Bank:
    accounts = []

    def open_account(self, name, balance, type):
        
        account_number = len(self.accounts) + 1

        match type:
            case "1":
                self.accounts.append(CheckingAccount(name, account_number, balance))
            
            case "2":
                self.accounts.append(SavingsAccount(name, account_number, balance))

            case "3":
                self.accounts.append(InvestmentAccount(name, account_number, balance))

            case _:
                raise Exception ("No account type chosen.")

    def select_account(self, number):
        
        for account in self.accounts:
            if account.account_number == number:
                account.display_details()
                account.options()
                return
        
        raise Exception ("Account not found.")

    def display_accounts(self):
        if (not self.accounts):
            raise Exception ("No Accounts")
        for account in self.accounts:
            account.display_details()


bank = Bank()

def open_account():
    try:     
        print("Account Type: \n1. Checking\n2. Saving\n3. Investment")
        type = input("Choose an option: ")
        name = input("Enter your name: ")
        balance = float(input("Enter the opening balance: "))
        bank.open_account(name, balance, type)
    except Exception as e:
        print(e)

def select_account():
    account_number = int(input("Enter your account number: "))
    try:
        bank.select_account(account_number)
    except Exception as e:
        print (e)

def list_accounts():
    try:
        bank.display_accounts()
    except Exception as e:
        print(e)

while True:
    print("1. Open a new account\n2. Select an account\n3. List all accounts\n4. Quit")
    choice = input("Choose an option: ")

    match choice:
        case "1":
            open_account()

        case "2":
            select_account()

        case "3":
            list_accounts()

        case "4":
            break

