import random

class InventoryItem():
    def __init__(self, name, price, qty, inv):
        self.name = name
        self.price = price
        self.qty = qty
        self.inv = inv

    def __str__(self):
        return self.name
    
    def prettyStr(self):
        return f"\n{self.name: <15} ${self.price: >7.2f} {self.qty: >5} {self.inv: >5}"

def print_menu(items):
    print()
    for num, item in enumerate(items, start=1):
        print(f"{num}. {item}")
    
    print("0. exit")

def fill_rand(lst, names):
    for item in names:
        p = random.randint(25, 50)
        q = random.randint(0, 5)
        i = random.randint(10, 100)
        lst.append(InventoryItem(item, float(p + 0.99), q, i))

categories = ["electronics", "motors", "batteries", "propellors"]
electronics = ["speed controller", "receiver"]
motors = ["brushless 2208", "9g servo"]
batteries = ["4S 4000mah", "3S 2200mah"]
propellors = ["6in two blade", "5in three blade"]

# probably a much better way to do this
inventory = {key : list() for key in categories}

# fill values with random numbers
fill_rand(inventory["electronics"], electronics)
fill_rand(inventory["motors"], motors)
fill_rand(inventory["batteries"], batteries)
fill_rand(inventory["propellors"], propellors)

if __name__ == "__main__":
    while True:
        print_menu(categories)
        # look for bad input values
        try:
            sel = int(input("enter: "))
        except ValueError:
            print("\nselect an item from the list")
            continue
        
        # break if falsy
        if not sel:
            break
        
        # check input range
        if not (0 < sel <= len(categories) ):
            print("\nselection out of range, try again")
            continue
        
        while True:
            print_menu(inventory[categories[sel-1]])
            # look for bad input
            try:
                sel2 = int(input("enter: "))
            except ValueError:
                print("\nselect an item from the list")
                continue

            # check falsy
            if not sel2:
                break

            # check in range
            if not (0 < sel2 <= len(inventory[categories[sel-1]])):
                print("\nselection out of range, try again\n")
                continue
            else:
                inv_itm = inventory[categories[sel-1]][sel2-1]
            
            # print the item stuff
            print(inv_itm.prettyStr())


#     Create a while True outer loop for the top-level category menu
#     Inside the outer loop, use print() statements to display a menu with 3 categories and an option to exit the program. For example:

#     Electronics
#     Clothing
#     Food
#     Exit

#     Use input() to collect the user's category selection

#     Use a match statement or if-elif-else to handle the category selection:
#         A valid category selection should enter an inner while True loop for the item menu
#         0 / exit should break out of the outer loop and end the program
#         Any invalid input should continue and reprint the category menu

# Inside each inner while True loop, use print() statements to display at least 2 items for that category, plus an option to go back. For example:

#     Laptop
#     Phone
#     Back

#     Use input() to collect the user's item selection

#     Use a match statement or if-elif-else to handle the item selection:
#         A valid item selection should print the item's details using print() and f-strings — each item should display a name, price, quantity, and inventory hardcoded as variables or directly in the print statement
#         0 / back should break out of the inner loop and return to the category menu
#         Any invalid input should continue and reprint the item menu

# Requirements checklist:

#     Outer while True loop for the category menu
#     Inner while True loop for each category's item menu
#     match statements or if-elif-else for handling menu selections
#     break to exit or navigate back
#     continue to handle invalid inputs
#     At least 3 categories and 2 items per category
#     Each item should display name, price, quantity, and inventory when selected
#     Output should be neatly formatted using f-strings