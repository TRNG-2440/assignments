def consoleMenu():
    while True:
        categoryChoice = int(input("Choose your category: 0. Exit 1. Electronics 2. Clothing 3. Food: "))
        match categoryChoice:
            case 0:
                break
    
            case 1:
                while True:
                    itemChoice = int(input("Choose your item: 1. Laptop 2. Phone 0. Back: "))
                    if itemChoice == 1:
                        print(f"Name = Lenovo, Price = 799.99, Quantity = 5, Inventory = In stock")
                    elif itemChoice == 2:
                        print(f"Name = iPhone 16e, Price = 399.99, Quantity = 10, Inventory = In stock")
                    elif itemChoice == 0:
                        break
                    else:
                        print(f"Choose a valid number (0-2)")
                        continue

            case 2:
                while True:
                    itemChoice = int(input("Choose your item: 1. Shirt 2. Shoes 0. Back: "))
                    if itemChoice == 1:
                        print(f"Name = Red Polo, Price = 19.99, Quantity = 20, Inventory = In stock")
                    elif itemChoice == 2:
                        print(f"Name = AF1, Price = 59.99, Quantity = 8, Inventory = In stock")
                    elif itemChoice == 0:
                        break
                    else:
                        print(f"Choose a valid number (0-2)")
                        continue
                
            case 3:
                while True:
                    itemChoice = int(input("Choose your item: 1. Pizza 2. Burger 0. Back: "))
                    if itemChoice == 1:
                        print(f"Name = Pepperoni, Price = 12.99, Quantity = 15, Inventory = In stock")
                    elif itemChoice == 2:
                        print(f"Name = Bacon Burger, Price = 8.99, Quantity = 25, Inventory = In stock")
                    elif itemChoice == 0:
                        break
                    else:
                        print(f"Choose a valid number (0-2)")
                        continue

            case _:
                print(f"Choose a valid input! (0-3)")
                continue

consoleMenu()