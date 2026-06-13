from datetime import datetime
import json

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
        self.history = []
    
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
            self.balance = round(self.balance + amount, 2)
            self.history.append(["Deposit", amount, str(datetime.now())])
            print(f"Successfully deposited ${amount:0.2f}.")

    # view history
    def ViewHistory(self):
        if not self.history:
            raise LookupError("No transaction history has been made.")
        else:   
            print("---------------------------------------")
            print("                HISTORY                ")
            print("---------------------------------------")
            for entry in self.history:
                print(f"{entry[0]}, {entry[1]}, DATE/TIME: {entry[2]}")
            print("---------------------------------------")
            print(f"Successfully printed {len(self.history)} entries.")

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

    def WithdrawHelper(self, amount):
        try:
            amount = round(float(amount), 2)
        except ValueError:
            raise ValueError("Amount needs to be a number.")
        
        if amount <= 0:
            raise ValueError("Amount cannot be 0 or negative.")
        elif amount > (self.balance + self.avail_overdraft):
            raise ValueError(f"Resulting balance cannot be beyond the available overdraft (${self.avail_overdraft:0.2f}).")
    
        return amount

    def Withdraw(self, amount):
        if self.balance != 0:
            if self.balance - amount < 0:
                self.avail_overdraft = round(self.avail_overdraft - (amount - self.balance), 2)
                self.balance = 0     
            else:
                self.balance = round(self.balance - amount, 2)
        else: 
            self.avail_overdraft = round(self.avail_overdraft - amount, 2)
        self.history.append(["Withdrawal", amount, str(datetime.now())])
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

    def WithdrawHelper(self, amount):
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
        
        return amount

    def Withdraw(self, amount):
        self.monthly_withdrawals -= 1
        self.balance = round(self.balance - amount, 2)
        self.history.append(["Withdrawal", amount, str(datetime.now())])
        print(f"Successfully withdrew ${amount:.2f}.")

    def ApplyInterest(self):
        earned = round(INTEREST_RATE * self.balance, 2)
        self.balance = round(self.balance + earned, 2)
        self.history.append(["Applied interest", earned, str(datetime.now())])
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
        print(f"Account Minimum     : ${MIN_BALANCE:0.2f}")
        print("---------------------------------------")

    def WithdrawHelper(self, amount):
        try:
            amount = round(float(amount), 2)
        except ValueError:
            raise ValueError("Amount needs to be a number.")

        if amount <= 0:
            raise ValueError("Amount cannot be 0 or negative.")
        elif (self.balance - amount) < MIN_BALANCE:
            raise ValueError(f"Resulting balance cannot be less than {MIN_BALANCE:0.2f}.")
        
        return amount

    def Withdraw(self, amount):
        self.balance = round(self.balance - amount, 2)
        self.history.append(["Withdrawal", amount, str(datetime.now())])
        print(f"Successfully withdrew ${amount:.2f}.")

    def ApplyReturn(self, rate):
        try:
            rate = round(float(rate), 2)
        except ValueError:
            raise ValueError("Rate needs to be a number.")

        if rate < -100 or rate > 100:
            raise ValueError("Rate cannot be less than -100 or greater than 100.")
        else:
            earned = round((rate / 100) * self.balance, 2)
            self.balance = round(self.balance + earned, 2)
            self.history.append(["Applied return", earned, str(datetime.now())])
            print(f"Successfully applied return rate of {rate:.2f}%.")

class Bank:
    def __init__(self):
        self.accounts = []
        self.auth_table = dict()
        self.curr_che_num = 0
        self.curr_sav_num = 0 
        self.curr_inv_num = 0 
    
    # in the format of CHE-00000
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

    def CreateAccount(self, user, pw):
        if user in self.auth_table:
            raise ValueError(f"User already exists. Unable to create account.")
        else: self.auth_table[user] = pw

    def LoginCred(self, user, pw):
        if user not in self.auth_table:
            raise LookupError(f"User \"{user}\" not found.")
        if self.auth_table[user] != pw:
            raise ValueError(f"Username or password is incorrect.")
        print("Successful log in!")

    def SaveData(self, filename="bank_data.json"):
        data = {
            "accounts": [],
            "auth_table": self.auth_table
        }

        for acct in self.accounts:
            acct_data = {
                "owner_name": acct.owner_name,
                "account_num": acct.account_num,
                "balance": acct.balance,
                "type": acct.type,
                "history": acct.history
            }

            if isinstance(acct, CheckingAccount):
                acct_data["avail_overdraft"] = acct.avail_overdraft
            elif isinstance(acct, SavingsAccount):
                acct_data["monthly_withdrawals"] = acct.monthly_withdrawals
            data["accounts"].append(acct_data)

        with open(filename, "w") as file:
            json.dump(data, file)

    def LoadData(self, filename="bank_data.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"{filename} does not exist.")
        
        self.accounts = []
        self.auth_table = data["auth_table"]

        for acct in data["accounts"]:
            if acct["type"] == "Checking":
                acct_data = CheckingAccount(acct["owner_name"], acct["account_num"], acct["balance"])
                acct_data.avail_overdraft = acct["avail_overdraft"]
            elif acct["type"] == "Savings":
                acct_data = SavingsAccount(acct["owner_name"], acct["account_num"], acct["balance"])
                acct_data.monthly_withdrawals = acct["monthly_withdrawals"]
            elif acct["type"] == "Investment":
                acct_data = InvestmentAccount(acct["owner_name"], acct["account_num"], acct["balance"])
            acct_data.history = acct["history"]
            self.accounts.append(acct_data)
    

def BankInteract():
    bank = Bank()
    try:
        bank.LoadData()
    except FileNotFoundError as e:
        print(f"Error: {e}")

    # login menu
    while True:
        print("=======================================")
        print("          Login to Bank CLI           ")
        print("=======================================")
        print(" [1] Create an account")
        print(" [2] Login")
        print(" [3] Quit")
        inp = input("Enter an option to proceed (1, 2, or 3): ")

        match inp:
            case "1":
                inp_user = input("Enter username: ")
                inp_pass = input("Enter password: ")
                try:
                    bank.CreateAccount(inp_user, inp_pass)
                except ValueError as e:
                    print(f"Error: {e}")
            case "2":
                inp_user = input("Enter username: ")
                inp_pass = input("Enter password: ")
                try:
                    bank.LoginCred(inp_user, inp_pass)
                    
                    # logged in, allows access to Bank CLI
                    while True:
                        print("=======================================")
                        print("          Welcome to Bank CLI          ")
                        print("=======================================")
                        print(" [1] Open a new account")
                        print(" [2] Select an account")
                        print(" [3] List all accounts")
                        print(" [4] Account transfers")
                        print(" [5] Monthly Reset Simulation")
                        print(" [6] Logout")
                        inp = input("Enter an option to proceed (1, 2, 3, 4, 5, or 6): ")
                        print("=======================================")

                        match inp:
                            case "1":
                                print("ACCOUNT TYPES:")
                                print(" [1] Checking")
                                print(" [2] Savings")
                                print(" [3] Investment")
                                print(" [4] Return to main menu")
                                inp = input("Choose an account type to create (1, 2, 3, or 4): ")
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
                                        print("Cancelling account creation. Returning to main menu.")
                                print("=======================================")
                            case "2":
                                inp = input("Enter the account number you would like to search for: ")
                                try:
                                    acct = bank.Lookup(inp)
                                except LookupError as e:
                                    print(f"Error: {e}")
                                    continue

                                while True:
                                    if isinstance(acct, CheckingAccount):
                                        print(" [1] Deposit")
                                        print(" [2] Withdraw")
                                        print(" [3] View Details")
                                        print(" [4] View Transaction History")
                                        print(" [5] Return to main menu")
                                        inp = input("Enter an option to proceed (1, 2, 3, 4, or 5): ")

                                        match inp:
                                            case "1":
                                                inp = input("Enter an amount to deposit: ")
                                                try:
                                                    acct.Deposit(inp)
                                                except ValueError as e:
                                                    print(f"Error: {e}")
                                            case "2":
                                                inp = input("Enter an amount to withdraw: ")
                                                try:
                                                    acct.Withdraw(acct.WithdrawHelper(inp))
                                                except ValueError as e:
                                                    print(f"Error: {e}")
                                            case "3":
                                                acct.AccountDetails()
                                            case "4":
                                                try:
                                                    acct.ViewHistory()
                                                except LookupError as e:
                                                    print(f"Error: {e}")
                                            case _:
                                                print("Returning to main menu.")
                                                print("=======================================")
                                                break
                                        print("=======================================")
                                    elif isinstance(acct, SavingsAccount):
                                        print(" [1] Deposit")
                                        print(" [2] Withdraw")
                                        print(" [3] Apply Monthly Interest")
                                        print(" [4] View Details")
                                        print(" [5] View Transaction History")
                                        print(" [6] Return to main menu")
                                        inp = input("Enter an option to proceed (1, 2, 3, 4, 5, 6): ")

                                        match inp:
                                            case "1":
                                                inp = input("Enter an amount to deposit: ")
                                                try:
                                                    acct.Deposit(inp)
                                                except ValueError as e:
                                                    print(f"Error: {e}")
                                            case "2":
                                                inp = input("Enter an amount to withdraw: ")
                                                try:
                                                    acct.Withdraw(acct.WithdrawHelper(inp))
                                                except ValueError as e:
                                                    print(f"Error: {e}")
                                            case "3":
                                                acct.ApplyInterest()
                                            case "4":
                                                acct.AccountDetails()
                                            case "5":
                                                try:
                                                    acct.ViewHistory()
                                                except LookupError as e:
                                                    print(f"Error: {e}")
                                            case _:
                                                print("Returning to main menu.")
                                                print("=======================================")
                                                break
                                        print("=======================================")
                                    elif isinstance(acct, InvestmentAccount):
                                        print(" [1] Deposit")
                                        print(" [2] Withdraw")
                                        print(" [3] Apply Return Rate")
                                        print(" [4] View Details")
                                        print(" [5] View Transaction History")
                                        print(" [6] Return to main menu")
                                        inp = input("Enter an option to proceed (1, 2, 3, 4, 5, 6): ")
                                        
                                        match inp:
                                            case "1":
                                                inp = input("Enter an amount to deposit: ")
                                                try:
                                                    acct.Deposit(inp)
                                                except ValueError as e:
                                                    print(f"Error: {e}")
                                            case "2":
                                                inp = input("Enter an amount to withdraw: ")
                                                try:
                                                    acct.Withdraw(acct.WithdrawHelper(inp))
                                                except ValueError as e:
                                                    print(f"Error: {e}")
                                            case "3":
                                                inp = input("Enter a rate to apply to your balance (1-100): ")
                                                try:
                                                    acct.ApplyReturn(inp)
                                                except ValueError as e:
                                                    print(f"Error: {e}")
                                            case "4":
                                                acct.AccountDetails()
                                            case "5":
                                                try:
                                                    acct.ViewHistory()
                                                except LookupError as e:
                                                    print(f"Error: {e}")
                                            case _:
                                                print("Returning to main menu.")
                                                print("=======================================")
                                                break
                                        print("=======================================")
                            case "3":
                                try:
                                    bank.ListAllAccounts()
                                except LookupError as e:
                                    print(f"Error: {e}")
                                print("=======================================")
                            case "4":
                                inp_1 = input("Enter the account number to transfer from: ")
                                try:
                                    acct_1 = bank.Lookup(inp_1)
                                except LookupError as e:
                                    print(f"Error: {e}")
                                    continue
                                
                                inp_2 = input("Enter the account number to transfer to: ")
                                try:
                                    acct_2 = bank.Lookup(inp_2)
                                except LookupError as e:
                                    print(f"Error: {e}")
                                    continue

                                inp_3 = input("Enter how much you want to transfer: ")
                                try: 
                                    acct_1.Withdraw(acct_1.WithdrawHelper(inp_3))
                                    acct_2.Deposit(inp_3)
                                    print(f"Successfully transferred ${inp_3}.")
                                except ValueError as e:
                                    print(f"Error: {e}")            
                            case "5":
                                for acct in bank.accounts:
                                    print("-----------------------------------")
                                    print("   ACCOUNT NUM   |     BALANCE")
                                    print("-----------------------------------")
                                    print(f"    {acct.account_num}    |     ${acct.balance:.2f}")
                                    print("-----------------------------------")

                                    if isinstance(acct, SavingsAccount):
                                        acct.monthly_withdrawals = MAX_WITHDRAWAL
                                        acct.ApplyInterest()
                                    elif isinstance(acct, InvestmentAccount):
                                        inp = input("Enter a rate to apply to your balance (-100 to 100): ")
                                        try:
                                            acct.ApplyReturn(inp)
                                        except ValueError as e:
                                            print(f"Error: {e}")
                                print(f"Successfully printed {len(bank.accounts)} account(s).")
                            case "6":
                                print("Thank you for banking with us. Securely logging you out.")
                                break
                except (LookupError, ValueError) as e:
                    print(f"Error: {e}")
            case "3":
                bank.SaveData()
                print("Thank you for banking with us. Exiting application.")
                break

BankInteract()
        