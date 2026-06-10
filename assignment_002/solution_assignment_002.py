def ItemPrinter(lst):
    print(f"Name: {lst[0]}")
    print(f"Price: {lst[1]}")
    print(f"Quantity: {lst[2]}")
    print(f"Inventory: {lst[3]}")
    print("\n")

def ConsoleMenuSelect():
    while True:
        print("-------------------- MENU --------------------")
        print("1. Electronics\n2. Clothing\n3. Food\n4. Pets\n5. Exit")
        menu_inp = str(input("Select a category to see items: "))
        print("\n")
        
        match menu_inp:
            case "1. Electronics":
                while True:
                    print("-------------------- ITEMS --------------------")
                    print("1. Laptop\n2. Phone\n3. Nintendo Switch\n4. Back")
                    inp = str(input("Select an item to see details: "))
                    print("\n")

                    match inp:
                        case "1. Laptop":
                            item_laptop = ["DELL 4 Plus Laptop", 1550, 16, "In Stock"]
                            ItemPrinter(item_laptop)
                        case "2. Phone":
                            item_phone = ["IPhone 200", 3000, 32, "In Stock"]
                            ItemPrinter(item_phone)
                        case "3. Nintendo Switch":
                            item_switch = ["Nintendo Switch 2", 499.99, 54, "In Stock"]
                            ItemPrinter(item_switch)
                        case "4. Back":
                            break
                        case _:
                            continue
            case "2. Clothing":
                while True:
                    print("-------------------- ITEMS --------------------")
                    print("1. Shirts\n2. Pants\n3. Shoes\n4. Back")
                    inp = str(input("Select an item to see details: "))
                    print("\n")

                    match inp:
                        case "1. Shirts":
                            item_shirt = ["Basic Stussy Tee", 45, 3, "In Stock"]
                            ItemPrinter(item_shirt)
                        case "2. Pants":
                            item_pants1 = ["Women's Low Crotch Baggy Jeans in Dirty Vintage Blue", 2250, 0, "Out of Stock"]
                            ItemPrinter(item_pants1)
                            item_pants2 = ["Baggy Jeans", 1, 99, "In Stock"]
                            ItemPrinter(item_pants2)
                        case "3. Shoes":
                            item_shoes = ["Gucci Slides", 899.99, 2, "In Stock"]
                            ItemPrinter(item_shoes)
                        case "4. Back":
                            break
                        case _:
                            continue
            case "3. Food":
                while True:
                    print("-------------------- ITEMS --------------------")
                    print("1. Coffee\n2. Popcorn\n3. Candy\n4. Back")
                    inp = str(input("Select an item to see details: "))
                    print("\n")

                    match inp:
                        case "1. Coffee":
                            item_coffee = ["Instant Coffee Mix", 14, 46, "In Stock"]
                            ItemPrinter(item_coffee)
                        case "2. Popcorn":
                            item_popcorn = ["Skinny Pop", 3.64, 29, "In Stock"]
                            ItemPrinter(item_popcorn)
                        case "3. Candy":
                            item_candy = ["Trolli Gummy Worms", 7.98, 32, "In Stock"]
                            ItemPrinter(item_candy)
                        case "4. Back":
                            break
                        case _:
                            continue
            case "4. Pets":
                while True:
                    print("-------------------- ITEMS --------------------")
                    print("1. Dog\n2. Cat\n3. Fish\n4. Back")
                    inp = str(input("Select an item to see details: "))
                    print("\n")

                    match inp:
                        case "1. Dog":
                            item_dog = ["German Shepherd Mixed", 599.99, 1, "In Stock"]
                            ItemPrinter(item_dog)
                        case "2. Cat":
                            item_cat = ["American Shorthair", 249.99, 2, "In Stock"]
                            ItemPrinter(item_cat)
                        case "3. Fish":
                            item_fish = ["Fishstick", 999.99, 1, "In Stock"]
                            ItemPrinter(item_fish)
                        case "4. Back":
                            break
                        case _:
                            continue
            case "5. Exit":
                break
            case _:
                continue
                                                  
ConsoleMenuSelect()