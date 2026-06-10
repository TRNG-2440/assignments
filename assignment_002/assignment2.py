
from unittest import case


def main():
    """Simple menu with item categories and subcategories. All items listed by name, price, quantity, and inventory."""
    while True:
        menu = "Menu"
        print(f"{menu:>3}")
        print("1. Electronics")
        print("2. Clothing")
        print("3. Food")
        print("4. Exit")
        category = int(input("Select a category(1-4):"))
        print()
        match category:
            case 1:
                case1()
                
            case 2:
                case2()
              
            case 3:
                case3()   
                      
            case 4:
                print("Exiting program")
                break
            case _:
                print("Invalid input.")
                continue


def case1():
    """Electronics category"""
    while True:
        print("Electronics Menu")
        print("1. Laptop")
        print("2. Phone")
        print("3. Back")
        sub_category = int(input("Please select a type of electronic(1-3): "))
        print() 
        match sub_category:
            #name, price, quantity, and inventory 
            case 1:
                name = "Dell inspiron 14"
                price = 700.00
                qty = 10
                inventory = "In Stock"
                print("You selected Laptop.")
                print(f"item name: {name:<3}, price: {price:<3.2f}, quantity: {qty:<3}, inventory: {inventory:<3}\n")
            case 2:
                name = "iphone 16 Pro Max"
                price = 1200.00
                qty = 5
                inventory = "In Stock"
                print("You selected Phone")
                print(f"item name: {name:<3}, price: {price:<3.2f}, quantity: {qty:<3}, inventory: {inventory:<3}\n")

            case 3:
                print(f"Back to main menu\n")
                return
            case _:
                print(f"Invalid input.\n")
                continue
def case2():
    """Clothing category"""
    while True:
        print("Clothing Menu")
        print("1. Shirt")
        print("2. Pants")
        print("3. Back")
        sub_category = int(input("Select an item of clothing(1-3): "))
        print()
        match sub_category:
            case 1:
                #name, price, quantity, and inventory 
                name = "Pink Shirt"
                price = 25.00
                qty = 2
                inventory = "Low Stock"
                print("You selected Shirt")
                print(f"item name: {name:<3}, price: {price:<3.2f}, quantity: {qty:<3}, inventory: {inventory:<3}\n")
            case 2:                
                name = "Blue Jeans"
                price = 40.00
                qty = 10
                inventory = "In Stock"
                print("You selected Pants")
                print(f"item name: {name:<3}, price: {price:<3.2f}, quantity: {qty:<3}, inventory: {inventory:<3}\n")
            case 3:
                print(f"Back to main menu\n")
                return
            case _:
                print(f"Invalid input.\n")
                continue
def case3():
    """Food category"""
    while True:
        print("Food Menu")
        print("1. Lasagna")
        print("2. Tacos")
        print("3. Back")
        sub_category = int(input("Select a type of Food(1-3): "))
        print()
        match sub_category:
            case 1: 
                    name = "Lasagna"
                    price = 12.99
                    qty = 0
                    inventory = "Out of Stock"
                    print("You selected Lasagna")
                    print(f"item name: {name:<3}, price: {price:<3.2f}, quantity: {qty:<3}, inventory: {inventory:<3}\n")
            case 2: 
                    name = "Tacos"
                    price = 9.99
                    qty = 20
                    inventory = "In Stock"
                    print("You selected Tacos")
                    print(f"item name: {name:<3}, price: {price:<3.2f}, quantity: {qty:<3}, inventory: {inventory:<3}\n")
            case 3: 
                    print(f"Back to main menu\n")
                    return
            case _:
                    print(f"Invalid input.\n")
                    continue 
                         


#run the program
if __name__ == "__main__":  
    main()


