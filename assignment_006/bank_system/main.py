# Mark White
# 06/12/2026
# Assignment 6
# Banking System

# This program simulates a banking system. 
# the program allows the user to open an account, select an account, list all accounts, and quit.
# you can deposit, withdraw, and apply interest to your account. 
# there are limits to withdrawals, overdrafts, and minimum balances according to accounts type.


from bank import Bank
from checking_account import CheckingAccount
from savings_account import SavingsAccount
from investment_account import InvestmentAccount
from exceptions import *


def main():

    bank = Bank()

    while True:

        print("\n==== Welcome to the Bank ====\n")
        print("1. Open Account")
        print("2. Select Account")
        print("3. List Accounts")
        print("4. Quit")

        choice = input("\nChoice: \n")

        if choice == "1":

            print("\n1. Checking")
            print("2. Savings")
            print("3. Investment")

            account_type = input("Type: ")
            owner = input("Owner: ")

            try:
                balance = float(input("Opening Balance: "))
            except ValueError:
                print("Invalid balance.")
                continue

            if account_type == "1":
                account = CheckingAccount(owner, balance)

            elif account_type == "2":
                account = SavingsAccount(owner, balance)

            elif account_type == "3":
                account = InvestmentAccount(owner, balance)

            else:
                print("Invalid account type.")
                continue

            bank.open_account(account)

            print(
                f"Created account {account.account_number}"
            )

        elif choice == "2":

            account_number = input(
                "Account Number: "
            )

            account = bank.find_account(
                account_number
            )

            if not account:
                print("Account not found.")
                continue

            while True:

                print("\n1. Deposit")
                print("2. Withdraw")
                print("3. Details")
                print("4. Apply Interest")
                print("5. Back to Menu")

                option = input("Choice: ")
                print("")

                try:

                    if option == "1":
                        amount = float(
                            input("Amount: ")
                        )
                        account.deposit(amount)

                    elif option == "2":
                        amount = float(
                            input("Amount: ")
                        )
                        account.withdraw(amount)

                    elif option == "3":
                        print(account.get_details())

                    elif option == "4":

                        if isinstance(
                            account,
                            SavingsAccount
                        ):
                            account.apply_interest()

                        elif isinstance(
                            account,
                            InvestmentAccount
                        ):
                            rate = float(
                                input(
                                    "Return Rate (0.05 = 5%): "
                                )
                            )
                            account.apply_return(rate)

                        else:
                            print(
                                "No interest to apply."
                            )

                    elif option == "5":
                        break

                except Exception as e:
                    print("Error:", e)

        elif choice == "3":
            bank.list_accounts()

        elif choice == "4":
            print("Leaving Bank System, Goodbye!")
            break

        else:
            print("Invalid choice.")



if __name__ == "__main__":
    main()