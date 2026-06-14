


def main_menu():

    while True:

        print("==============================")
        print("PyStore Inventory System")    
        print("==============================")
        print("[1] Manager Menu")
        print("[2] Customer Menu")
        print("[3] Quit")
        print()
        role = input("Select option(1-3): ")

        if role == 1:
            manager_menu()
        elif role == 2:
            customer_menu()
        elif role == 3:
            break
        else:
            print("Invalid option")
            print()
            continue

def manager_menu()
        

        print() 
        print("-----Manager Menu-------")
        print()
        print("[1] Add product")
        print("[2] Remove product")
        print("[3] Restock product")
        print("[4] List all inventory")
        print("[5] Back")

        option  = input("Please select option(1-5)")

        match option:
            case 1: 
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                return
             

def customer_menu():
     



           














if __name__ == "__main__":
    main_menu()



