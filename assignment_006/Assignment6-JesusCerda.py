# Define exceptions classes
class AvailableFundsExceededError(Exception):
    def __init__(self, amount):
        super().__init__(f"Available funds exceeded! Only {amount} available.")
        self.amount = amount
        
class MonthlyWithdrawalLimitReachedError(Exception):
    def __init__(self, withdraw_lim):
        super().__init__(f"Cannot withdraw more than {withdraw_lim} times!")
        self.withdraw_lim = withdraw_lim

class MinimumBalanceError(Exception):
    def __init__(self, min_bal):
        super().__init__(f"Account balance cannot be below {min_bal}! Transaction not")
        self.min_bal = min_bal

class InvalidAccountError(Exception):
    def __init__(self, account_number):
        super().__init__(f"Cannot find account number {account_number}!")
        
class AccountHasNoInterestRate(Exception):
    def __init__(self, acc_num):
        super().__init__(f"The account number {acc_num} is not an Interest Accruing Account")

# Define classes
class Account:
    def __init__(self, owner_name:str, account_number:str, balance:float):
        self.owner_name = owner_name
        self.account_number = account_number
        self.balance = balance

    def depositMoney(self, deposit_amount): # Returns new balance
        # Ensure the withdrawal is not negative
        if deposit_amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        self.balance += deposit_amount
        return self.balance
    
    def returnAccountDetails(self): # Returns Dict with Account details
        return {"Owner": self.owner_name, "Account #": self.account_number, "Balance": self.balance}
    
    def withdrawMoney(self, withdrawal_amount):
        raise NotImplementedError("Subclasses must implement withdrawMoney()")

class CheckingAccount(Account):
    def __init__(self, owner_name:str, account_number:str, balance:float, overdraft_limit: float):
        super().__init__(owner_name, account_number, balance)
        self.overdraft_limit = overdraft_limit
    
    def withdrawMoney(self, withdrawal_amount): # Returns the new balance
        # Ensure the withdrawal is not negative
        if withdrawal_amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        # Max amount available including overdraft
        available_funds = self.balance + self.overdraft_limit
        
        # Ensure sufficient funds are present'
        if withdrawal_amount > available_funds:
            raise AvailableFundsExceededError(f"{available_funds:.2f}")
        self.balance -= withdrawal_amount
        return self.balance

    def returnAccountDetails(self): # Returns the account details as a Dict
        details = super().returnAccountDetails()
        details["Overdraft Limit"] = self.overdraft_limit
        return details
    
class SavingsAccount(Account):
    def __init__(self, owner_name:str, account_number:str, balance:float, interest_rate:float, withdrawal_limit: int=3):
        super().__init__(owner_name, account_number, balance)
        self.interest_rate = interest_rate
        self.withdrawal_limit = withdrawal_limit
        self.withdrawal_count = 0

    def withdrawMoney(self, withdrawal_amount): # Returns the new balance
        # Ensure the withdrawal is not negative
        if withdrawal_amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        # Ensure we have not hit our max withdrawal count limit
        if self.withdrawal_count >= self.withdrawal_limit:
            raise MonthlyWithdrawalLimitReachedError(str(self.withdrawal_limit))
        
        # Ensure sufficient funds are present
        if withdrawal_amount > self.balance:
            raise AvailableFundsExceededError(f"{self.balance:.2f}")
        self.balance -= withdrawal_amount
        
        # Increase counter and return
        self.withdrawal_count += 1
        return self.balance
    
    def applyMonthlyInterest(self): # Returns the new balance
        if self.balance <= 0:
            return self.balance
        
        interest = self.balance * self.interest_rate
        self.balance += interest
        return self.balance    

    def returnAccountDetails(self):
        details = super().returnAccountDetails()
        details["Withdrawal Limit"] = self.withdrawal_limit
        details["Withdrawals This month"] = self.withdrawal_count
        details["Interest Rate"] = self.interest_rate
        return details

class InvestmentAccount(Account):
    def __init__(self, owner_name: str, account_number: str, balance: float, min_balance: float, base_return_rate: float):
        super().__init__(owner_name, account_number, balance)
        self.min_balance = min_balance
        self.base_return_rate = base_return_rate

    def withdrawMoney(self, withdrawal_amount):
        if withdrawal_amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if self.balance - withdrawal_amount < self.min_balance:
            raise MinimumBalanceError(f"{self.min_balance:.2f}")

        self.balance -= withdrawal_amount
        return self.balance

    def applyReturnRate(self, variable_rate=None):
        rate = self.base_return_rate if variable_rate is None else variable_rate

        if self.balance <= 0:
            return self.balance

        return_amount = self.balance * rate
        self.balance += return_amount
        return self.balance

    def returnAccountDetails(self):
        details = super().returnAccountDetails()
        details["Minimum Balance"] = self.min_balance
        details["Base Return Rate"] = self.base_return_rate
        return details

class Bank:
    def __init__(self):
        self.__accounts = []  # Private list of Account objects
        self.__currentAccNum = 1
    
    # Account Creation    
    def createAccount(self, newAcc:Account):
        self.__accounts.append(newAcc)
        self.__currentAccNum += 1
        return newAcc
        
    def createCheckingAccount(self, owner_name:str, balance:float, overdraft_limit: float): # Returns a new checking account    
        account_number = f"CHK-{self.__currentAccNum:05d}"
        account = CheckingAccount(owner_name, account_number, balance, overdraft_limit)
        return self.createAccount(account)
    
    def createSavingsAccount(self, owner_name:str, balance:float, interest_rate:float, withdrawal_limit: int=3):
        account_number = f"SAV-{self.__currentAccNum:05d}"
        account = SavingsAccount(owner_name, account_number, balance, interest_rate, withdrawal_limit)
        return self.createAccount(account)
    
    def createInvestmentAccount( self, owner_name: str, balance: float, min_balance: float, base_return_rate: float):
        account_number = f"INV-{self.__currentAccNum:05d}"
        account = InvestmentAccount(owner_name, account_number, balance, min_balance, base_return_rate)
        return self.createAccount(account)

    # Account Lookup
    def getAccount(self, account_number:str):
        for account in self.__accounts:
            if account.account_number == account_number:
                return account
        raise InvalidAccountError(account_number)
    
    def getAllAccounts(self):
        return self.__accounts.copy() # Return copy, to ensure internal list is not modified
    
    # Deposits and Withdrawals
    def depositToBank(self, account_number:str, amount:float):
        account = self.getAccount(account_number)
        return account.depositMoney(amount)
    
    def withdrawFromBank(self, account_number:str, amount:float):
        account = self.getAccount(account_number)
        return account.withdrawMoney(amount)
    
    # Apply interest
    def bankAppliesInterest(self, account_num:str, variable_rate=None):
        account = self.getAccount(account_num)
        if isinstance(account, SavingsAccount):
            return account.applyMonthlyInterest()
        elif isinstance(account, InvestmentAccount):
            return account.applyReturnRate(variable_rate)
        else:
            raise AccountHasNoInterestRate

# The main menu interface, packed into a function
def runBankCli(bank):
    print(
        "--------------------------------\n"
        "           Bank System          \n"
        "--------------------------------\n"
        "1. Open a new account\n"
        "2. Select an account\n"
        "3. List all accounts\n"
        "0. Quit\n"
    )
    
    selected_account = None
    
    while True:
        user_input = input(
            "\n--------------------------------\n"
            "Select an option: "
        ).strip()

        if user_input == "0":
            break
        
        elif user_input == "1":  # Open new account
            while True:
                owner_name = input("Owner name: ").strip()
                balance = float(input("Starting balance: ").strip())
                account_type = input("Account type (CHK/SAV/INV): ").strip().upper()

                if account_type == "CHK":
                    account_number = input("Account number (optional or blank for auto): ").strip()
                    if not account_number:
                        overdraft = float(input("Overdraft limit: ").strip())
                        newAcc = bank.createCheckingAccount(owner_name, balance, overdraft)
                        print(f"New Checking Account Created!\nAccount Number: {newAcc.account_number}")
                        break
                    else:
                        overdraft = float(input("Overdraft limit: ").strip())
                        bank.createCheckingAccount(owner_name, balance, overdraft)
                        print("New Checking Account Created!")
                        print(f"New Checking Account Created!\nAccount Number: {newAcc.account_number}")
                        break

                elif account_type == "SAV":
                    account_number = input("Account number (optional or blank for auto): ").strip()
                    rate = float(input("Interest rate (e.g. 0.02): ").strip())
                    withdrawal_limit = int(input("Withdrawal limit (default 3): ") or 3)
                    newAcc = bank.createSavingsAccount(owner_name, balance, rate, withdrawal_limit)
                    print(f"New Savings Account Created!\nAccount Number: {newAcc.account_number}")
                    break

                elif account_type == "INV":
                    min_balance = float(input("Minimum balance: ").strip())
                    base_rate = float(input("Base return rate (e.g. 0.05): ").strip())
                    newAcc = bank.createInvestmentAccount(owner_name, balance, min_balance, base_rate)
                    print(f"New Investment Account Created!\nAccount Number: {newAcc.account_number}")
                    break
                
                elif account_type == "0":
                    print("Account Creation Canceled")
                    break

                else:
                    print("Invalid account type")
                continue

        elif user_input == "2":  # Select account
            account_number = input("Enter account number: ").strip()

            try:
                account = bank.getAccount(account_number)
            except InvalidAccountError as e:
                print(e)
                continue

            selected_account = account
            print(f"Selected: {account.account_number}")

            while True:
                action = input(
                    "\n--- Account Menu ---\n"
                    f"Current Account : {selected_account.account_number}\n"
                    "1. Deposit\n"
                    "2. Withdraw\n"
                    "3. View details\n"
                    "4. Apply Interest\n"
                    "0. Back\n"
                    "Select: "
                ).strip()

                if action == "0":
                    break

                elif action == "1":
                    amount = float(input("Deposit amount: ").strip())
                    try:
                        print(f"New Balance: {bank.depositToBank(selected_account.account_number, amount)}")
                    except Exception as e:
                        print(e)
                    continue

                elif action == "2":
                    amount = float(input("Withdraw amount: ").strip())
                    try:
                        print(f"New Balance: {bank.withdrawFromBank(selected_account.account_number, amount)}")
                    except Exception as e:
                        print(e)
                    continue

                elif action == "3":
                    details = selected_account.returnAccountDetails()
                    print(
                        "\n------------------------------\n"
                        "Account Details\n"
                        "------------------------------"
                    )

                    print(f"Owner       : {details['Owner']}")
                    print(f"Account #   : {details['Account #']}")

                    if isinstance(acc, CheckingAccount):
                        print("Type        : Checking")
                        print(f"Balance     : ${details['Balance']:.2f}")
                        print(f"Overdraft   : ${details['Overdraft Limit']:.2f}")

                    elif isinstance(acc, SavingsAccount):
                        print("Type        : Savings")
                        print(f"Balance     : ${details['Balance']:.2f}")
                        print(
                            f"Withdrawals : "
                            f"{details['Withdrawals This month']}/"
                            f"{details['Withdrawal Limit']} used this month"
                        )
                        print(
                            f"Interest    : "
                            f"{details['Interest Rate'] * 100:.2f}% monthly"
                        )

                    elif isinstance(acc, InvestmentAccount):
                        print("Type        : Investment")
                        print(f"Balance     : ${details['Balance']:.2f}")
                        print(
                            f"Min Balance : "
                            f"${details['Minimum Balance']:.2f}"
                        )
                        print(
                            f"Return Rate : "
                            f"{details['Base Return Rate'] * 100:.2f}%"
                        )
                    print("------------------------------")
                    continue

                elif action == "4":
                    try:
                        variable_rate = None
                        if isinstance(selected_account, InvestmentAccount):
                            variable_rate = input(
                                "Enter return rate or press enter for default: "
                            ).strip()

                            rate = float(variable_rate) if variable_rate else None
                        newAccBalance = bank.bankAppliesInterest(selected_account, rate)
                        print(f"New Balance = {newAccBalance}")

                    except Exception as e:
                        print(e)

                    continue

                else:
                    print("Invalid input")
                    continue

        elif user_input == "3":  # List all accounts
            accounts = bank.getAllAccounts()

            for acc in accounts:
                details = acc.returnAccountDetails()

                print(
                    "\n------------------------------\n"
                    "Account Details\n"
                    "------------------------------"
                )

                print(f"Owner       : {details['Owner']}")
                print(f"Account #   : {details['Account #']}")

                if isinstance(acc, CheckingAccount):
                    print("Type        : Checking")
                    print(f"Balance     : ${details['Balance']:.2f}")
                    print(f"Overdraft   : ${details['Overdraft Limit']:.2f}")

                elif isinstance(acc, SavingsAccount):
                    print("Type        : Savings")
                    print(f"Balance     : ${details['Balance']:.2f}")
                    print(
                        f"Withdrawals : "
                        f"{details['Withdrawals This month']}/"
                        f"{details['Withdrawal Limit']} used this month"
                    )
                    print(
                        f"Interest    : "
                        f"{details['Interest Rate'] * 100:.2f}% monthly"
                    )

                elif isinstance(acc, InvestmentAccount):
                    print("Type        : Investment")
                    print(f"Balance     : ${details['Balance']:.2f}")
                    print(
                        f"Min Balance : "
                        f"${details['Minimum Balance']:.2f}"
                    )
                    print(
                        f"Return Rate : "
                        f"{details['Base Return Rate'] * 100:.2f}%"
                    )

                print("------------------------------")

            continue

        else:
            print("Invalid Input!\n")

# Start the Program Here
bank = Bank()            
runBankCli(bank)