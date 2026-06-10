

while True:
    print("1. Electronics")
    print("2. Clothing")
    print("3. Food")
    print("4. Exit")

    choice = int(input("Enter the number for your choice: "))
    match choice:
        case 1:
            while True:
                print("1. Laptop")
                print("2. Phone")
                print("3. Back")
                sub_choice = int(input("Enter the number for your choice: "))
                match sub_choice:
                    case 1:
                        laptop_name = "Laptop"
                        laptop_price = 950.99
                        laptop_quantity = 12
                        laptop_inventory = 123456
                        print(f"Name: {laptop_name}, Price: ${laptop_price}, Quantity: {laptop_quantity}, Inventory: {laptop_inventory}")
                    case 2:
                        phone_name = "Phone"
                        phone_price = 500.00
                        phone_quantity = 15
                        phone_inventory = 234567
                        print(f"Name: {phone_name}, Price: ${phone_price}, Quantity: {phone_quantity}, Inventory: {phone_inventory}")
                    case 3:
                        break
                    case _:
                        continue
        case 2:
            while True:
                print("1. Shirt")
                print("2. Pants")
                print("3. Back")
                sub_choice = int(input("Enter the number for your choice: "))
                match sub_choice:
                    case 1:
                        shirt_name = "Shirt"
                        shirt_price = 22.85
                        shirt_quantity = 21
                        shirt_inventory = 345678
                        print(f"Name: {shirt_name}, Price: ${shirt_price}, Quantity: {shirt_quantity}, Inventory: {shirt_inventory}")
                    case 2:
                        pants_name = "Pants"
                        pants_price = 27.50
                        pants_quantity = 19
                        pants_inventory = 456789
                        print(f"Name: {pants_name}, Price: ${pants_price}, Quantity: {pants_quantity}, Inventory: {pants_inventory}")
                    case 3:
                        break
                    case _:
                        continue

        case 3:
            while True:
                print("1. Sandwich")
                print("2. Soup")
                print("3. Back")
                sub_choice = int(input("Enter the number for your choice: "))
                match sub_choice:
                    case 1:
                        sandwich_name = "Sandwich"
                        sandwich_price = 8.69
                        sandwich_quantity = 15
                        sandwich_inventory = 567891
                        print(f"Name: {sandwich_name}, Price: ${sandwich_price}, Quantity: {sandwich_quantity}, Inventory: {sandwich_inventory}")
                    case 2:
                        soup_name = "Soup"
                        soup_price = 5.00
                        soup_quantity = 13
                        soup_inventory = 678912
                        print(f"Name: {soup_name}, Price: ${soup_price}, Quantity: {soup_quantity}, Inventory: {soup_inventory}")
                    case 3:
                        break
                    case _:
                        continue
        case 4:
            break
        case _:
            continue