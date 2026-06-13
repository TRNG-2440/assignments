# Assignment 7 by Ariyan Shaikh

class Product:
    def __init__(self):
        pass

def get_selection(num_selections: int) -> int:
    """
    Collects and validates users's Selection.
    Requires the number of selections passed as an int paramater
    """
    print()
    while True:
        try:
            selection = int(input("Select an option: "))        
            if selection > num_selections or selection < 1:
                raise Exception("Invalid input detected")
        except Exception as ex:
            print("\nThat is not a valid input. Please try again\n")
            return get_selection(num_selections)
        return selection


if __name__ == "__main__":
    print("=" * 40)
    print(f'{"PyStore Inventory System":^40}')
    print("=" * 40)

    print()
    print("[1] Manager Menu")
    print("[2] Customer Menu")
    print("[3] Quit")

    while True:
        menu_option = get_selection(3)
        match menu_option:
            case 1:
                pass
            case 2:
                pass
            case 3:
                print("Goodbye")
                break
