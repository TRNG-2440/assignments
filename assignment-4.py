
def count_freq():

    word_count = {}
   
    while True:

        print("-" * 30)
        print("WORD FREQUENCY COUNTER")
        print("-" * 30)
        print("1. Analyse a sentence")
        print("2. View word counts")
        print("3. View most frequent word")
        print("4. Clear results")
        print("0. Exit")
        print("-" * 30)
        print("Select an option: ")
        option = input()

        if option == '0':
            break
       

        print("Enter a sentence:")
    
        sentence = input()
        words = sentence.split()
        for word in words:
            word = word.lower()
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1


        if option == '1':

            print("Enter a sentence:")

            print(f'✔ Processed {len(words)} words.')
            
        

        elif option == '2':
        
            if not word_count:
                print("No words counted yet.")
            else:
                print("Word Counts:")
                print("-" * 30)
                sorted_dict = dict(sorted(word_count.items()))
                for word, count in sorted_dict.items():
                    print(f"{word}:    {count}")
                print("-" * 30)
                print("Total unique words:", len(word_count))
            

        elif option == '3':
            if not word_count:
                print("No words counted yet.")
            else:
                most_frequent_word = max(word_count, key=word_count.get)
                frequency = word_count[most_frequent_word]
                print(f"Most frequent word: '{most_frequent_word}' ({frequency} times)")
            

        elif option == '4':
            word_count.clear()
            print("✔ Word count has been cleared.")     

        else:
            print("Please try again.")

count_freq()