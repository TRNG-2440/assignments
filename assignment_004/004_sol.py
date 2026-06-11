#Code solution for Assignment 4
#Alex Tran

#Word Frequency Counter

word_count = {}

while True:
    print("\n=== WORD FREQUENCY COUNTER ===")
    print("1. Analyze a sentence")
    print("2. View word counts")
    print("3. View most frequent word")
    print("4. Clear results")
    print("5. Exit")

    option = input("Enter your choice: ")

    #Analyze sentence

    if option == "1":
        sentence = input("Enter a sentence: ")
    
        #Ignore casing
        sentence = sentence.lower()

        #split sentence into words
        words = sentence.split()

        for word in words:
            if word in word_count:
                word_count[word] +=1
            else:
                word_count[word] = 1
        
        print(f"{len(words)} processed.")


    #Display word count
    elif option == "2":
        if len(word_count) == 0:
            print("No words have been analysed. ")
        else:
            print("\n---Word Counts ---")
            for word in sorted(word_count):
                print(f"{word}: {word_count[word]}")
    
    #view most frequent word
    elif option == "3":
        if len(word_count) == 0:
            print("No words have been analysed. ")
        else:
            most_freq_word = ""
            highest_count = 0

            for word, count in word_count.items():
                if count > highest_count:
                    highest_count = count
                    most_freq_word = word
            print(f"Most frequent word: {most_freq_word}")
            print(f"Number of times: {highest_count}")

    #clear word counts
    elif option == "4":
        word_count.clear()
        print("The word count has been cleared.")
    
    elif option == "5":
        print("Exiting program. Goodbye!")
        break

    #Invalid menu option
    else:
        print("Invalid option. Please select a valid number from the menu.")
