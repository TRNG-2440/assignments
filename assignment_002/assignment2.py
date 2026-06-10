

while True:
    menu = "Menu"
    print(f"{menu:>3}")
    print("1. Electronics")
    print("2. Clothing")
    print("3. Food")
    print("4. Exit")
    category = int(input("Select a category(1-4)"))
    match category:
        case 1:
            while True:
                print("Electronics")
                print("1. Laptop")
                print("2. Phone")
                print("3. Back")
                sub_category = int(input("Select a type of electronic(1-3)"))
                match sub_category:
                    #name, price, quantity, and inventory 
                    case 1:
                        print("You selected Laptop")
                    case 2:
                        print("You selected Phone")
                    case 3:
                        print("Back to main menu")
                        break
                    case _:
                        print("Invalid input.")
                        continue
        case 2:
            while True:
                print("Clothing")
                print("1. Shirt")
                print("2. Pants")
                print("3. Back")
                sub_category = int(input("Select an item of clothing(1-3)"))
                match sub_category:
                    case 1:
                        #name, price, quantity, and inventory 
                        print("You selected Shirt")
                    case 2:
                        print("You selected Pants")
                    case 3:
                        print("Back to main menu")
                        break
                    case _:
                        print("Invalid input.")
                        continue
        case 3:
            while True:
                print("Food")
                print("1.Lasagna")
                print("2. Tacos")
                print("3. Back")
                sub_category = int(input("Select a type of Food(1-3)"))
                match sub_category:
                   case 1: 
                        print("You selected Lasagna")
                   case 2: 
                        print("You selected Tacos")
                
                   case 3: 
                        print("Back to main menu")
                        break
                   case _:
                        print("Invalid input.")
                        continue           
        case 4:
            print("Exiting program")
            break
        case _:
            print("Invalid input.")
            continue
    #continue






