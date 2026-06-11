"""
Build a console-based Word Frequency Counter that takes a sentence from the user, 
counts how many times each word appears, and displays the results. 
The user should be able to analyse multiple sentences in a loop until 
they choose to exit. This activity focuses on dictionaries and practices string methods, 
for loops, while loops, if-else, and input().

"""
# ------------------------------------------------------------------------

# Main menu
def Menu():

  print("\n------------------------------"\
  "\n     Word Frequency Counter"\
  "\n------------------------------"\
  '\n1. Analyse a sentence'\
  '\n2. View word counts'\
  '\n3. View most frequent word'\
  '\n4. Clear results'
  '\n0. Exit\n')

# ------------------------------------------------------------------------

# Algorithm used to analyze sentence
def AnalyzeSentence() -> list:
  sentence = input('\nEnter sentence: ')

  while(True):

    if not sentence:

      print('\nError - sentence cannot be empty, please re-enter\n')

      sentence = input('\nEnter sentence: ')
    
    else:
      break

  return [w.strip() for w in sentence.split()]

# ------------------------------------------------------------------------

# Determine the number of words within a sentence
def WordCount(word_count) -> None:

  # Add space
  print()

  print("\n------------------------------"\
  "\n     Word Counts"\
  "\n------------------------------")

  # Determine word count for each word
  for w in word_count:
    print(f'{w} : {word_count[w]}')

# ------------------------------------------------------------------------
  
# Determine most frequent word
def MostFrequentWord(word_count) -> str:

  # Retreive word with most frequent count
  maxWord = max(word_count, key=word_count.get)

  # Retreive most frequent count
  maxCount = word_count[maxWord]

  # Return most frequent word
  return f'\nMost frequent word: "{maxWord}" ({maxCount} time{"s" if maxCount > 1 else ""})'

# ------------------------------------------------------------------------

# Reset program
def ClearWord(wordList,word_count) -> None:

  wordList.clear()

  word_count.clear()

# ------------------------------------------------------------------------

# Main menthod
def main():

  # Declare variable that collects words
  wordList = [] 

  # Declare dictionary to keep track of each word
  word_count = dict()

  while(True):

    # Display main menu
    Menu()

    # Prompt user
    option = input('Input Option: ')

    match(option):

        case "0":

            # Print exit message
            print("\nProgram has been terminated.\n")

            print("Goodbye!\n")

            # Terminate program
            break

        case "1":

            # Implement sentence algorithm
            wordList = AnalyzeSentence()

            # Determine
            for w in wordList:
              word_count[w] = word_count.get(w, 0) + 1 

            # Print confirmation message
            print('\nSentence has been sucessfully analyzed')

        case "2":

            # Count word
            WordCount(word_count)

        case "3":

            # Print the most frequent word
            print(MostFrequentWord(word_count))

        case "4":

            # Clear list and dictionary
            ClearWord(wordList,word_count)

            print('\nList successfully cleared\n')

        case _:

            # Alert user that invalid entry was entered
            print('\nInvalid entry - please re-enter option')


main()