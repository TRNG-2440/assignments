# Defining some functions ahead of time to reduce repeated code for formatted data
# Should also help improve readability
def printOptions(options):
    output = "   Pick an Option! Type the number you want:\n"
    current_option = 1
    for option in options:
        output += f"{str(current_option)}. {option}\n"
        current_option+= 1
    print(output)

def printDetails(details):
    print(
        f"Name: {details[0]}\n"
        f"Price: {details[1]}\n"
        f"Quantity: {details[2]}\n"
        f"Inventory: {details[3]}"
    )

# Block with various hardcoded details
main_menu = ["Electronics", "Clothing", "Food", "Exit"]
electronics_menu = ["Laptop", "Desktop", "Phone", "Exit"]
clothing_menu = ["Shirt", "Pants", "Shoes", "Exit"]
food_menu = ["Burger", "Hotdog", "Taco", "Exit"]
#details = ["name", "price", "quantity", "inventory"]
laptop_details = ["Laptop", "$500.00", "1", "15"]
desktop_details = ["Desktop", "$1750.00", "1", "20"]
phone_details = ["IPhone", "$1000.00", "1", "1000"]
shirt_details = ["Supreme", "$2500.00", "3", "15"]
pants_details = ["Levi's", "$50.00", "2", "151"]
shoes_details = ["Nike", "$120.00", "2", "60"]
burger_details = ["In-n-out", "$15.00", "4", "1100"]
hotdog_details = ["Costco Hot Dog", "$1.50", "2", "150000"]
taco_details = ["Taco Bell", "$5.00", "4", "1500"]

# Start the program, specifically the outer loop
while True:
    # Print out the options from main menu, and take user input
    printOptions(main_menu)
    user_in= input()
    # Compare the user input with the possible cases
    match user_in:
        # Within each case, there resides another while loop,
        # It does the same as the outer, but with if elif else statements
        case "1": # Electronics
            while True:
                printOptions(electronics_menu)
                user_in2 = input()
                if user_in2 == "1": #Laptop
                    printDetails(laptop_details)
                elif user_in2 == "2": #Desktop
                    printDetails(desktop_details)
                elif user_in2 == "3": #Phone
                    printDetails(phone_details)
                elif user_in2 == "4": #exit
                    break
                else:
                    print("Invalid input, please try again!")
                    continue
        case "2": #Clothing
            while True:
                printOptions(clothing_menu)
                user_in2 = input()
                if user_in2 == "1": #Shirt
                    printDetails(shirt_details)
                elif user_in2 == "2": #Pants
                    printDetails(pants_details)
                elif user_in2 == "3": #Shoes
                    printDetails(shoes_details)
                elif user_in2 == "4": #exit
                    break
                else:
                    print("Invalid input, please try again!")
                    continue
        case "3": #Food
            while True:
                printOptions(food_menu)
                user_in2 = input()
                if user_in2 == "1": #Burger
                    printDetails(burger_details)
                elif user_in2 == "2": #Hotdog
                    printDetails(hotdog_details)
                elif user_in2 == "3": #Tacos
                    printDetails(taco_details)
                elif user_in2 == "4": #exit
                    break
                else:
                    print("Invalid input, please try again!")
                    continue
        case "4": #Exit
            break
        case _:
            print("Invalid input, please try again!")
            continue

