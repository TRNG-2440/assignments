# word frequency counter
word_count = {}

# main loop
while True:
    # options
    print("════════════════════════════════════════")
    print("         TO-DO LIST MANAGER")
    print("════════════════════════════════════════")
    print("1. Analyse a sentence")
    print("2. View word counts")
    print("3. View most frequent word")
    print("4. Clear results")
    print("0. Exit")

    choice = int(input("Select an option: "))

    match choice:
        case 0: # exit
            print("Goodbye!")
            break

        case 1: # analyse sentence
            print("")
            sentence = input("Enter a sentence: ")
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


        case 4: # clear results
            print("")
            word_count.clear()
            print("Results cleared. Returning to main menu.")
            print("")