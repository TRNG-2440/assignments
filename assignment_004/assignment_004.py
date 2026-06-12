# Assignment 4
from collections import Counter

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

def add_to_dict(sentence: str) -> int:
    """
    Adds words to dictionary and returns the word count.
    """
    word_list = sentence.split()
    for word in word_list:
        if word in word_frequency:
            word_frequency[word] += 1
        else:
            word_frequency[word] = 1
    return len(word_list)

def show_word_count() -> int:
    """
    prints the words stored in the dictionary
    """
    print("-" * 40)
    if not word_frequency:
        print("You have not analyzed anything yet.")
        print("-" * 40)
        return 0
    for word in word_frequency:
        print(f"  {word:<13}: {word_frequency[word]}")
    print("-" * 40)
    return len(word_frequency)

def print_most_frequent() -> None:
    """
    Prints the most frequent words
    """
    if not word_frequency:
        print("You have not analyzed anything yet.")
        print("-" * 40)
        return
    print(f'Most frequent word: "{Counter(word_frequency).most_common(1)[0][0]}" ({Counter(word_frequency).most_common(1)[0][1]}) times')

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
        match selected_option:
            case 1:
                word_count = add_to_dict(input("Enter sentence to analyze: "))
                print(f"✔ Processed {word_count}\n")
                print("═" * 40)
            case 2:
                print(f"  You have {show_word_count()} unique words\n")
                print("=" * 40)
            case 3:
                print_most_frequent()
                print("=" * 40)
            case 4:
                word_frequency.clear()
            case 5:
                print("Goodbye")
                break