word_count = {}

def main_menu():
    print(f"\n{"=" * 10}\nWord Frequency Counter\n{"=" * 10}\n1. Analyze a sentence\n2. View word counts\n3. View most frequent word\n4. Clear results\n5. Exit\n\n")

def analyze_sentence(sentence:str):
    words = sentence.lower().split()
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

def view_word_counts():
    if len(word_count) == 0:
        print("No words have been analyzed yet! Do that first!!!")
    else:
        for word, count in sorted(word_count.items()):
            print(f"{word:<12} : {count}")

def most_frequent_word():
    if len(word_count) == 0:
        print("No words have been analyzed yet! Do that first!!!")
    else:
        most_word = max(word_count, key=word_count.get)
        print(f"Most frequent word: {most_word}")

def clear_results():
    word_count.clear()
    print("Word counts cleared!")

while True:
    main_menu()
    user_input = input("Select an option: ")

    match user_input:
        case '1':
            input_sentence = input("Please enter a sentence you would like analyzed: ")
            analyze_sentence(input_sentence)
        case '2':
            view_word_counts()
        case '3':
            most_frequent_word()
        case '4':
            clear_results()
        case '5':
            print("Thank you for using our program!\n")
            break
        case _:
            print("User input must be an integer, please re-try.\n\n")