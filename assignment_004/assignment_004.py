# libraries
from string import punctuation

# word frequency counter
word_count = {}

# main loop
while True:
    # options
    print("════════════════════════════════════════")
    print("         WORD FREQUENCY COUNTER")
    print("════════════════════════════════════════")
    print("1. Analyse a sentence")
    print("2. View word counts (alphabetical order)")
    print("3. View most frequent word")
    print("4. Top 3 most frequent words")
    print("5. Search for a word")
    print("6. View Word Counts (Most to Least)")
    print("7. View Word Counts in (Least to Most)")
    print("8. Clear results")
    print("0. Exit")

    choice = int(input("Select an option: "))

    match choice:
        case 0: # exit
            print("Goodbye!")
            break

        case 1: # analyse sentence
            print("")
            sentence = input("Enter a sentence: ")
            sentence = sentence.translate(str.maketrans('', '', punctuation))
            words = sentence.lower().split()
            for word in words:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
            print(f"Processed {len(words)} words. Returning to main menu.")
            print("")

        case 2: # view word counts
            print("")
            if word_count:
                print("Word Counts:")
                print("────────────────────────────────────────")
                for word in sorted(word_count):
                    print(f" {word} : {word_count[word]}")
                print("────────────────────────────────────────")
                print(f" Total unique words: {len(word_count)}")
                print("")
            else:
                print("No words have been analysed yet. Returning to main menu.")
                print("")

        case 3: # view most frequent word
            print("")
            if word_count:
                most_frequent_word, times_appeared = sorted(word_count.items(), key = lambda x: x[1], reverse = True)[0]
                print(f"Most frequent word: '{most_frequent_word}' ({times_appeared} times)")
                print("")
            else:
                print("No words have been analysed yet. Returning to main menu.")
                print("")

        case 4: # top three most frequent words
            print("")
            if word_count:
                top_three = sorted(word_count.items(), key = lambda x: x[1], reverse = True)[0:3]
                for word, times in top_three:
                    print(f"'{word}', used {times} times)")
                print("")
            else:
                print("No words have been analysed yet. Returning to main menu.")
                print("")

        case 5: # search for a word
            print("")
            if not word_count:
                print("No words have been analysed yet. Returning to main menu.")
                print("")
            else:
                word = input("Enter a word to search for: ")
                if word.lower() in word_count:
                    print(f"'{word}' appears {word_count[word.lower()]} times.")
                else:
                    print(f"'{word}' does not appear in the word count. Returning to main menu.")
                    print("")

        case 6: # view word counts by frequency
            print("")
            if not word_count:
                print("No words have been analysed yet. Returning to main menu.")
                print("")
            else:
                print("Word Counts:")
                print("────────────────────────────────────────")
                word_counts = sorted(word_count.items(), key = lambda x: x[1], reverse = True)
                for word, times in word_counts:
                    print(f" {word}: {times}")
                print("────────────────────────────────────────")

        case 7: # view word counts least to most
            print("")
            if not word_count:
                print("No words have been analysed yet. Returning to main menu.")
                print("")
            else:
                word_counts = sorted(word_count.items(), key = lambda x: x[1])
                print("Word Counts:")
                print("────────────────────────────────────────")
                for word, times in word_counts:
                    print(f" {word}: {times}")
                print("────────────────────────────────────────")

        case 8: # clear results 
            print("")
            word_count.clear()
            print("Results cleared. Returning to main menu.")
            print("")

        