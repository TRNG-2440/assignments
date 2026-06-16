word_count = {}

while True: 
    print("\n======= WORD FREQ COUNTER =======")
    print("1. Analyze a sentence")
    print("2. View word counts")
    print("3. View most frequent word")
    print("4. Clear results")
    print("5. Exit")

    choice = input("Select an option:")

    if choice == "1":
        sentence = input("Enter a sentence: ")
        words = sentence.split()

        for word in words:
            word = word.lower()
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
                
        print(f"Processed {len(words)} words.")

    elif choice == "2":
        if word_count:
            print("No words have been analyzed yet.")
        else:
            print("\nWord Counts:")
            for word in sorted(word_count):
                print(f"{word}: {word_count[word]}")

            print(f"\nTotal unique words: {len(word_count)}")
    
    elif choice == "3":
        if not word_count:
            print("No words have been analyzed yet.")
        else:
            most_frequent_word = max(word_count, key=word_count.get)
            count = word_count[most_frequent_word]

            print(f'Most frequent word: {most_frequent_word} ({count} times)')

    elif choice == "4":
        word_count.clear()
        print("Results cleared.")
    
    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Please try again.")