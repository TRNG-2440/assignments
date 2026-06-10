#Solution for Assignment 2
#Alex Tran


while True:
    print("\n=== MENU ===")
    print("1. Electronics")
    print("2. Clothing")
    print("3. Food")
    print("4. Exit")

    #prompt the user to choose the category
    option = input("Please choose a category: ")
    
    match option:
        #Electronics Menu
        case "1":
            while True:
                print("\n---Electronics---")
                print("1. Laptop")
                print("2. Phone")
                print("3. Back")

                #prompt user input for choosing an item

                item = input("Choose an item: ")

                #case handling for item

                match item:
                    case "1":
                        name = "Macbook Air"
                        price = 1199.99
                        quantity = 4
                        inventory = "In Stock"

                        #Display item, price, quantity and inventory for the selected item
                        print(f"\nName: {name}")
                        print(f"Price: ${price:.2f}")
                        print(f"Quantity: {quantity}")
                        print(f"Inventory: {inventory}")
                    
                    case "2":
                        name = "iPhone 17"
                        price = 999.99
                        quantity = 2
                        inventory = "Low Stock"

                        #Display item, price, quantity and inventory for the selected item
                        print(f"\nName: {name}")
                        print(f"Price: ${price:.2f}")
                        print(f"Quantity: {quantity}")
                        print(f"Inventory: {inventory}")

                    case "3":
                        break

                    case _:
                        print("Invalid item selection. Please choose an item from the menu.")
                        continue
        #CLothing Menu
        case "2":
            while True:
                print("\n---Clothing---")
                print("1. Shirt")
                print("2. Shoes")
                print("3. Back")

                #prompt user input for choosing an item

                item = input("Choose an item: ")

                #case handling for item

                match item:
                    case "1":
                        name = "T-Shirt"
                        price = 19.99
                        quantity = 20
                        inventory = "In Stock"

                        #Display item, price, quantity and inventory for the selected item
                        print(f"\nName: {name}")
                        print(f"Price: ${price:.2f}")
                        print(f"Quantity: {quantity}")
                        print(f"Inventory: {inventory}")
                    
                    case "2":
                        name = "Running Shoes"
                        price = 79.99
                        quantity = 0
                        inventory = "Out of Stock"

                        #Display item, price, quantity and inventory for the selected item
                        print(f"\nName: {name}")
                        print(f"Price: ${price:.2f}")
                        print(f"Quantity: {quantity}")
                        print(f"Inventory: {inventory}")

                    case "3":
                        break

                    case _:
                        print("Invalid item selection. Please choose an item from the menu.")
                        continue
        #Food Menu
        case "3":
            while True:
                print("\n---Food---")
                print("1. Pizza")
                print("2. Burger")
                print("3. Back")

                #prompt user input for choosing an item

                item = input("Choose an item: ")

                #case handling for item

                match item:
                    case "1":
                        name = "Pizza"
                        price = 2.99
                        quantity = 4
                        inventory = "In Stock"

                        #Display item, price, quantity and inventory for the selected item
                        print(f"\nName: {name}")
                        print(f"Price: ${price:.2f}")
                        print(f"Quantity: {quantity}")
                        print(f"Inventory: {inventory}")
                    
                    case "2":
                        name = "Burger"
                        price = 8.99
                        quantity = 8
                        inventory = "In Stock"

                        #Display item, price, quantity and inventory for the selected item
                        print(f"\nName: {name}")
                        print(f"Price: ${price:.2f}")
                        print(f"Quantity: {quantity}")
                        print(f"Inventory: {inventory}")

                    case "3":
                        break

                    case _:
                        print("Invalid item selection. Please choose an item from the menu.")
                        continue
        case "4":
            print("Exiting Menu...")
            break
        
        #Invalid Selection
        case _:
            print("Invalid Category Selection.")
            continue
