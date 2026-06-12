
class Account:
    """1. Create a base `Account` class that holds common attributes 
    such as owner name, account number, and balance. It should support depositing
    funds and displaying account details."""
    def __init__(self,owner_name,acct_num,bal):
        self.__owner_name = owner_name
        self.__acct_num = acct_num
        self.__bal = bal
    
    #takes any int
    def deposit(self,val):
        #only supports depositing
        deposit = abs(val)
        self.__bal += deposit
        print(f"Deposit amount: {deposit}")
    

    def display(self):
        print("______________________________")
        print(f" {'Owner Name':<18} {':'} {self.__owner_name:<20}")
        print(f" {'Account Number':<18} {':'} {self.__acct_num:<20}")
        print(f" {'Balance':<18} {':'} ${self.__bal:<20,.2f}")
        print("______________________________")


def main():
    #for testing
    this_acct = Account("me",000000,30.00)
    this_acct.deposit(30.00)
    this_acct.display()


if __name__ == "__main__":
    main()




