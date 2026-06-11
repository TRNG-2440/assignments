    #1. Analyze a sentence
# This function breaks the sentence into a list of individual words
# Note: there is no counting being done here, this is simply to clean the data so it can be counted
def stringToWordList(sentence):
    if sentence:
        print("There are no words to process")
    word_list = []
    current_word = ""
    for letter in sentence:
        if letter.isalpha():
            current_word += letter
            #print(f"adding {letter}")
        else:
            current_word.strip()
            if current_word:
                word_list.append(current_word.lower())  # make word lowercase and add it to the word list
            current_word = ""
            continue
    if current_word: # If theres still a word in my word buffer
        word_list.append(current_word.lower())

    if not word_list:
        print("No words have been processed")
    else:
        print(f"Done! Processed {len(word_list)} words")
    return word_list

# This takes a clean list of words, not a sentence, as well as a dictionary of words to add
def updateWordCount(current_dict, word_list):
    combined_dict = {}
    for word in word_list:
        if current_dict.get((word)) == None:
            current_dict[word] = 1
        else:
            current_dict[word] += 1
    return combined_dict

    #2. View word counts
def printWordCount(word_count):
    if not word_count:
        print("There are no words to count!")
        return
    print(  "\nWord Counts:\n " \
            "--------------------------------\n" )
    for key, val in word_count.items():
        print(  f"   {key:<20}{val:>4}")
    print(   "--------------------------------\n" \
            f"   Total unique words: {len(word_count)}")

    #3. View most frequent word
def mostFrequentWord(word_count):
    if not word_count:
        print("No words have been analyzed!\nPlease add a sentence before using this commmand")
        return
        
    mode_word = "" # Mode aka most frequent
    mode_count = 0
    for word, count in word_count.items():
        if count > mode_count:
            mode_word = word
            mode_count = count
    print(f"\nThe most frequent word is \"{mode_word}\" ({mode_count} times)\n")

    #4. Clear results
# Done below

    #5. Word search
# Also done below


print(  "--------------------------------\n" \
        "     Word Frequency Counter     \n" \
        "--------------------------------\n" \
        "1. Analyze a sentence\n" \
        "2. View word counts\n" \
        "3. View most frequent word\n" \
        "4. Clear Results\n" \
        "5. Search for a word\n" \
        "0. Exit\n")

user_input  = ""
word_count = {}

while True:
    user_input = input( "\n--------------------------------\n" \
                        "Select an option: ")
    if user_input == "0":
        break
    elif user_input == "1":
        
        # Test: The   quick brown  fox jumps 12? over      the lazy dog. True
        # Test2: Hello World!
        user_input = input("Enter a sentence: ") # Get sentence
        word_list = stringToWordList(user_input) # convert to word list
        # The following is sanity check
        #for word in word_list:
            #print(word)
        # Count list
        updateWordCount(word_count, word_list)
        continue
    elif user_input == "2":
        printWordCount(word_count)
        continue
    elif user_input == "3":
        mostFrequentWord(word_count)
        continue
    elif user_input == "4": # Clear results
        if word_count:
            word_count = {}
            print("All results have been cleared!")
        else:
            print("No words have been analyzed yet!")
        continue
    elif user_input == "5": # word search
        lookingForThisWord = input("What word would you like to search for: ")
        how_many = word_count.get(lookingForThisWord)
        if how_many:
            print(f"\nThe word {lookingForThisWord} is present {how_many} times!\n")
        else:
            print("\nThis word has not been analyzed yet")
        continue
    else:
        print("Invalid Input!\n")