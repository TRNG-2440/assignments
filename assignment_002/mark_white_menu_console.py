# Mark White
# 06/09/2026
# Console Menu Selection System

# This program implements a console-based menu selection system for a store. 
# it allows users to select from different categories (Electronics, Clothing, Food) 
# then choose specific items within those categories and view details (Name, Price, Quantity, Inventory).



while True:
    print("""
        MENU:
        1. Electronics
        2. Clothing
        3. Food
        4. Exit
          """)
    
    category = input("Please select a category (1-4): ")
    
    if not category.isdigit():
        print("Invalid selection.")
        continue
    
    category = int(category)
    
    match category:
        case 1:
            while True:
                print("""
                  Electronics:
                  1. Phone
                  2. Laptop
                  3. Back to Main Menu
                  """)
                option = input("Please select an option (1-3): ")
                match option:
                    case "1":
                        name = "Phone"
                        price = 699.99
                        quantity = 1
                        inventory = 50
                        
                        print(f"""
                            Selected Item: {name}
                            Price: ${price}
                            Quantity: {quantity}
                            Inventory: {inventory}
                            """)
                    case "2":
                        name = "Laptop"
                        price = 999.99
                        quantity = 1
                        inventory = 30
                        
                        print(f"""
                            Selected Item: {name}
                            Price: ${price:.2f}
                            Quantity: {quantity}
                            Inventory: {inventory}
                            """)
                        
                    case "3":
                        break

                    case _:
                        print("Invalid selection. Please try again.")
        case 2:
            while True:
                print("""
                  Clothing:
                  1. Shirt
                  2. Pants
                  3. Back to Main Menu
                  """)
                option = input("Please select an option (1-3): ")
                match option:
                    case "1":
                        name = "Shirt"
                        price = 29.99
                        quantity = 1
                        inventory = 100
                    
                        print(f"""
                            Selected Item: {name}
                            Price: ${price:.2f}
                            Quantity: {quantity}
                            Inventory: {inventory}
                            """)
                    case "2":
                        name = "Pants"
                        price = 49.99
                        quantity = 1
                        inventory = 80
                    
                        print(f"""
                            Selected Item: {name}
                            Price: ${price:.2f}
                            Quantity: {quantity}
                            Inventory: {inventory}
                            """)
                    case "3":
                        break

                    case _:
                        print("Invalid selection. Please try again.")
        case 3:
            while True:
                print("""
            
                    Food:
                    1. Milk
                    2. Bread 
                    3. Back to Main Menu
                    """)

                option = input("Please select an option (1-3): ") 

                match option:
                    case "1":  
                        name = "Milk"
                        price = 2.99
                        quantity = 1
                        inventory = 200
                    
                        print(f"""
                            Selected Item: {name}
                            Price: ${price:.2f}
                            Quantity: {quantity}
                            Inventory: {inventory}
                            """)
                    case "2":
                        name = "Bread"
                        price = 1.99
                        quantity = 1
                        inventory = 150
                    
                        print(f"""
                            Selected Item: {name}
                            Price: ${price:.2f}
                            Quantity: {quantity}
                            Inventory: {inventory}
                            """)
                    case "3":
                        break

                    case _:
                        print("Invalid selection. Please try again.")
        case 4:
            print("Exiting the program. Goodbye!")
            break
        case _:
            print("Invalid selection. Please try again.")

