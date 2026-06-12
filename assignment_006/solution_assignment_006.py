MAX_OVERDRAFT = 200.00
MAX_WITHDRAWAL = 3
INTEREST_RATE = 0.05
MIN_BALANCE = 500

class Account:
    def __init__(self, owner_name, account_num, balance, type):
        self.owner_name = owner_name
        self.account_num = account_num
        self.balance = float(balance)
        self.type = type
    
    # display method: overridden by checking, saving, investment
    def AccountDetails(self):
        print(f"Owner       : {self.owner_name}")
        print(f"Account #   : {self.account_num}")
        print(f"Balance     : {self.balance}")

    # deposit method
    def Deposit(self, amount):
        try:
            amount = round(float(amount), 2)
        except ValueError:
            raise ValueError("Amount needs to be a number.")
        
        if amount <= 0:
            raise ValueError("Amount cannot be 0 or negative.")
        else:
            self.balance += amount

class CheckingAccount(Account):
    def __init__(self, owner_name, account_num, balance):
        super().__init__(owner_name, account_num, balance, "Checking")
        self.avail_overdraft = MAX_OVERDRAFT

    # display method: overwrites parent class
    def AccountDetails(self):
        print("---------------------------------------")
        print("            ACCOUNT DETAILS            ")
        print("---------------------------------------")
        print(f"Owner               : {self.owner_name}")
        print(f"Account #           : {self.account_num}")
        print(f"Type #              : {self.type}")
        print(f"Balance             : ${self.balance:.2f}")
        print(f"Available Overdraft : ${self.avail_overdraft:.2f} out of ${MAX_OVERDRAFT:.2f} left")
        print("---------------------------------------")

    def Withdraw(self, amount):
        try:
            amount = round(float(amount), 2)
        except ValueError:
            raise ValueError("Amount needs to be a number.")
        
        if amount <= 0:
            raise ValueError("Amount cannot be 0 or negative.")
        elif amount > (self.balance + self.avail_overdraft):
            raise ValueError(f"Resulting balance cannot be beyond the available overdraft (${self.avail_overdraft:0.2f}).")
        else:
            if self.balance != 0:
                if self.balance - amount < 0:
                    self.avail_overdraft = self.avail_overdraft - (amount - self.balance)
                    self.balance = 0     
                else:
                    self.balance -= amount           
            else: self.avail_overdraft -= amount
            print(f"Successfully withdrew ${amount:.2f}.")

class SavingsAccount(Account):
    def __init__(self, owner_name, account_num, balance):
        super().__init__(owner_name, account_num, balance, "Savings")
        self.monthly_withdrawals = MAX_WITHDRAWAL
    
    # display method: overwrites parent class
    def AccountDetails(self):
        print("---------------------------------------")
        print("            ACCOUNT DETAILS            ")
        print("---------------------------------------")
        print(f"Owner               : {self.owner_name}")
        print(f"Account #           : {self.account_num}")
        print(f"Type #              : {self.type}")
        print(f"Balance             : ${self.balance:.2f}")
        print(f"Withdrawals         : {self.monthly_withdrawals}/{3} left")
        print(f"Interest Rate       : {INTEREST_RATE * 100:.2f}% monthly")
        print("---------------------------------------")

    def Withdraw(self, amount):
        try:
            amount = round(float(amount), 2)
        except ValueError:
            raise ValueError("Amount needs to be a number.")
        
        if (self.monthly_withdrawals - 1) < 0:
            raise ValueError(f"Monthly withdrawals cannot exceed {MAX_WITHDRAWAL}.")
        elif amount <= 0:
            raise ValueError("Amount cannot be 0 or negative.")
        elif (self.balance - amount) < 0:
            raise ValueError("Resulting balance cannot be less than 0.")
        else:
            self.monthly_withdrawals -= 1
            self.balance -= amount
            print(f"Successfully withdrew ${amount:.2f}.")

    def ApplyInterest(self):
        interest = 1 + INTEREST_RATE
        self.balance += interest
        print(f"Successfully applied interest rate of {(INTEREST_RATE * 100):.2f}%. New balance is ${self.balance:.2f}")

class InvestmentAccount(Account):
    def __init__(self, owner_name, account_num, balance):
        super().__init__(owner_name, account_num, balance, "Investment")  
    
    # display method: overwrites parent class
    def AccountDetails(self):
        print("---------------------------------------")
        print("            ACCOUNT DETAILS            ")
        print("---------------------------------------")
        print(f"Owner               : {self.owner_name}")
        print(f"Account #           : {self.account_num}")
        print(f"Type #              : {self.type}")
        print(f"Balance             : ${self.balance:.2f}")
        print(f"Account Minimum     : ${MIN_BALANCE}")
        print("---------------------------------------")

    def Withdraw(self, amount):
        try:
            amount = round(float(amount), 2)
        except ValueError:
            raise ValueError("Amount needs to be a number.")

        if amount <= 0:
            raise ValueError("Amount cannot be 0 or negative.")
        elif (self.balance - amount) < MIN_BALANCE:
            raise ValueError(f"Resulting balance cannot be less than {MIN_BALANCE:0.2f}.")
        else:
            self.balance -= amount
            print(f"Successfully withdrew ${amount:.2f}.")

    def ApplyReturn(self, rate):
        if not rate.isdigit():
            raise ValueError("Rate needs to be a number.")
        else:
            rate = int(rate)
            if rate <= 0:
                raise ValueError("Rate cannot be 0 or negative.")
            else:
                convert_rate = 1 + (rate / 100)
                self.balance += convert_rate  
                print(f"Successfully applied return rate of {rate:.2f}%.")

class Bank:
    def __init__(self):
        self.accounts = []
        self.curr_che_num = 0
        self.curr_sav_num = 0 
        self.curr_inv_num = 0 
    
    def AccountNumCreation(self, type):
        s = ""
        if type == "C":
            s = f"CHE-{self.curr_che_num:05d}"
            self.curr_che_num += 1
        elif type == "S":
            s = f"SAV-{self.curr_sav_num:05d}"
            self.curr_sav_num += 1
        elif type == "I":
            s = f"INV-{self.curr_inv_num:05d}"
            self.curr_inv_num += 1
        return s

    # opening new accounts
    def OpenChecking(self, owner_name):
        acct = CheckingAccount(owner_name, self.AccountNumCreation("C"), 0)
        acct.AccountDetails()
        self.accounts.append(acct)

    def OpenSavings(self, owner_name):
        acct = SavingsAccount(owner_name, self.AccountNumCreation("S"), 0)
        acct.AccountDetails()
        self.accounts.append(acct)

    def OpenInvestment(self, owner_name):
        acct = InvestmentAccount(owner_name, self.AccountNumCreation("I"), MIN_BALANCE)
        acct.AccountDetails()
        self.accounts.append(acct)

    # look up account by account num
    def Lookup(self, num):
        for a in self.accounts:
            if a.account_num == num:
                print(f"Account selected: {a.owner_name} ({a.account_num})")
                return a
        raise LookupError(f"Account \"{num}\" not found.")
    
    # lists all accounts w/ types and balances
    def ListAllAccounts(self):
        if len(self.accounts) == 0:
            raise LookupError("No accounts have been made.")
        else:
            print("-----------------------------------")
            print("   ACCOUNT NUM   |     BALANCE")
            print("-----------------------------------")
            for a in self.accounts:
                print(f"    {a.account_num}    |     ${a.balance:.2f}")
            print("-----------------------------------")
            print(f"Printed {len(self.accounts)} account(s).")

def BankInteract():
    bank = Bank()

    while True:
        print("=======================================")
        print("          Welcome to Bank CLI          ")
        print("=======================================")
        print(" [1] Open a new account")
        print(" [2] Select an account")
        print(" [3] List all accounts")
        print(" [4] Quit")
        inp = input("Enter an option to proceed (1, 2, 3, 4): ")
        print("=======================================")

        match inp:
            case "1":
                print("ACCOUNT TYPES:")
                print(" [1] Checking")
                print(" [2] Savings")
                print(" [3] Investment")
                inp = input("Choose an account type to create (1, 2, or 3): ")
                match inp:
                    case "1":
                        inp = input("Enter the name for the account: ")
                        bank.OpenChecking(inp)
                        print(f"Successfully created account for \"{inp}\".")
                    case "2":
                        inp = input("Enter the name for the account: ")
                        bank.OpenSavings(inp)
                        print(f"Successfully created account for \"{inp}\".")
                    case "3":
                        inp = input("Enter the name for the account: ")
                        bank.OpenInvestment(inp)
                        print(f"Successfully created account for \"{inp}\".")
                    case _:
                        print("Cancelling account creation. Going back to main menu.")
                print("=======================================")
            case "2":
                inp = input("Enter the account number you would like to search for: ")
                acct = bank.Lookup(inp)

                while True:
                    if acct.type == "Checking":
                        print(" [1] Deposit")
                        print(" [2] Withdraw")
                        print(" [3] View Details")
                        inp = input("Enter an option to proceed (1, 2, 3, or 4): ")

                        match inp:
                            case "1":
                                inp = input("Enter an amount to deposit: ")
                                acct.Deposit(inp)
                            case "2":
                                inp = input("Enter an amount to withdraw: ")
                                acct.Withdraw(inp)
                            case "3":
                                acct.AccountDetails()
                            case _:
                                print("Going back to main menu.")
                                print("=======================================")
                                break
                    elif acct.type == "Savings":
                        print(" [1] Deposit")
                        print(" [2] Withdraw")
                        print(" [3] Apply Monthly Interest")
                        print(" [4] View Details")
                        inp = input("Enter an option to proceed (1, 2, 3, 4, or 5): ")

                        match inp:
                            case "1":
                                inp = input("Enter an amount to deposit: ")
                                acct.Deposit(inp)
                            case "2":
                                inp = input("Enter an amount to withdraw: ")
                                acct.Withdraw(inp)
                            case "3":
                                acct.ApplyInterest()
                            case "4":
                                acct.AccountDetails()
                            case _:
                                print("Going back to main menu.")
                                print("=======================================")
                                break
                    elif acct.type == "Investment":
                        print(" [1] Deposit")
                        print(" [2] Withdraw")
                        print(" [3] Apply Return Rate")
                        print(" [4] View Details")
                        inp = input("Enter an option to proceed (1, 2, 3, 4, or 5): ")
                        
                        match inp:
                            case "1":
                                inp = input("Enter an amount to deposit: ")
                                acct.Deposit(inp)
                            case "2":
                                inp = input("Enter an amount to withdraw: ")
                                acct.Withdraw(inp)
                            case "3":
                                inp = input("Enter a rate to apply to your balance (1-100): ")
                                acct.ApplyReturn(inp)
                            case "4":
                                acct.AccountDetails()
                            case _:
                                print("Going back to main menu.")
                                print("=======================================")
                                break
            case "3":
                bank.ListAllAccounts()
                print("=======================================")
            case "4":
                print("Thank you for banking with us. Securely logging you out.")
                break

BankInteract()
        