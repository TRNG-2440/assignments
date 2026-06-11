# This function breaks the sentence into a list of individual words
# Note: there is no counting being done here, this is simply to clean the data so it can be counted
def stringToWordList(sentence):
    word_list = []
    current_word = ""
    for letter in sentence:
        current_word=current_word.strip()
        if (not letter.isalnum()) and current_word: # If word has ended, and current word is not null
            word_list.append(current_word.lower())  # make word lowercase and add it to the word list
            current_word = ""
            continue
        if letter != "" and letter != " ":
            current_word += letter
    if current_word: # If theres still a word in my word buffer
        word_list.append(current_word.lower())
    return word_list

# This takes a clean list of words, not a sentence, as well as a dictionary of words to add
def updateWordCount(currentDict, word_list):
    combined_dict = {}
    for word in word_list
    return combined_dict


# Main while loop
# Get User Input
    #1. Analyze a sentence
        # Strip words out of a sentence
        # 
    #2. View word counts
    #3. View most frequent word
    #4. Clear results
    #0. Exit
# Print Menu
print(  "--------------------------------\n" \
        "     Word Frequency Counter     \n" \
        "--------------------------------\n" \
        "1. Analyse a sentence\n" \
        "2. View word counts\n" \
        "3. View most frequent word\n" \
        "4. Clear Results\n" \
        "0. Exit\n")

while True:
    user_input = input( "\n--------------------------------\n" \
                        "Select an option: ")
    if user_input == "0":
        break
    elif user_input == "1":
        
        # Test: The   quick brown  fox jumps 12? over      the lazy dog. True
        user_input = input("Enter a sentence: ") # Get sentence
        word_list = stringToWordList(user_input) # convert to word list
        
        # The following is sanity check
        #for word in word_list:
            #print(word)
        # Count list

        continue
    elif user_input == "2":
        continue # TODO
    elif user_input == "3":
        continue # TODO
    elif user_input == "4":
        continue # TODO
    elif user_input == "5":
        continue # TODO
    else:
        print("Invalid Input!\n")