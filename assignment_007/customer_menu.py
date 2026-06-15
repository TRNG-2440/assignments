



def customer_menu():
    print("\n===Customer Menu===\n")
    print("[1] Browse all products")
    print("[2] Search by name")
    print("[3] Place an order")
    print("[4] Back to main menu\n")


    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            browse_products()
        elif choice == "2":
            search_by_name()
        elif choice == "3":
            place_order()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
