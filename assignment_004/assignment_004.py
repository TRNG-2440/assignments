# Assignment 4
word_frequency = {}

def get_selection(num_selections: int) -> int:
    """
    Collects and validates users's Selection.
    Requires the number of selections passed as an int paramater
    """
    while True:
        try:
            selection = int(input("Select an option: "))        
            if selection > num_selections or selection < 1:
                raise Exception("Invalid input detected")
        except Exception as ex:
            print("\nThat is not a valid input. Please try again\n")
        return selection

if __name__ == "__main__":
    print("═" * 40)
    print(" " * 7 + "WORD FREQUENCY COUNTER" + " " * 7)
    print("═" * 40)
    while True:
        print("1. Analyse a sentence")
        print("2. View word counts")
        print("3. View most frequent word")
        print("4. Clear results")
        print("5. Exit")
        print("═" * 40)
        selected_option = get_selection(5)
        if selected_option == 5:
            break
        break