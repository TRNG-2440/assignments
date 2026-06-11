def get_count(item):
    return item[1]


def word_frequency_counter():
    word_count = {}

    while True:
        print("════════════════════════════════════════")
        print("       WORD FREQUENCY COUNTER")
        print("════════════════════════════════════════")
        print("1. Analyse a sentence")
        print("2. View word counts alphabetically")
        print("3. View top 3 most frequent words")
        print("4. Clear results")
        print("5. Search for a word")
        print("6. View word counts by frequency")
        print("0. Exit")
        print("════════════════════════════════════════")

        choice = int(input("Select an option: "))

        match choice:
            case 1:
                sentence = input("Enter a sentence: ").lower()
                words = sentence.split()

                for word in words:
                    word = word.strip(".,!?;:\"'()[]{}")

                    if word:
                        if word in word_count:
                            word_count[word] += 1
                        else:
                            word_count[word] = 1

                print(f"Processed {len(words)} words.")

            case 2:
                if not word_count:
                    print("No words have been analysed yet.")
                else:
                    print("Word Counts:")
                    print("────────────────────────────────────────")

                    for word, count in sorted(word_count.items()):
                        print(f"{word}: {count}")

                    print("────────────────────────────────────────")
                    print(f"Total unique words: {len(word_count)}")

            case 3:
                if not word_count:
                    print("No words have been analysed yet.")
                else:
                    sorted_words = sorted(word_count.items(), key=get_count, reverse=True)

                    print("Top 3 Most Frequent Words:")
                    for word, count in sorted_words[:3]:
                        print(f'"{word}" ({count} times)')

            case 4:
                word_count.clear()
                print("Results cleared.")

            case 5:
                if not word_count:
                    print("No words have been analysed yet.")
                else:
                    search_word = input("Enter a word to search: ").lower().strip(".,!?;:\"'()[]{}")
                    count = word_count.get(search_word, 0)

                    print(f'"{search_word}" appeared {count} times.')

            case 6:
                if not word_count:
                    print("No words have been analysed yet.")
                else:
                    print("Word Counts by Frequency:")
                    print("────────────────────────────────────────")

                    sorted_words = sorted(word_count.items(), key=get_count, reverse=True)

                    for word, count in sorted_words:
                        print(f"{word}: {count}")

            case 0:
                print("Goodbye!")
                break

            case _:
                print("Please choose a valid option.")


word_frequency_counter()