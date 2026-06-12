word_count = {}

while True:
    print("================================")
    print("WORD FREQUENCY COUNTER")
    print("================================")
    print("1. Analyse a sentence")
    print("2. View word counts")
    print("3. View most frequent word")
    print("4. Clear results")
    print("0. Exit")
    print("================================")

    category = input("Select an option: ")

    match category:
        case "1":
            sentence = input("Enter a sentence to analyse: ")
            if sentence:
                words = sentence.lower().split()
                for word in words:
                    word_count[word] = word_count.get(word, 0) + 1
                print("Processed amount of words: ", len(words))
            else:
                print("No sentence entered.")
        case "2":
            if word_count:
                for word, count in word_count.items():
                    print(f"{word}: {count}")
            else:
                print("No word counts available.")
        case "3":
            if word_count:
                most_frequent_word = max(word_count, key=word_count.get)
                print(f"Most frequent word: {most_frequent_word} (appears {word_count[most_frequent_word]} times)")
            else:
                print("No word counts available.")
        case "4":
            word_count.clear()
            print("Results cleared.")
        case "0":
            print("Exiting...")
            break
        case _:
            print("Invalid option. Please try again.")