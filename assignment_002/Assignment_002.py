

while(True):
    print("-----Menu-----")
    print("1.Electronics")
    print("2.Clothing")
    print("3.Food")
    print("4.Exit")
    
    choice = input("Enter your choice: ")
    
    match choice:
        case "1" | "Electronics":
            while(True):
                print("1. Laptops")
                print("2. Phones")
                print("3. Back")
                sub_choice = input("Enter your choice: ")
                if sub_choice == "1":
                    print(f"Item: Laptop | Price: $999 | Qty: 5 | Inventory: In Stock")
                elif sub_choice == "2":
                    print(f"Item: Phone | Price: $699 | Qty: 10 | Inventory: In Stock")
                elif sub_choice == "3":
                    break
                else:
                    print("Invalid choice, please try again.")
                    continue
        case "2" | "Clothing":
            while(True):
                print("1. Shirts")
                print("2. Pants")
                print("3. Back")
                sub_choice = input("Enter your choice: ")
                if sub_choice == "1":
                    print(f"Item: Shirt | Price: $25 | Qty: 20 | Inventory: In Stock")
                elif sub_choice == "2":
                    print(f"Item: Pants | Price: $40 | Qty: 15 | Inventory: In Stock")
                elif sub_choice == "3":
                    break
                else:
                    print("Invalid choice, please try again.")
                    continue
        case "3" | "Food":
            while(True):
                print("1. Ground Beef")
                print("2. Ground Turkey")
                print("3. Back")
                sub_choice = input("Enter your choice: ")
                if sub_choice == "1":
                    print(f"Item: Ground Beef | Price: $7 | Qty: 50 | Inventory: In Stock")
                elif sub_choice == "2":
                    print(f"Item: Ground Turkey | Price: $5 | Qty: 40 | Inventory: In Stock")
                elif sub_choice == "3":
                    break
                else:
                    print("Invalid choice, please try again.")
                    continue
        case "4":
            print("Exit")
            break
        case _:
            print("Invalid choice, please try again.")
            continue