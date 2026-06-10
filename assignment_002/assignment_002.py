# outer loop for category menu
while True:
    print("1. Electronics")
    print("2. Clothing")
    print("3. Food")
    print("4. Exit")

    cat = int(input("Select a category (by number): "))

    match cat:
        case 1: 
            # inner loop for electronics menu
            while True:
                print("1. Laptop")
                print("2. Phone")
                print("3. Watch")
                print("4. Back")
                item = int(input("Select an item (by number): "))

                match item:
                    case 1:
                        print("Laptop: Macbook Pro, $1000, 1, In stock")
                    case 2:
                        print("Phone: iPhone 15, $500, 1, In stock")
                    case 3:
                        print("Watch: Apple Watch Series 8, $200, 1, In stock")
                    case 4:
                        break
                    case _:
                        print("Invalid item. Please try again.")
                        continue
        case 2:
            # inner loop for clothing menu
            while True:
                print("1. Shirt")
                print("2. Pants")
                print("3. Jacket")
                print("4. Back")
                item = int(input("Select an item (by number): "))

                match item:
                    case 1:
                        print("Shirt: Nike, $20, 1, In stock")
                    case 2:
                        print("Pants: Levi's, $30, 1, In stock")
                    case 3:
                        print("Jacket: North Face, $100, 1, In stock")
                    case 4:
                        break
                    case _:
                        print("Invalid item. Please try again.")
                        continue
        case 3:
            # inner loop for food menu
            while True:
                print("1. Pizza")
                print("2. Burger")
                print("3. Hot Dog")
                print("4. Back")
                item = int(input("Select an item (by number): "))

                match item:
                    case 1:
                        print("Pizza: Pepperoni, $10, 1, In stock")
                    case 2:
                        print("Burger: McDonald's, $5, 1, In stock")
                    case 3:
                        print("Hot Dog: Hot Dog, $3, 1, In stock")
                    case 4:
                        break
                    case _:
                        print("Invalid item. Please try again.")
                        continue
        case 4:
            break
        case _:
            print("Invalid category. Please try again.")
            continue
