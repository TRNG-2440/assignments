
def console_menu():

    # harcoded values for the products 
    l_name = "Acer"
    l_price = 800
    l_quanity = 35
    l_inventory = 100

    p_name = "IPhone"
    p_price = 900
    p_quantity = 40
    p_inventory = 80

    s_name = "Shirt"
    s_price = 15
    s_quantity = 80
    s_inventory = 100

    pants_name = "Pants"
    pants_price = 30
    pants_quantity = 40
    pants_inventory = 80

    fruit_name = "Apple"
    fruit_price = 2
    fruit_quantity = 50
    fruit_inventory = 60

    rice_name = "Rice"
    rice_price = 40
    rice_quantity = 70
    rice_inventory = 100

    flag = True
    while flag:
        print("1. Electronics")
        print("2. Clothing")
        print("3. Food")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("1. Laptop")
            print("2. Phone")
            print("3. Back")

            sub_choice = input("Enter your choice: ")

            if sub_choice == '1':
                print(f"The product is {l_name}")
                print(f"The price is ${l_price}")
                print(f"Quantity available: {l_quanity}")
                print(f"Inventory: {l_inventory}")
                break

            elif sub_choice == '2':
                 print(f"The product is {p_name}")
                 print(f"The price is ${p_price}")
                 print(f"Quantity available: {p_quantity}")
                 print(f"Inventory: {p_inventory}")
                 break
            
            elif sub_choice == '3':
                continue
  

        elif choice == '2':
            print("1. Shirt")
            print("2. Pants")
            print("3. Back")

            sub_choice = input("Enter your choice: ")

            if sub_choice == '1':
                print(f"The product is {s_name}")
                print(f"The price is ${s_price}")
                print(f"Quantity available: {s_quantity}")
                print(f"Inventory: {s_inventory}")
                break
            elif sub_choice == '2':
                print(f"The product is {pants_name}")
                print(f"The price is ${pants_price}")
                print(f"Quantity available: {pants_quantity}")
                print(f"Inventory: {pants_inventory}")
                break
            elif sub_choice == '3':
                continue

        elif choice == '3':
            print("1. Apple")
            print("2. Rice")
            print("3. Back")

            sub_choice = input("Enter your choice: ")
            if sub_choice == '1':
                print(f"The product is {fruit_name}")
                print(f"The price is ${fruit_price}")
                print(f"Quantity available: {fruit_quantity}")
                print(f"Inventory: {fruit_inventory}")
                break
            elif sub_choice == '2':
                print(f"The product is {rice_name}")
                print(f"The price is ${rice_price}")
                print(f"Quantity available: {rice_quantity}")
                print(f"Inventory: {rice_inventory}")
                break
            elif sub_choice == '3':
                continue

        elif choice == '4' or '0':
            flag = False






console_menu()