main_menu = True

print("════════════════════════════════════════")
print("       WORD FREQUENCY COUNTER           ")
print("════════════════════════════════════════")
print("1. Analyse a sentence")
print("2. View word counts")
print("3. View most frequent word")
print("4. Clear results")
print("0. Exit")
print("════════════════════════════════════════")

while main_menu:
    choice = int(input("Select an option: "))
    print()
    
    match choice:
        case 1:
            sentence = input("Enter a sentence: ")
            word_counts = {}
            for word in sentence.split():
                word = word.lower()
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1
            print("Sentence analysed successfully!")
            print()
            print("════════════════════════════════════════")

        case 2:
            if not word_counts:
                print("No sentence analysed yet.")
                print()
                continue
            else:
                print("Word Counts:")
                print("────────────────────────────────────────")
                for word, count in word_counts.items():
                    print(f"{word:<10} | {count}")
                print("-────────────────────────────────────────")
                print("Total unique words:", len(word_counts))
                print()
                print("════════════════════════════════════════")
                continue
        case 3:
            if not word_counts:
                print("No sentence analysed yet.")
                print()
                continue
            else:
                for word, count in word_counts.items():
                    if count == max(word_counts.values()):
                        print(f"Most frequent word: \"{word}\"  ({count} times)")
                print()
                print("════════════════════════════════════════")
                continue
        case 4:
            word_counts.clear()
            print("Results cleared successfully!")
            print()
            print("════════════════════════════════════════")
            continue
        case 0:
            print("Goodbye!")
            break
        case _:
            print("Invalid choice. Please try again.")
            print()
            print("════════════════════════════════════════")
            continue
    