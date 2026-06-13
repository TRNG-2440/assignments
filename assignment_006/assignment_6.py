from bank import Bank
#1
# from account import CheckingAccount, SavingsAccount, InvestmentAccount

def main():
   
    bank = Bank()
    while True: 

    
        print("Welcome to the Bank! Please select an option:")
        print("___________________________________________")
        print("[1] Open a new account")
        print("[2] Select an account")
        print("[3] List all accounts")
        print("[4] Quit")

        choice = input("Enter your selection (1-4): ")

        match choice:
            case "1":
                type = select_type()
                if type:
                    create_account(type, bank)
                else:
                    continue
               
            case "2":
                if bank.COUNTER < 1:
                    print("No accounts in bank! Please open an account first.")
                    continue
                else:
                    acct_num = input("Enter the account number to select: ")
                    account = bank.account_lookup(acct_num)
                    account_menu(account, bank)
                   
            case "3":
                bank.displayAll()
            case "4":
                print("Thank you for banking with us! Goodbye!")
                break
            case _:
                print("Invalid selection. Please enter a number between 1 and 4.")
                continue


def select_type():
    """Select the type of account to open"""
    
    print("Type of Account:")
    print("1. Checking Account")
    print("2. Savings Account")
    print("3. Investment Account")
    print()

    type = input("Please select a type of account to open(1-3): ")
    match type:
        case "1": 
            return "Checking"
        case "2":
            return "Savings"
        case "3":
            return "Investment"
        case _: 
            print("Invalid Account Type Selection")
            return False
    
    
def create_account(type, bank):

    """Open a  new account helper method that handles user input and exceptions for opening a new account"""
    try:
        owner_name = input("Enter the account owner's name: ")
        input_bal = int(input("Enter the opening balance: "))
        acct_num  = bank.open_acct(owner_name, input_bal, type)
        print()
        print(f"{type} account opened for {owner_name}.")
        print(f"Account #: {acct_num}  |  Balance: ${input_bal:.2f}")
        print("___________________________________________")
    except ValueError:
        print("Invalid input! Please enter a numeric value for the opening balance.")

def account_menu(account, bank):
    if account:
        while True:
            print()
            print("Account Menu:")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Apply Monthly Interest")
            print("4. View Details")
            print("5. Back to Main Menu")

            acct_choice = input("Enter your selection (1-5): ")
            match acct_choice:
                case "1":
                    try:
                        amnt = float(input("Enter the amount to deposit: "))
                        account.deposit(amnt)
                    except ValueError:
                        print("Invalid input! Please enter a numeric value for the deposit amount.")
                case "2":
                    try:
                        amnt = float(input("Enter the amount to withdraw: "))
                        account.withdraw(amnt)
                    except ValueError as e:
                        print(f"Error: {e}")
                case "3":
                    if account.TYPE == "Savings":
                        account.apply_interest()
                    else:
                        print("Account not eligible for monthly interest")
                    
                case "4":
                    account.display()
                    
                case _:
                    print("Invalid selection. Please enter a number between 1 and 4.")
                    
    else:
        return


if __name__ == "__main__":
    main()
