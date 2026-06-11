# Console Menu Selection System

def print_inventory(name, price, quantity, inventory):
    print(f"{'Name':<12}{'Price':<12}{'Quantity':<12}{'Inventory':<12}")
    print("-" * 45)
    print(f"{name:<12}${price:<12.2f}{quantity:<12}{inventory:<12}")
    print("\n")


def electronics_inventory():
    # need to show at least 2 items 
    # if the selection is valid, then print the name, price, quantioty, and inventory
    # 0 --> back to the category menu
    # invalid --> continue to reprint

    while True:
        print("\nHere are our current electronic menu: ") 
        print("1. Laptop \n2. Phone \n3. Back")
        elec_option = input("Please choose an option: ")
        print("\n")

        if elec_option == "1":
            name = "Laptop"
            price = 899.99
            quantity = 1
            inventory = 20
            print_inventory(name, price, quantity, inventory)

        elif elec_option == "2":
            name = "Phone"
            price = 999.99
            quantity = 1
            inventory = 53
            print_inventory(name, price, quantity, inventory)

        elif elec_option == "3" or elec_option == "0":
            break
        else:
            print("\nPlease select a valid option")




def clothing_inventory():
    while True:
        print("\nHere are our current clothing menu: ") 
        print("1. Shirts \n2. Pants \n3. Back")
        clothing_option = input("Please choose an option: ")
        print("\n")

        if clothing_option == "1":
            name = "Shirts"
            price = 12.99
            quantity = 4
            inventory = 127
            print_inventory(name, price, quantity, inventory)

        elif clothing_option == "2":
            name = "Pants"
            price = 54.99
            quantity = 3
            inventory = 200
            print_inventory(name, price, quantity, inventory)

        elif clothing_option == "3" or clothing_option == "0":
            break
        else:
            print("\nPlease select a valid option")


def food_inventory():
    while True:
        print("\nHere are our current electronic menu: ") 
        print("1. Noodles \n2. Chips \n3. Back")
        food_option = input("Please choose an option: ")
        print("\n")

        if food_option == "1":
            name = "Noodles"
            price = 5.99
            quantity = 1
            inventory = 370
            print_inventory(name, price, quantity, inventory)

        elif food_option == "2":
            name = "Chips"
            price = 4.99
            quantity = 1
            inventory = 500
            print_inventory(name, price, quantity, inventory)

        elif food_option == "3" or food_option == "0":
            break
        else:
            print("\nPlease select a valid option")





def main():

    # while true outer loop
    while True:
        # continue to reprint until choice is valid

        print("Hi! Welcome to the menu. Here are our departments...")
        print("1. Electronics \n2. Clothing \n3. Food \n4. Exit")

        user_input = input("Please select a department: ")
                # enter item option
        if user_input == "1":
            electronics_inventory()
        elif user_input == "2":
            clothing_inventory()
        elif user_input == "3":
            food_inventory()
        elif user_input == "0" or user_input == "4":
            break
        else:
            print("\nnPlease select a valid option")

        
        



if __name__ == "__main__":
    main()