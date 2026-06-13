
from account import CheckingAccount, SavingsAccount, InvestmentAccount

class Bank:
    """" 
   - Opening a new account of any supported type
   - Looking up an account by account number
   - Listing all accounts and their current balances
   """
    
    __id = 99999
    COUNTER = 0

    def __init__(self):
        self.__account_dict = {}
    @staticmethod
    def update_id():
        Bank.__id +=1

    def open_acct(self,owner_name,bal,type): 
        Bank.COUNTER +=1
        self.update_id()
        acct_num = f"{type[:3].upper()}-{Bank.__id}"
        match type:
            case "Checking":
                self.__account_dict[acct_num] = CheckingAccount(owner_name,bal,acct_num)
            case "Savings":
                self.__account_dict[acct_num] = SavingsAccount(owner_name,bal,acct_num)
            case "Investment":
                self.__account_dict[acct_num] = InvestmentAccount(owner_name,bal,acct_num)
           
        return acct_num
    
    
    def account_lookup(self, acct_num):
        if self.COUNTER>0:
            print(acct_num)
            for k,v in self.__account_dict.items():
                print(acct_num)
                print(k)
                if k == acct_num.upper():
                    print("Account found:")
                    v.display()
                    return v
               
            print(f"{acct_num} not found in Bank") #if it's not found
            return False

        else:
            print("Bank is empty")

    def displayAll(self):
        if self.COUNTER>0:
            for v in self.__account_dict.values():
                v.display()
        else:
            print("Bank is empty")
   


