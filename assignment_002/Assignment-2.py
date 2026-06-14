

total_price = 0

options = {"1": [9.78, 0, 12, "Grand Burger"], "2": [6.50, 0, 10, "Bacon Cheeseburger"], "3": [7.00, 0, 8, "Green Chile Cheeseburger"],
            "4": [3.50, 0, 20, "French Fries"], "5":[4, 0, 12, "Onion Rings"], "6": [3.25, 0, 7, "Salad"],
            "7": [3.75, 0, 13, "Milkshake"], "8":[2.25, 0, 31, "Fountain Drink"], "9":[2.75, 0, 15, "Lemonade"]}


def item_details(choice):

    options[choice][1] += 1
    options[choice][2] -= 1

    print(f'''You ordered a {options[choice][3]}! You currently have a quantity of {options[choice][1]} of them now
          for {options[choice][0]} each, and we now have {options[choice][2]} in our inventory''')

while True:
    selection = input('''
Welcome to McRonalds!  What would you like?
1. Burgers
2. Sides
3. Drinks
4. Exit\n''')
        
    
    match selection:
        case "1":
            while True:
                burg_sel = input('''
Which burger would you like?
1. Grand Burger
2. Bacon Cheeseburger
3. Green Chile Cheeseburger
4. Go back\n''')
                match burg_sel:
                    case "1": 
                        total_price += options["1"][0]
                        item_details("1")
                    case "2": 
                        total_price += options["2"][0]
                        item_details("2")
                    case "3": 
                        total_price += options["3"][0]
                        item_details("3")
                    case "4": 
                        print("Hope you enjoyed your time here! Bye!")
                        break
                    case _: print("Sorry, we don't have that here!")

                
        case "2":
            while True:
                side_sel = input('''
Which side do you want?
1. Fries
2. Onion Rings
3. Salad
4. Back\n''')
                match side_sel:
                    case "1": 
                        total_price += options["4"][0]
                        item_details("4")
                    case "2": 
                        total_price += options["5"][0]
                        item_details("5")
                    case "3": 
                        total_price += options["6"][0]
                        item_details("6")
                    case "4": 
                        break
                    case _: print("Sorry, we don't have that here!")

        case "3":
            while True:
                drink_sel = input('''
What would you like to drink?
1. A milkshake
2. Fountain Drink
3. Housemade Lemonade
4. Back\n''')
                match drink_sel:
                    case "1": 
                        total_price += options["7"][0]
                        item_details("7")
                    case "2": 
                        total_price += options["7"][0]
                        item_details("7")
                    case "3": 
                        total_price += options["8"][0]
                        item_details("8")
                    case "4": 
                        break
                    case _: print("Sorry, we don't have that here!")
                
        case "4": 
            break
        case _: print("Please select a valid input")

