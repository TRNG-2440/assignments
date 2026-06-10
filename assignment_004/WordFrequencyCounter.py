word_count = {}

while True: # top menu
    print ("1. Analyze a sentence")
    print ("2. View word counts")
    print ("3. View most frequent word")
    print ("4. Clear results")
    print ("0. Exit")

    choice = input("Pick an option: ")
    match choice:
        case "1": # analyze a sentence
            sentence = input("Enter a sentence: ")
            sentence = sentence.lower()
            words = sentence.split()
            
            c = 0
            for word in words:
                word_count.update({word: word_count.get(word, 0) + 1})
                c += 1

            print (f"Words processed: {c}")

        case "2": # sort and print the words and their frequency
            if (word_count):
                sorted_words = dict(sorted(word_count.items()))
                for word, count in sorted_words.items():
                    print(f"{word}: {count}")
                print("")
            else:
                print ("No words have been analyzed yet.\n")

        case "3": # find word with highest frequency
            if (word_count):
                max_count = 0
                max_item = ()
                for word_item in word_count.items():
                    if word_item[1] > max_count:
                        max_count = word_item[1]
                        max_item = word_item
                print (f"Most frequent word: {max_item[0]} ({max_item[1]} times)\n")
            else:
                print ("No words have been analyzed yet.\n")

        case "4":
            word_count.clear()
            print ("Word count reset.\n")

        case "0":
            print("Goodbye!")
            break