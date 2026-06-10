#Function calls to reprint menu for each iteration of the for loop
def MainMenu():
    print("***This is the Main Menu!***\n1. Electronics\n2. Clothing\n3. Food\n4. Toys\n5. Exit\n\n")
    pass

def Electronics():
    print("\n***Electronics***\n1. Laptop\n2. Playstation 5\n3. Iphone 64\n4. RAM\n5. Back\n\n")
    pass

def Clothing():
    print("\n***Clothing***\n1. Long Johns\n2. Horse Mask\n3. Shark Onesie\n4. Clown Shoes\n5. Back\n\n")
    pass

def Food():
    print("\n***Food***\n1. Burgers\n2. Sushi\n3. Pasta\n4. Burritos\n5. Back\n\n")
    pass

def Toys():
    print("\n***Toys***\n1. Needoh\n2. Fushigi\n3. Yo-Yo\n4. Lego Playset\n5. Back\n\n")
    pass


while True:
    MainMenu()
    user_input = input(f"What Section would you like to see?  ")

    match user_input:
        case '1':
            while True:
                Electronics()
                user_input = input(f"What Section would you like to see?  ")
                
                match user_input: #1. Laptop\n2. Playstation 5\n3. Iphone 64\n4. RAM
                    case '1':
                        print("Name: Laptop     Price: $900      \nQuantity: 10     Inventory: 200\n")
                        
                    case '2':
                        print("Name: Playstation 5     Price: $700     \nQuantity: 2       Inventory: 1\n")
                        
                    case '3':
                        print("Name: Iphone 64     Price: $800     \nQuantity: 23       Inventory: 25\n")
                        
                    case '4':
                        print("Name: RAM     Price: $46,000     \nQuantity: 0       Inventory: 0\n")
                        
                    case '5':
                        print("Back to Main\n")
                        break
                        
                    case _:
                        print("User input must be an integer, please re-try.\n\n")


        case '2':
            while True:
                Clothing() #1. Long Johns\n2. Horse Mask\n3. Shark Onesie\n4. Clown Shoes
                user_input = input(f"What Section would you like to see?  ")
                
                match user_input:
                    case '1':
                        print("Name: Long Johns     Price: $25    \nQuantity: 50     Inventory: 100\n")
                        
                    case '2':
                        print("Name: Horse Mask     Price: $20     \nQuantity: 100     Inventory: 6000\n")
                        
                    case '3':
                        print("Name: Shark Onesie     Price: $ 50    \nQuantity: 1     Inventory: 10\n")
                        
                    case '4':
                        print("Name: Clown Shoes     Price: $ 230,000    \nQuantity: 3     Inventory: 0\n")
                        
                    case '5':
                        print("\nBack to Main\n")
                        break
                    case _:
                        print("User input must be an integer, please re-try.\n\n")

        case '3':
            while True:
                Food() #1. Burgers\n2. Sushi\n3. Pasta\n4. Burritos
                user_input = input(f"What Section would you like to see?  ")
                
                match user_input:
                    case '1':
                        print("Name: Burger     Price: $20     \nQuantity: 900     Inventory: 2,000\n")
                        
                    case '2':
                        print("Name: Sushi     Price: $50     \nQuantity: 45     Inventory: 600\n")
                        
                    case '3':
                        print("Name: Pasta     Price: $15     \nQuantity: 60       Inventory: 50,000\n")
                        
                    case '4':
                        print("Name: Burritos     Price: $30     \nQuantity: 90       Inventory: 20\n")
                        
                    case '5':
                        print("Back to Main\n")
                        break
                    case _:
                        print("User input must be an integer, please re-try.\n\n")

        
        case '4':
            while True:
                Toys() #1. Needoh\n2. Fushigi\n3. Yo-Yo\n4. Lego Playset
                user_input = input(f"What Section would you like to see?  ")
                
                match user_input:
                    case '1':
                        print("Name: Needoh     Price: $20     \nQuantity: 40     Inventory: 10\n")
                        
                    case '2':
                        print("Name: Fushigi     Price: $3     \nQuantity: 900     Inventory: 46,000\n")
                        
                    case '3':
                        print("Name: Yo-Yo     Price: $50     \nQuantity: 2      Inventory: 0\n")
                        
                    case '4':
                        print("Name: Lego Playset     Price: $90     \nQuantity: 30     Inventory: 10\n")
                        
                    case '5':
                        print("Back to Main\n")
                        break
                    case _:
                        print("User input must be an integer, please re-try.\n\n")
        
        case '5':
            print("\nThank you for shopping with us!\n")
            break

        case _:
            print("User input must be an integer, please re-try.\n\n")
            