"""
Console Menu Selection System

# Activity 2 — Console Menu Selection System

## Objective:

Practice nested while loops, match statements, if-else, break, continue, and formatted output using only what you have learned so far

## Instructions:

* Create a while True outer loop for the top-level category menu
* Inside the outer loop, use print() statements to display a menu with 3 categories and an option to exit the program. For example:
1. Electronics
2. Clothing
3. Food
4. Exit
* Use input() to collect the user's category selection
* Use a match statement or if-elif-else to handle the category selection:

  * A valid category selection should enter an inner while True loop for the item menu
  * 0 / exit should break out of the outer loop and end the program
  * Any invalid input should continue and reprint the category menu

Inside each inner while True loop, use print() statements to display at least 2 items for that category, plus an option to go back. For example:

1. Laptop
2. Phone
3. Back
* Use input() to collect the user's item selection
* Use a match statement or if-elif-else to handle the item selection:

  * A valid item selection should print the item's details using print() and f-strings — each item should display a name, price, quantity, and inventory hardcoded as variables or directly in the print statement
  * 0 / back should break out of the inner loop and return to the category menu
  * Any invalid input should continue and reprint the item menu

Requirements checklist:

* Outer while True loop for the category menu
* Inner while True loop for each category's item menu
* match statements or if-elif-else for handling menu selections
* break to exit or navigate back
* continue to handle invalid inputs
* At least 3 categories and 2 items per category
* Each item should display name, price, quantity, and inventory when selected
* Output should be neatly formatted using f-strings

"""
class Item:
    """
    Utility class for an item
    """
    def __init__(self, name: str, price: float, quantity: int, inventory: int):
        self.name: str = name
        self.price: float = price
        self.quantity: int = quantity
        self.inventory: int = inventory

    def get_name(self) -> str:
        """
        Get the name of this item
        :return: the name
        """
        return self.name

    def __str__(self):
        return f"{self.name}: Price: ${self.price:,.2f}, Quantity: {self.quantity}, Inventory: {self.inventory}"


BACK: str = "Back"
EXIT: str = "Exit"
MENU: dict[str, dict[str, Item]] = {
    "Ships": {
        "Yacht": Item("Yacht", 200_000.00, 1, 20),
        "Destroyer": Item("Destroyer", 10_000_000_000.00, 1, 2),
        "Tanker": Item("Tanker", 15_000_000_000.00, 1, 2)
    },
    "Animals": {
        "Cat": Item("Cat", 80, 2, 10),
        "Dog": Item("Dog", 100, 1, 8),
        "Bird": Item("Bird", 20, 4, 40),
        "Lizard": Item("Lizard", 20, 1, 3),
    },
    "Colors": {
        "Red": Item("Red", 5, 20, 100),
        "Yellow": Item("Yellow", 5, 20, 120),
        "Green": Item("Green", 5, 20, 80),
    },
    "Directions": {
        "Left": Item("Left", 2, 10, 10),
        "Right": Item("Right", 200, 1, 4),
    }
}

def main():
    """
    The main control loop
    :return:
    """
    while True:
        #outer loop
        try:
            print_list(list(MENU))
            print(EXIT)
            outer_input: str = input("Enter a category or `Exit` to exit: ")

            if outer_input == "0" or outer_input.lower() == EXIT.lower():
                break

            if (outer_input in MENU):
                while True:
                    #Inner Loop
                    try:
                        items: dict[str, Item] = MENU[outer_input]
                        names: list[str] = list(items)
                        print_list(names)
                        print(BACK)
                        inner_input: str = input("Enter an item or `Back` to go back: ")

                        if (inner_input == "0" or inner_input.lower() == BACK.lower()):
                            break

                        if inner_input in items:
                            print(items[inner_input])
                            return

                    except Exception:
                        continue
        except Exception:
            continue


def print_list(list_obj: list[str]):
    """
    Utility to print a numbered list
    :param list_obj:
    :return:
    """
    for i in range(0, len(list_obj)):
        print(list_obj[i])


if __name__ == "__main__":
    main()