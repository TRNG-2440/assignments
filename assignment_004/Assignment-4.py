word_count = {}
word_list = []


while True:

    choose = input('''
════════════════════════════════════════
Word Frequency Counter
════════════════════════════════════════
1. Analyse a sentence
2. View word counts
3. View most frequent word
4. Clear results
0. Exit
''')


    match choose:
        case "1":
            sent = input("Please enter a sentence for analysis: ")

            word_list = sent.lower().split()

            for w in word_list:
                word_count[w] = word_count.get(w, 0) + 1
            
            print(f"{len(word_count)} words processed!")

        case "2":
            if not word_list:
                print("No words have been analyzed!")
            else:
                word_count = dict(sorted(word_count.items(), key = lambda item: item[1], reverse = True))
                for k, v in word_count.items():
                    
                    print(f"\"{k}\" occurs {v} times")

        case "3":
            if not word_list:
                print("No words have been analyzed!")

            else: 
                most = max(word_count.items(), key = lambda item: item[1])
                print(f"\"{most[0]}\" is the most frequent word and occurs {most[1]} times!")
        case "4":
            word_count.clear()
            word_list.clear()
            print("Word counts have been reset!")
        case "0":
            print("Bye, have a good time!")
            break
        case _:
            print("I do NOT recognize that")