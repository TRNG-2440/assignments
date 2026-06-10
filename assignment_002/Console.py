while True:
    print("\n===Store Menu===")
    print("1. Electronics")
    print("2. Clothing")
    print("3. Food")
    print("4. Exit")

    category = input("\n Category: ")

    match category:
        case "1":
            while True:
                print("\n---Electronics---")
                print("1. Laptop")
                print("2. Phone")
                print("3. Back")

                item = input("\n Item: ")

                match item:
                    case "1":
                        name = "Laptop"
                        price = 999.99
                        quantity = 10
                        inventory = "In Stock"
                        print(f"Name: {name}\nPrice: ${price}\nQuantity: {quantity}\nInventory Status: {inventory}")
                    case "2":
                        name = "Phone"
                        price = 498.99
                        quantity = 20
                        inventory = "In Stock"
                        print(f"Name: {name}\nPrice: ${price}\nQuantity: {quantity}\nInventory Status: {inventory}")
                    case "3":
                        break
                    case _:
                        continue
        case "2":
            while True:
                print("\n---Clothing---")
                print("1. T-Shirt")
                print("2. Jeans")
                print("3. Back")

                item = input("\n Item: ")

                match item:
                    case "1":
                        name = "T-Shirt"
                        price = 19.99
                        quantity = 50
                        inventory = "In Stock"
                        print(f"Name: {name}\nPrice: ${price}\nQuantity: {quantity}\nInventory Status: {inventory}")
                    case "2":
                        name = "Khakis"
                        price = 29.99
                        quantity = 30
                        inventory = "In Stock"
                        print(f"Name: {name}\nPrice: ${price}\nQuantity: {quantity}\nInventory Status: {inventory}")
                    case "3":
                        break
                    case _:
                        continue
        case "3":
            while True:
                print("\n---Food---")
                print("1. Rice")
                print("2. Chicken")
                print("3. Back")

                item = input("\n Item: ")

                match item:
                    case "1":
                        name = "Rice"
                        price = 3.99
                        quantity = 40
                        inventory = "In Stock"
                        print(f"Name: {name}\nPrice: ${price}\nQuantity: {quantity}\nInventory Status: {inventory}")
                    case "2":
                        name = "Chicken"
                        price = 5.99
                        quantity = 50
                        inventory = "In Stock"
                        print(f"Name: {name}\nPrice: ${price}\nQuantity: {quantity}\nInventory Status: {inventory}")
                    case "3":
                        break
                    case _:
                        continue
        case "4":
            print("\nEnd")
            break
        case _:
            print("Invalid category. Please try again.")
            continue