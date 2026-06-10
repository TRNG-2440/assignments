category = {
    1: "1. Laptop\n2. Phone\n3. Back",
    2: "1. T-shirt\n2. Pants\n3. Back",
    3: "1. Pizza\n2. Burger\n3. Back"
}

# I could have used a two dimensional Numpy array here but I did not want to import Numpy
# The Ideal data structure would be a 2 dimensional Numpy array but this is a bit easier to visualize
items = {
    "11": "Name: Laptop\nPrice: $2,000\nQuantity: 400 units\nInventory: The best",
    "12": "Name: Phone\nPrice: $1,000\nQuantity: 5,000 units\nInventory: Good",
    "21": "Name: T-shirt\nPrice: $60\nQuantity: 15,000 units\nInventory: The best",
    "22": "Name: Pants\nPrice: $450\nQuantity: 225 units\nInventory: Not good",
    "31": "Name: Pizza\nPrice: $20\nQuantity: 125 units\nInventory: Good",
    "32": "Name: Burger\n Price: $15\nQuantity: 200 units\nInventory: Good"
}

def get_selection(num_selections: int) -> int:
    """
    Collects and validates users's Selection.
    Requires the number of selections passed as an int paramater
    """
    while True:
        try:
            selection = int(input())        
            if selection > num_selections or selection < 1:
                raise Exception("Invalid input detected")
        except Exception as ex:
            print("\nThat is not a valid input. Please try again\n")
        return selection

if __name__ == "__main__":
    while True:
        print("Please select a catagory\n1. Electronics\n2. Clothing\n3. Food \n4. Exit")
        category_selection = get_selection(4)
        if category_selection == 4:
            print("Okay bye.")
            break
        while True:
            print("\nPlease select an item")
            print (category[category_selection])
            item_selection = get_selection(3)
            if item_selection == 3:
                break
            print(items[f"{category_selection}{item_selection}"])
    