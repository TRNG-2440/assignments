


def manager_menu():
    print("\n===Manager Menu===\n")
    
    print("[1] Add product")
    print("[2] Remove product")
    print("[3] Restock product")
    print("[4] List all inventory")
    print("[5] Back to main menu\n")
    
    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            add_product()
        elif choice == "2":
            remove_product()
        elif choice == "3":
            restock_product()
        elif choice == "4":
            list_inventory()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")