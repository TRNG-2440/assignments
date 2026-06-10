categoryMenu = True

while categoryMenu:
    print("Select an option:")
    print("1. Electronics")
    print("2. Clothing")
    print("3. Food")
    print("4. Exit")
    choice = input("Enter your choice: ")

    if choice == "1" or choice == "Electronics":
        print("You selected Electronics.")

        ElectronicsMenu = True

        while ElectronicsMenu:

            print("Electronics Menu:")
            print("1. Laptop")
            print("2. Phone")
            print("3. Back ")
            electronics_choice = input("Enter your choice: ")

            if electronics_choice == "1" or electronics_choice == "Laptop":
                name = "Laptop"
                price = 999.99
                quantity = 1
                inventory = 12
                print(f"\nItem: {name}")
                print(f"Price: ${price}")
                print(f"Quantity: {quantity}")
                print(f"Inventory: {inventory}")

            elif electronics_choice == "2" or electronics_choice == "Phone":
                name = "Phone"
                price = 599.99
                quantity = 1
                inventory = 25
                print(f"\nItem: {name}")
                print(f"Price: ${price}")
                print(f"Quantity: {quantity}")
                print(f"Inventory: {inventory}")

            elif electronics_choice == "3" or electronics_choice == "Back":
                print("Returning to main menu.")
                ElectronicsMenu = False

            else:
                print("Invalid choice. Please try again.")
                continue


    elif choice == "2" or choice == "Clothing":
        print("You selected Clothing.")

        ClothingMenu = True

        while ClothingMenu:

            print("Clothing Menu:")
            print("1. Shirt")
            print("2. Pants")
            print("3. Back ")
            clothing_choice = input("Enter your choice: ")

            if clothing_choice == "1" or clothing_choice == "Shirt":
                name = "Shirt"
                price = 29.99
                quantity = 1
                inventory = 50
                print(f"\nItem: {name}")
                print(f"Price: ${price}")
                print(f"Quantity: {quantity}")
                print(f"Inventory: {inventory}")

            elif clothing_choice == "2" or clothing_choice == "Pants":
                name = "Pants"
                price = 49.99
                quantity = 1
                inventory = 30
                print(f"\nItem: {name}")
                print(f"Price: ${price}")
                print(f"Quantity: {quantity}")
                print(f"Inventory: {inventory}")

            elif clothing_choice == "3" or clothing_choice == "Back":
                print("Returning to main menu.")
                ClothingMenu = False

            else:
                print("Invalid choice. Please try again.")
                continue

    elif choice == "3" or choice == "Food":
        print("You selected Food.")

        FoodMenu = True

        while FoodMenu:

            print("Food Menu:")
            print("1. Apple")
            print("2. Bread")
            print("3. Back ")
            food_choice = input("Enter your choice: ")

            if food_choice == "1" or food_choice == "Apple":
                name = "Apple"
                price = 0.99
                quantity = 1
                inventory = 100
                print(f"\nItem: {name}")
                print(f"Price: ${price}")
                print(f"Quantity: {quantity}")
                print(f"Inventory: {inventory}")

            elif food_choice == "2" or food_choice == "Bread":
                name = "Bread"
                price = 2.99
                quantity = 1
                inventory = 40
                print(f"\nItem: {name}")
                print(f"Price: ${price}")
                print(f"Quantity: {quantity}")
                print(f"Inventory: {inventory}")

            elif food_choice == "3" or food_choice == "Back":
                print("Returning to main menu.")
                FoodMenu = False

            else:
                print("Invalid choice. Please try again.")
                continue

    elif choice == "4" or choice == "Exit":
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Please try again.")
        continue
