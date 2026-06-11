while True:
    print("\nCATEGORY MENU")
    print("1. Electronics")
    print("2. Clothing")
    print("3. Books")
    print("4. Food")
    print("5. Exit")

    category = input("Select a category (1-5): ")

    if category == "1":
        while True:
            print("\nELECTRONICS")
            print("1. Laptop")
            print("2. Phone")
            print ("3. Back")

            item = input("Select an item: ")

            if item == "1":
                print(f"\nName: Laptop")
                print(f"Price: $999.99")
                print(f"Quantity: 1")
                print(f"Inventory: 10")

            elif item == "2":
                print(f"\nName: Phone")
                print(f"Price: $599.99")
                print(f"Quantity: 1")
                print(f"Inventory: 20")

            elif item == "3":
                print(f"\nName: Ipad")
                print(f"Price: $799.99")
                print(f"Quantity: 1")
                print(f"Inventory: 15")

            elif item == "4":
                break

            else: 
                print("Invalid selection. Please try again.")
                continue

    elif category == "2":
        while True:
            print("\nCLOTHING")
            print("1.Shirt")
            print("2.Pants")
            print("3.Jeans")
            print("4. Back")

            item = input("Select an item: ")

            if item == "1":
                print(f"\nName: Shirt")
                print(f"Price: $19.99")
                print(f"Quantity: 1")
                print(f"Inventory: 50")

            elif item == "2":
                print(f"\nName: Pants")
                print(f"Price: $39.99")
                print(f"Quantity: 1")
                print(f"Inventory: 30")

            elif item == "3":
                print(f"\nName: Jeans")
                print(f"Price: $49.99")
                print(f"Quantity: 1")
                print(f"Inventory: 25")

            elif item == "4":
                break

            else:
                print("Invalid selection. Please try again.")
                continue

    elif category == "3":
        while True: 
            print("\nBOOKS")
            print("1.Novel")
            print("2. Textbook")
            print("3. Back")

            item = input("Select an item: ")

            if item == "1":
                print(f"\nName: Novel")
                print(f"Price: $14.99")
                print(f"Quantity: 1")
                print(f"Inventory: 40")

            elif item == "2":
                print(f"\nName: Textbook")
                print(f"Price: $129.99")
                print(f"Quantity: 1")
                print(f"Inventory: 15")

            elif item == "3":
                break

            else:
                print("Invalid selection. Please try again.")
                continue

    elif category == "4":
        while True: 
            print("\nFOOD")
            print("1. Paella")
            print("2. Empanada")
            print("3. Back")

            item = input("Select an item: ")

            if item == "1":
                print(f"\nName: Paella")
                print(f"Price: $19.99")
                print(f"Quantity: 1")
                print(f"Inventory: 20")

            elif item == "2":
                print(f"\nName: Empanada")
                print(f"Price: $5.99")
                print(f"Quantity: 1")
                print(f"Inventory: 30")

            elif item == "3":
                break

            else:
                print("Invalid selection. Please try again.")
                continue

    elif category == "5":
        print("Exiting...")
        break

    else:
        print("Invalid selection. Please try again.")
        continue