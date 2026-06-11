# Mark White
# 06/11/2026
# Word Counter

# This program counts the occurrences of each word in user-inputted sentences.
# The user can enter sentences, and the program will keep track of how many times each word has been used.
# After each sentence, it displays the current word count for all words entered so far.
# The program will continue to run until the user types "quit" to exit.


word_count = {}


def display_word_count():

    # Loop for user input, counting words, and exiting the program
    while True:
        user_sentence = input("Type a sentence (or 'quit' to exit): ")
        if user_sentence.lower() == 'quit':
            print("\n Exiting word counter, goodbye!")
            break

        # Split the sentence into words and count them
        for word in user_sentence.split():
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

        # Display the current word count
        print("\nWord Count:")
        for word, count in word_count.items():
            print(f"{word}: {count}")

if __name__ == "__main__":
    display_word_count()