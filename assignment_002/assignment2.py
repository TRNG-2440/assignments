categories = {
    1: {
        "name": "Electronics",
        "items": {
            1: {"name": "Laptop", "price": 699, "quantity": 23, "inventory": 100},
            2: {"name": "Phone", "price": 449, "quantity": 43, "inventory": 230},
        },
    },
    2: {
        "name": "Clothing",
        "items": {
            1: {"name": "Pants", "price": 40, "quantity": 45, "inventory": 324},
            2: {"name": "Dress", "price": 64, "quantity": 37, "inventory": 478},
            3: {"name": "Shirt", "price": 36, "quantity": 82, "inventory": 862},
        },
    },
    3: {
        "name": "Food",
        "items": {
            1: {"name": "Burger", "price": 15, "quantity": 63, "inventory": 392},
            2: {"name": "Fries", "price": 7, "quantity": 43, "inventory": 375},
            3: {"name": "Sandwich", "price": 12, "quantity": 54, "inventory": 673},
        },
    },
}


def printMenu(data, is_category=True):
    """
    Display a formatted menu with options from the provided data dictionary.

    Args:
        data (dict): Dictionary containing menu items with 'name' keys
        is_category (bool): If True, shows 'Exit' option; if False, shows 'Back' option. Defaults to True.

    Returns:
        None
    """
    print()
    for key, value in data.items():
        print(f"{key}. {value['name']}")
    print(f"{len(data) + 1}. {'Exit' if is_category else 'Back'}")
    print()


if __name__ == "__main__":
    while True:
        # Print categories + exit option
        printMenu(categories)
        selected_category = int(input("Enter chosen category number:"))
        # Handle category selection using match statement
        match selected_category:
            case value if value in range(1, len(categories) + 1):  # Valid category
                selected_items = categories[value]["items"]
                while True:
                    # Display items for the selected category
                    printMenu(selected_items, is_category=False)
                    selected_item = int(input("Enter chosen item number:"))
                    if selected_item in range(1, len(selected_items) + 1):
                        # Display selected item's details
                        item = selected_items[selected_item]
                        print(
                            f"Name:{item['name']}\nPrice:{item['price']}\nQuantity:{item['quantity']}\nInventory:{item['inventory']}"
                        )
                    elif selected_item != len(selected_items) + 1:  # Invalid choice
                        print("Invalid option! Try again..")
                    else:  # Back option selected - return to category menu
                        break
            case value if (
                value == len(categories) + 1
            ):  # Exit option selected - end program
                break
            case _:  # Invalid choice
                print("Invalid option! Try again..")
