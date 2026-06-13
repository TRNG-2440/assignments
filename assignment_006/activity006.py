from enum import Enum

MENU_WIDTH = 29

class NoAccountFoundError(Exception):
    """raised when no account found"""
    def __init__(self, acc=0, message="no account found"):
        super().__init__(f"{message} -- account entered: {acc}")

class InvalidAccountError(Exception):
    """raised when account# is negative"""
    def __init__(self, acc=0, message="negative numbers aren't allowed"):
        super().__init__(f"{message} -- account entered: {acc}")

class InsufficientFundsError(Exception):
    def __init__(self, funds=0, message="Not enough funds remaining"):
        super().__init__(f"{message} funds entered: {funds}")

class MonthlyWithdrawLimitError(Exception):
    def __init__(self, message="Monthly withdraw limit reached"):
        super().__init__(f"{message}")

class AccountType(Enum):
    SAVINGS = "savings"
    CHECKING = "checking"
    INVESTMENT = "investing"

class Account:
    def __init__(self, name:str, acc_no:int, balance=0):
        self.owner_name = name
        self.account_number = acc_no
        self.balance = balance

    def __str__(self):
        return f"{self.name: 15<}{self.account_number: >15}"
    
    def deposit(self):
        bal = valid_balance()
        self.balance += bal
        print(f"Deposited: ${float(bal):,.2f}\nNew Balance: ${float(self.balance):,.2f}")

    def withdraw(self):
        bal = valid_balance()
        if bal < self.balance:
            self.balance -= bal
        else:
            raise InsufficientFundsError(bal)
        print(f"withdrew: {bal}\nnew balance: {self.balance}")

    def details(self):
        bal = f"${float(self.balance):,.2f}"
        return f"Name: {self.owner_name: >19}\nAccount#: {self.account_number: >15}\nBalance: {bal: >16}\n"

class CheckingAccount(Account):
    def __init__(self, name:str, acct_no:int, bal:int=0, od_lim:int=500):
        super().__init__(name, acct_no, bal)
        self.account_type = AccountType.CHECKING
        self.overdraft_lim = od_lim
    
    def details(self):
        sup = super().details()
        a_t = f"type: {self.account_type.value: >19}"
        od_lim = f"${float(self.overdraft_lim):,.2f}"
        return f"{sup}{a_t}\nOverdraft limit: {od_lim: >8}\n"

    def withdraw(self):
        bal = valid_balance()
        if bal < self.balance + self.overdraft_lim:
            self.balance -= bal
        else:
            raise InsufficientFundsError(bal)
        print(f"withdrew: {bal}\nnew balance: {self.balance}")

    def apply_interest(self):
        print("cannot apply interest to a checking account")

    
class SavingsAccount(Account):
    def __init__(self, name, acct_no, bal=0, rate:float=0.0, max_wd=0):
        super().__init__(name, acct_no, bal)

        self.account_type = AccountType.SAVINGS
        self.interest_rate = rate
        self.monthly_withdraw_limit = max_wd
        self.current_monthly_withdraw = 0
    
    def details(self):
        sup = super().details()
        a_t = f"type: {self.account_type.value: >19}\n"
        month_take = f"{self.current_monthly_withdraw}/{self.monthly_withdraw_limit}"
        r = f"%{(self.interest_rate * 100.0):.1f}"
        return f"{sup}{a_t}Withdrawals: {month_take: >12}\nInterest rate: {r: >10}\n"

    def withdraw(self):
        bal = valid_balance()
        if self.current_monthly_withdraw >= self.monthly_withdraw_limit:
            raise MonthlyWithdrawLimitError
        if bal < self.balance:
            self.balance -= bal
            self.current_monthly_withdraw += 1
        else:
            raise InsufficientFundsError
        print(f"withdrew: {bal}\nnew balance: {self.balance}")

    def apply_interest(self):
        month_rate = self.interest_rate / 12
        interest = (self.balance * month_rate)
        old = f"${float(self.balance):,.2f}"
        self.balance += interest

        print(f"old balance: {old}\nnew balance: ${float(self.balance):,.2f}\naccrued interest: ${float(interest):,.2f}" )

class InvestmentAccount(Account):
    def __init__(self, name, acct_no, bal=0, min_bal=0, var_growth=0.015):
        super().__init__(name, acct_no, bal)

        self.account_type = AccountType.INVESTMENT
        self.minimum_balance = min_bal
        self.variable_growth_rate = var_growth

    def details(self):
        sup = super().details()
        a_t = f"type: {self.account_type.value: >19}\n"
        m_b = f"${float(self.minimum_balance):,.2f}"
        rate = f"%{(self.variable_growth_rate * 100.0):.1f}"
        return f"{sup}{a_t}Minimum Balance: {m_b: >8}\nInterest Rate: {rate: >11}\n"

    def withdraw(self):
        bal = valid_balance()

        if bal < self.balance - self.minimum_balance:
            self.balance -= bal
        else:
            raise InsufficientFundsError(bal)
        print(f"withdrew: {bal}\nnew balance: {self.balance}")

    def apply_interest(self):
        month_rate = self.variable_growth_rate / 12
        interest = (self.balance * month_rate)
        old = f"${float(self.balance):,.2f}"
        self.balance += interest

        print(f"old balance: {old}\nnew balance: ${float(self.balance):,.2f}\ngrowth: ${float(interest):,.2f}" )
 


class Bank:
    __total_accounts = 0
    __invest_min = 1000
    __default_rate = 0.015
    __monthly_take_lim = 3


    def __init__(self):
        self._accounts = {}
        self.main_options = ["Open a new account", 
                             "Select an account", 
                             "List all accounts"]
        self.type_options = ["Checking", 
                                "Savings", 
                                "Investment"]
        self.account_options = ["Deposit",
                                "Withdraw",
                                "Apply Monthly Interest",
                                "View Details"]
        
    def generate_acc_no(self, bs=2, br=1):
        # build account number from base, branch, user
        # change to allow more users/branches
        base = bs * (10**5)
        branch = br * (10**3)
        user = Bank.__total_accounts
        Bank.__total_accounts += 1

        return base + branch + user

    def open_new_acct(self, acc_type):
        name = input("account holder: ")
        bal = valid_balance()
        
        match acc_type:
            case AccountType.CHECKING:
                acc = self.generate_acc_no()
                self._accounts[acc] = CheckingAccount(name, acc, bal)
            case AccountType.SAVINGS:
                acc = self.generate_acc_no()
                self._accounts[acc] = SavingsAccount(name, 
                                                     acc, 
                                                     bal, 
                                                     Bank.__default_rate, 
                                                     Bank.__monthly_take_lim)
            case AccountType.INVESTMENT:
                acc = self.generate_acc_no()
                while bal < Bank.__invest_min:
                    try:
                        print(f"the minimum investment balance is {Bank.__invest_min}")
                        bal = int(input("initial deposit: "))
                    except ValueError:
                        print("bad input, must be a numeric value")
                self._accounts[acc] = InvestmentAccount(name, acc, bal, Bank.__invest_min)

    def acct_lookup(self) -> int:
        try:
            acc = int(input("enter account#: "))
        except ValueError:
            print("bad input")
            return None
        except Exception as e: 
            raise e

        if acc < 0:
            raise InvalidAccountError(acc)
        
        if acc in self._accounts:
            
            return acc
        else:
            raise NoAccountFoundError(acc)
        
    
    def display_all(self):
        if not len(self._accounts):
            raise NoAccountFoundError
        
        for acc in self._accounts:
            print(self._accounts[acc].details())

    def main_menu(self):
        w = MENU_WIDTH
        border = "=" * w + "\n"
        title = "Welcome to A Bank"
        banner = f"{border}{title: ^{w}}\n{border}"
        print(banner)
        while True:
            print_menu(*self.main_options)
            user_selection = get_selection(len(self.main_options))
            match user_selection:
                case 1: # open account
                    self.type_menu()
                case 2: # select account
                    try:
                        self.account_menu()
                    except Exception as e:
                        print(f"unhandled error {e}")

                case 3: # list all
                    try:
                        self.display_all()
                    except NoAccountFoundError:
                        print("there are no accounts to display")
                    # except Exception as e:
                    #     print(f"unexpected exception {e}")
                    #     print("exiting")
                    #     return None
                case 0: # exit
                    print("exiting...\nGoodbye")
                    return user_selection
    
    def type_menu(self):
        print("Account Type")
        print_menu(*self.type_options)
        user_selection = get_selection(len(self.type_options))
        match user_selection:
            case 1: # checking
                self.open_new_acct(AccountType.CHECKING)
            case 2: # savings
                self.open_new_acct(AccountType.SAVINGS)
            case 3: # investment
                self.open_new_acct(AccountType.INVESTMENT)
            case 0:
                print("canceling account creation")
                return None
            
    def account_menu(self):
        try:
            acc = self.acct_lookup()
        except InvalidAccountError as e:
            print(e)
            return None
        except NoAccountFoundError as e:
            print(e)
            return None
        except Exception as e:
            raise e

        while True:
            print("Account Options")
            print_menu(*self.account_options)
            user_selection = get_selection(len(self.account_options))
            match user_selection:
                case 1: # deposit
                    self._accounts[acc].deposit()
                case 2: # Withdraw
                    try:
                        self._accounts[acc].withdraw()
                    except MonthlyWithdrawLimitError as e:
                        print(e)
                    except InsufficientFundsError as e:
                        print(e) 
                case 3: # Apply Monthly Interest
                    self._accounts[acc].apply_interest()
                case 4: # View Details
                    print(self._accounts[acc].details())
                case 0:
                    print("returning to main menu")
                    return None
def valid_balance():
    bal = 0

    while bal <= 0:
        try:
            bal = int(input("amount: "))
        except ValueError:
            print("enter a dollar amount")
            continue
        if bal <= 0:
            print("amount must be greater than 0")
    return bal

def print_menu(*args:str) -> None:
    w = MENU_WIDTH
    """
    print main menu from list
    """
    print()
    for idx, item in enumerate(args, 1):
        print(f"[{idx}] {item:.>{w}}")
    print("[0]" + "." * (w-4) + " exit")

def get_selection(lim:int = 0) -> int:
    """
    get selection from user, return int within limit
    - repeat on ValueError
    """
    valid = False
    while not valid:
        try:
            sel = int(input(f"> "))
        except ValueError:
            print("bad value")
            continue
        except Exception as e:
            raise e
        print()
        match sel:
            case sel if sel < 0 :
                print("value too low")
                valid = False
            case sel if sel > lim:
                print("value too high")
                valid = False
            case _:
                valid = True
    return sel



if __name__ == "__main__":
    b = Bank()

    b.main_menu()