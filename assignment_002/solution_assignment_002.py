def ItemPrinter(item):
    print(f"Name: {item[0]}")
    print(f"Price: {item[1]}")
    print(f"Inventory: {item[2]}")
    print("\n")

def cartPrinter(item, q):
    print(f"Name: {item[0]}")
    print(f"Price: {item[1]}")
    print(f"Quantity: {q}")
    print("\n")

def checkBuy(item):
    i = []
    inp = input("Enter \"BUY\" to buy item. Type anything else to go back to category menu: ")
    if inp.lower() == "buy":
        inp = input("Enter amount you would like to buy: ")
        if not inp.isdigit():
            print("Invalid input. Going back to menu.")
        else:
            inp = int(inp)
            if inp <= 0 or inp > item[2]:
                print("Invalid input. Going back to menu.")
            else:
                item[2] -= inp
                i = item
                cartPrinter(item, inp)
                print(f"Successfully added {inp} item(s) to cart. Going back to menu.")
    return i


def ConsoleMenuSelect():
    elec = [["DELL 4 Plus Laptop", 1550, 20], ["IPhone 200", 3000, 32], ["Nintendo Switch 2", 499.99, 54]]
    cloth = [["Basic Stussy Tee", 45, 3], ["Baggy Jeans", 1, 99], ["Gucci Slides", 899.99, 2]]
    food = [["Instant Coffee Mix", 14, 46], ["Skinny Pop", 3.64, 29], ["Trolli Gummy Worms", 7.98, 32]]
    pets = [["German Shepherd Mixed", 599.99, 1], ["American Shorthair", 249.99, 2], ["Feeshstick", 999.99, 1]]

    while True:
        print("-------------------- MENU --------------------")
        print("1. Electronics\n2. Clothing\n3. Food\n4. Pets\n5. Exit")
        menu_inp = str(input("Select a category to see items: "))
        print("\n")
        
        match menu_inp:
            case "1" | "1. Electronics":
                while True:
                    print("-------------------- ITEMS --------------------")
                    print("1. Laptop\n2. Phone\n3. Nintendo Switch\n4. Back")
                    inp = str(input("Select an item to see details: "))
                    print("\n")

                    match inp:
                        case "1" | "1. Laptop":
                            ItemPrinter(elec[0])
                            checkBuy(elec[0])
                        case "2" | "2. Phone":
                            ItemPrinter(elec[1])
                            checkBuy(elec[1])
                        case "3" | "3. Nintendo Switch":
                            ItemPrinter(elec[2])
                            checkBuy(elec[2])
                        case "4" | "4. Back":
                            break
                        case _:
                            continue
            case "2" | "2. Clothing":
                while True:
                    print("-------------------- ITEMS --------------------")
                    print("1. Shirts\n2. Pants\n3. Shoes\n4. Back")
                    inp = str(input("Select an item to see details: "))
                    print("\n")

                    match inp:
                        case "1" | "1. Shirts":
                            ItemPrinter(cloth[0])
                            checkBuy(cloth[0])
                        case "2" | "2. Pants":
                            ItemPrinter(cloth[1])
                            checkBuy(cloth[1])
                        case "3" | "3. Shoes":
                            ItemPrinter(cloth[2])
                            checkBuy(cloth[2])
                        case "4" | "4. Back":
                            break
                        case _:
                            continue
            case "3" | "3. Food":
                while True:
                    print("-------------------- ITEMS --------------------")
                    print("1. Coffee\n2. Popcorn\n3. Candy\n4. Back")
                    inp = str(input("Select an item to see details: "))
                    print("\n")

                    match inp:
                        case "1" | "1. Coffee":
                            ItemPrinter(food[0])
                            checkBuy(food[0])
                        case "2" | "2. Popcorn":
                            ItemPrinter(food[1])
                            checkBuy(food[1])
                        case "3" | "3. Candy":
                            ItemPrinter(food[2])
                            checkBuy(food[2])
                        case "4" | "4. Back":
                            break
                        case _:
                            continue
            case "4" | "4. Pets":
                while True:
                    print("-------------------- ITEMS --------------------")
                    print("1. Dog\n2. Cat\n3. Fish\n4. Back")
                    inp = str(input("Select an item to see details: "))
                    print("\n")

                    match inp:
                        case "1" | "1. Dog":
                            ItemPrinter(pets[0])
                            checkBuy(pets[0])
                        case "2" | "2. Cat":
                            ItemPrinter(pets[1])
                            checkBuy(pets[1])
                        case "3" | "3. Fish":
                            ItemPrinter(pets[2])
                            checkBuy(pets[2])
                        case "4" | "4. Back":
                            break
                        case _:
                            continue
            case "5" | "5. Exit":
                break
            case _:
                continue
                                                  
ConsoleMenuSelect()