# item information variables
name = ""
price = ""
quantity = ""
inventory = ""

while True: # top level category menu
    print ("1. Fantasy")
    print ("2. Sci-Fi")
    print ("3. Mystery")
    print ("4. Exit\n")

    choice = input("Pick a category: ")

    match choice:
        case "1" | "Fantasy":
            while True: # Fantasy Menu
                print ("1. The Fellowship of The Ring")
                print ("2. The Way of Kings")
                print ("3. Back\n")
                choice = input("Pick an item: ")

                match choice: 
                    case "1" | "The Fellowship of the Ring":
                        name = "The Fellowship of the Ring"
                        price = "$19.99"
                        quantity = "3"
                        inventory = "50"
                    
                    case "2" | "The Way of Kings":
                        name = "The Way of Kings"
                        price = "$24.99"
                        quantity = "5"
                        inventory = "30"

                    case "3" | "Back":
                        break

                    case _:
                        continue

                # print item information
                print(f"Name: {name}\nPrice: {price}\nQuantity: {quantity}\nInventory: {inventory}\n")

        case "2" | "Sci-Fi":
            while True: # Sci-Fi Menu
                print ("1. Ender's Game")
                print ("2. The Hitchiker's Guide to the Galaxy")
                print ("3. Back \n")
                choice = input("Pick an item: ")

                match choice: 
                    case "1" | "Ender's Game":
                        name = "Ender's Game"
                        price = "$21.99"
                        quantity = "4"
                        inventory = "39"
                    
                    case "2" | "The Hitchiker's Guide to the Galaxy":
                        name = "The Hitchiker's Guide to the Galaxy"
                        price = "$28.99"
                        quantity = "2"
                        inventory = "68"

                    case "3" | "Back":
                        break

                    case _:
                        continue
                
                # print item information
                print(f"Name: {name}\nPrice: {price}\nQuantity: {quantity}\nInventory: {inventory}\n")

        case "3" | "Mystery":
            while True: # Mystery Menu
                print ("1. The Girl With the Dragon Tattoo")
                print ("2. Where the Crawdads Sing")
                print ("3. Back\n")
                choice = input("Pick an item: ")

                match choice: 
                    case "1" | "The Girl With the Dragon Tattoo":
                        name = "The Girl With the Dragon Tattoo"
                        price = "$28.99"
                        quantity = "1"
                        inventory = "33"
                    
                    case "2" | "Where the Crawdads Sing":
                        name = "Where the Crawdads Sing"
                        price = "$15.99"
                        quantity = "7"
                        inventory = "48"

                    case "3" | "Back":
                        break

                    case _:
                        continue

                # print item information
                print(f"Name: {name}\nPrice: {price}\nQuantity: {quantity}\nInventory: {inventory}\n") 

        case "4" | "Exit":
            break
        
        case _:
            continue
