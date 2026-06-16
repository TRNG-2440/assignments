word_count = {}


while True:
    print("1. Analyze a sentence")
    print("2. View word count")
    print("3. View most frequent words")
    print("4. Clear results")
    print("0. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "0" or choice == "Exit":
        print("Exiting...")
        break
    
    elif choice == "1" or choice == "Analyze a sentence":
        
        sentence = input("Enter a sentence: ")
        sentence = sentence.lower()
        words = sentence.split()
        
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
            print(f"Word count updated. Total  words: {len(words)}")
            
    elif choice == "2" or choice == "View word count":
        
        if len(word_count) == 0:
            print("No words analyzed yet.")
        else:
            for word, count in sorted(word_count.items()):
                print(f"  {word}: {count}")
                
    elif choice == "3" or choice == "View most frequent words":
        
        if len(word_count) == 0:
            print("No words analyzed yet.")
        else:
            max_count = 0
            max_word = ""
            for word, count in word_count.items():
                if count > max_count:
                    max_count = count
                    max_word = word
            print(f"Most frequent word: {max_word}")
            
    elif choice == "4" or choice == "Clear results":
        
        word_count.clear()
        print("Results cleared.")
        
    else:
        print("Invalid choice. Please try again.")
