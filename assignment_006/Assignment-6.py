import random


class Account:
    def __init__(self, name, acnt_num, balance):
        self.name = name
        self.acnt_num = acnt_num
        self.balance = balance
        self.type = ""

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Invalid deposit amount")
        self.balance += amount
        print(f"Successfully deposited ${amount}.")

    def withdraw(self, amount):
        if amount > 0:
            self.balance -= amount
            print(f"Successfully withdrew ${amount}. Current balance: {self.balance}")
        else:
            print("Invalid amount!")

    def show_details(self):
        print(f'''
------------------------------
Account details:
------------------------------
Owner:    {self.name}
Number:   {self.acnt_num}
Balance:  ${self.balance}
------------------------------
''')
    def get_name(self):
        return self.name
    
    def get_number(self):
        return self.acnt_num
    
    def get_balance(self):
        return self.balance
        
    def get_type(self):
        return self.type
# Checking Account
class CheckingAccount(Account):
    def __init__(self, name, acnt_num, balance):
        super().__init__(name, acnt_num, balance)
        self.limit = 10000
        self.type = "checking"

    def withdraw(self, amount):
        if amount > self.limit or amount <= 0:
            raise ValueError("Invalid withdrawal amount.")
        self.balance -= amount
        print(f"Successfully withdrew ${amount}. Your balance is ${self.balance}.")

    def show_details(self):
        print(f'''
------------------------------
Account details:
------------------------------
Owner    :{self.name}
Number   :{self.acnt_num}
Balance  :${self.balance}
Type     :Checking
Limit    :{self.limit}
------------------------------
''')

# Savings Account
class SavingsAccount(Account):
    def __init__(self, name, acnt_num, balance):
        super().__init__(name, acnt_num, balance)
        self.wthdrwl_cnt_lmt = 3
        self.wthdrwl_cnt = 0
        self.type = "savings"
        self.intrst_rt = 2.5

    def apply_interest(self):
        self.balance *= (1 + self.intrst_rt * 0.01)
        print(f"Applied interest of {self.intrst_rt}%")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Invalid withdrawal amount.")

        if self.wthdrwl_cnt > self.wthdrwl_cnt_lmt:
            raise ValueError(f"Unable to perform action: You've reached your limit of {self.wthdrwl_cnt_lmt} this month!")

        self.balance -= amount
        self.wthdrwl_cnt += 1
        print(f"Successfuly withdrew ${amount}.  You have withdrawn {self.wthdrwl_cnt} times this month out of {self.wthdrwl_cnt_lmt} New balance: {self.balance}.")

    def reset_limit(self):
        self.wthdrwl_cnt = 0
        print("Reset withdrawl limit")

    def show_details(self):
        print(f'''
------------------------------
Account details:
------------------------------
Owner      :{self.name}
Number     :{self.acnt_num}
Balance    :${self.balance}
Type       :Savings
Withdrawals:{self.wthdrwl_cnt}/{self.wthdrwl_cnt_lmt} used this month
Interest   :{self.intrst_rt}% monthly
------------------------------
''')

# Investment Account
class InvestmentAccount(Account):
    def __init__(self, name, acnt_num, balance):
        super().__init__(name, acnt_num, balance)
        self.min_bal = 10000
        self.rtrn_rate = 2.5
        self.type = "investment"

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Invalid withdrawal amount.")

        if self.balance-amount < self.min_bal:
            raise ValueError(f"Cannot do this action, as it would put you below your minimum balance of ${self.min_bal}")
        
        self.balance -= amount
    
        print(f"Successfully withdrew ${amount}.  Your balance is now ${self.balance}, your minimum is ${self.min_bal}.")

    def apply_return(self):
        self.balance = self.balance * (1 + self.rtrn_rate * 0.01)
        print(f"Successfully applied return rate of {self.rtrn_rate}%, balance is now ${self.balance}.")

    def show_details(self):
        print(f'''
------------------------------
Account details:
------------------------------
Owner       :{self.name}
Number      :{self.acnt_num}
Balance     :${self.balance}
Type        :Investment
Min. Balance:${self.min_bal}
Return Rate :{self.rtrn_rate}% monthly
------------------------------
''')


class Bank:
    def __init__(self):
        self.accounts = {}

    def open_account(self, account_obj):
        self.accounts[account_obj.acnt_num] = account_obj

    # Accessing acounts
    def get_account(self, number):
        return self.accounts.get(number)
        
    def get_details(self, number):
        return self.accounts[number].show_details
    
    def list_accounts(self):
        print("\n--- All Bank Accounts ---")
        for num, acc in self.accounts.items():
            print(f"Account: {num} | Owner: {acc.name} | Balance: ${acc.balance}")

def main():
    bank = Bank()

    print('''
==============================
   Welcome to PyBank CLI
==============================
''')
    while True:
        main_sel = input('''
[1] Open a new account
[2] Select an account
[3] List all accounts
[4] Quit
          ''')
        
        match main_sel:
            # Opening an account
            case "1":
                print("Account Type")
                type = input('''
[1] Checking
[2] Savings
[3] Investment
                             ''')
                match type:
                    case "1":
                        name = input("Owner name: ")
                        bal = float(input("Opening Balance: "))
                        num = "CHE-00" + str(random.randint(0, 999))
                        bank.open_account(CheckingAccount(name, num,bal))
                    case "2":
                        name = input("Owner name: ")
                        bal = float(input("Opening Balance: "))
                        num = "SAV-00" + str(random.randint(0, 999))
                        bank.open_account(SavingsAccount(name, num,bal))

                    case "3":
                        name = input("Owner name: ")
                        bal = float(input("Opening Balance: "))
                        num = "INV-00" + str(random.randint(0, 999))
                        bank.open_account(InvestmentAccount(name, num,bal))
            # Selecting an account
            case "2":
                select = input("Input your account number!")
                sel_acnt = bank.get_account(select)
                if not sel_acnt:
                    print("Account not found")
                    continue
                else:
                    print(f"Account Selected: {sel_acnt.get_name()} ({sel_acnt.get_number()})")
                while True:

                    print('''
[1] Show Details
[2] Deposit
[3] Withdraw''')

                    if sel_acnt.type == "savings":
                        print("[4] Apply Interest")
                    elif sel_acnt.type == "investment":
                        print("[4] Apply Return")
                    
                    print("[0]: Back to main menu")

                    action = input(">")

                    match action:
                        case "1":
                            sel_acnt.show_details()
                        case "2":
                            deposit = input("Input your deposit amount: ")
                            try:
                                deposit = float((deposit)) 
                                sel_acnt.deposit(deposit)
                            except ValueError as e:
                                print(f"Deposit failed: {e}")
                        case "3":
                            withdraw = input("Input your withdrawal amount: ")
                            try:
                                withdraw = float((withdraw))
                                sel_acnt.withdraw(withdraw)
                            except ValueError as e:
                                print(f"Withdrawal failed: {e}")
                        case "4":
                            if sel_acnt.type == "savings":
                                sel_acnt.apply_interest()
                            elif sel_acnt.type == "investment":
                                sel_acnt.apply_return()
                        case "0":
                            break

            # If user selects "list accounts"
            case "3":
                bank.list_accounts()
            # What if the user selects exit?
            case "4":
                break

    
main()
