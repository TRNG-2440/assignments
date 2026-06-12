
def main():
    #
    word_count = {}

    while True:
        print("=========================================")
        print("Word Frequency Counter")
        print("=========================================")
        print("1. Analyse a sentence")
        print("2. View word counts")
        print("3. View most frequent word")
        print("4. Clear results")
        print("0. Exit")
        try:
            print("=========================================")
            user_input = int(input("Please select an option(1-4) or 0 to exit: "))
            print()
            match user_input:
                case 1:
                    case_1(word_count)
                    print()
                    
                case 2:
                    case_2(word_count)
                    print()
                    
                case 3:
                    case_3(word_count)
                    print()
                case 4:
                    case_4(word_count)
                    print()
                case 0:
                    print("exiting program...Goodbye.")
                    break
                case _:
                    print("Invalid selection.")
                    continue
        except ValueError:
            print("Invalid selection. Please type an integer.")
            continue


def case_1(word_count):
        
        processed_words = 0
        sentence = input("Please enter a sentence: ").lower()  #ignore case
        for word in sentence.split():
            if word.isalpha():   #decided not to count symbols or digits in dictionary
                word_count[word] = (word_count.get(word,0)) + 1  #get word but if nonexistent get 0, add 1, store in dict
                processed_words += 1
        print(f"---{processed_words} words were processed---")
        return

def case_2(word_count):
    """- If `word_count` is empty, print a message saying no words have been analysed yet
- Otherwise loop over itmes in `word_count` and display each word and its count in a formatted list, sorted alphabetically"""
    if not word_count:
        print("No words have been analyzed yet")
    else:
        print(f"{'word':<20} | {'count':>5}")
        print("------------------------------")
        sorted_words = sorted(word_count.items()) # returns a sorted list of tuples
        for word,count in sorted_words: #unpack tuples
            print(f"{word:<20} | {count:>5}")
    return

    
def case_3(word_count):
    """- If `word_count` is empty, print a message saying no words have been analysed yet
- Otherwise find and display the word with the highest count"""
    if not word_count:
        print("No words have been analyzed yet.")
    else:
        max_count = max(word_count, key = word_count.get)
        print(f"Most frequent word: {max_count}.")

    return

def case_4(word_count):
    """- Clear the `word_count` dictionary
- Print a confirmation message"""
    word_count.clear()
    print("Dictionary has been cleared!")



if __name__ == "__main__":
    main()