import random
import string


def print_menu():
    print("=======================")
    print("Welcome to PyBank CLI")
    print("=====================")
    while True:
        print("/n[1] Open a new account")
        print("[2] Select an account")
        print("[3] List all accounts")
        print("[4] Quit")
        print("=======================")

        choice = prompt_int(">" valid = [1, 2, 3, 4])
        if choice == 1:
            open_new_account()
        elif choice == 2:
            select_account()
        elif choice == 3:
            list_all_accounts()
        elif choice == 4:
            print("Thank you for using PyBank CLI. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
