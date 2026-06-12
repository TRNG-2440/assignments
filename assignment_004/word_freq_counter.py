import os
from time import sleep
import time
"""
    1. Start with getting user input until the user exits:
        - just keep one common dict for all words (from all sentences)

        1. Analyze a sentence
            - ask user to enter sentence (case insensitive)
            - split sentence
            - count occurance of each word
            - count how many words processed and tell that to the user
        
        2. View word counts
            - if empty --> say empty
            - present all words in list ALPHABETICALLY

        3. View most frequent word
            - if empty --> say empty
            - return the word with highest count (if tie, return in alphabetical order)
        
        4. Clear results
            - set curr dict to empty dict
            - print conf msg
        
        0. Exit
"""

# def clear_console():
#     os.system("clear")

def clear_console():
    print("\033[2J\033[H", end="")

def analyze_sentence(word_counter):
    """
    1. Analyze a sentence
        - ask user to enter sentence (case insensitive) -- Done
        - split sentence -- Done
        - count occurance of each word -- Done
        - count how many words processed and tell that to the user -- Done
    """
    while True:
        sentence = input("\nHi! Please type the sentence you want to analyze:  ").strip().upper()
        if not sentence:
            print("\nSentence can't be empty, try again!")

        else: break
    
    word_list = sentence.split()

    for w in word_list:
        w = w.strip(".,!?;:\"'")
        if not w:
            continue
        word_counter[w] = 1 + word_counter.get(w, 0)

    print(f"Analyzed {len(word_list)} words!\n")


def view_word_counts(word_counter):
    if not word_counter:
        print("\nThere are no words to display")
        return
    
    top_words = sorted(word_counter, key=lambda x: -word_counter[x])
    print("Word Counts:")
    print("----------------")

    for w in top_words:
        print(f"{w:<12}{word_counter[w]:<12}")

    # for w, c in word_counter.items():
    #     print(f"{w:<11}{c:<11}")
        

def view_k_freq_word(word_counter, k):
    if not word_counter or k==0:    # handeled base case
        print("\nThere are no words to display")
        return
    
    top_words = sorted(word_counter, key=lambda x: (-word_counter[x], x))

    print(f"Here is a list of the {k} most frequent words:")
    print("-----------------------------------------------")
    for w in top_words[:k]:
        print(f" \"{w}\" — {word_counter[w]} times")


def clear_dict(word_counter):
    if not word_counter:
        print("\nYour dictionary is empty, no words to clear!")
        return
    word_counter.clear()
    print("All results cleared!")


def search_word(word_counter):
    while True:
        word = input("\nHi! Please type the sentence you want to analyze:  ").strip().upper().strip(".,!?;:\"'")
        if not word:
            print("\nSentence can't be empty, try again!")
        elif len(word.split()) > 1:
            print("\nYour word was too long, please enter one word...")
        elif word not in word_counter:
            print("\nSorry, but that word is not in your current dictionary...")
            answer = input("Would you like to create a new sentence with that word? (Yes or No)").upper()
            if answer == "YES":
                analyze_sentence(word_counter)
            elif answer == "NO":
                continue
            else:
                print("\nSorry I did not recognize that. Rerouting you back to word search...")

        else: break


    print(f"\n{word} found!")
    print(f"{word} had been counted {word_counter[word]} times")
 

def main():
    word_counter = {}

    while True:
        print("\nHi, welcome to the Word Frequency Counter!")
        print("Here is our menu: \n1. Analyse a sentence \n2. View word counts \n3. View most frequent word \n4. Clear results \n5. Search for a word \n0. Exit")

        try:
            user_choice = int(input("How would you like to proceed? (enter a number)  "))
        except ValueError:
            print("Please enter a number!")
            continue

        if user_choice == 1:
            clear_console()
            analyze_sentence(word_counter)
        
        elif user_choice == 2:
            clear_console()
            view_word_counts(word_counter)
        
        elif user_choice == 3:
            clear_console()
            while True:
                try:
                    number = int(input("How many top words would you like displayed?  "))
                except ValueError:
                    print("Please enter a number!")
                    continue
                if 0 < number <= len(word_counter):
                    break
                print("Please enter a valid number")

            view_k_freq_word(word_counter, number)
        
        elif user_choice == 4:
            clear_console()
            clear_dict(word_counter)
        
        elif user_choice == 5:
            clear_console()
            search_word(word_counter)
        
        elif user_choice == 0:
            clear_console()
            print("Goodbye!")
            break
        
        else:
            clear_console()
            print("\nInvalid option! Please choose 0-5.")
        
        # sleep(3)


if __name__ == "__main__":
    main()