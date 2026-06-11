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
def WordCount(wordList) -> None:

  # Add space
  print()


  print("\n------------------------------"\
  "\n     Word Counts"\
  "\n------------------------------")

  # Declare dictionary to keep track of each word
  wordDictionary = dict()

  # Determine
  for w in wordList:
    wordDictionary[w] = wordDictionary.get(w, 0) + 1

  # Determine word count for each word
  for w in wordDictionary:
    print(f'{w} : {wordDictionary[w]}')

# ------------------------------------------------------------------------
  
# Determine most frequent word
def MostFrequentWord(wordList) -> str:

# Declare dictionary to keep track of each word
  wordDictionary = dict()

  # Determine word count for each word
  for w in wordList:
    wordDictionary[w] = wordDictionary.get(w, 0) + 1


  # Retreive word with most frequent count
  maxWord = max(wordDictionary, key=wordDictionary.get)

  # Retreive most frequent count
  maxCount = wordDictionary[maxWord]

  # Return most frequent word
  return f'\nMost frequent word: "{maxWord}" ({maxCount} time{"s" if maxCount > 1 else ""})'

# ------------------------------------------------------------------------

# Reset program
def ClearWord(wordList) -> None:
  wordList.clear()

# ------------------------------------------------------------------------

# Main menthod
def main():

  # Declare global variable that collects words
  wordList = []  

  # Traverse through items
  while(True):

    # Display main menu
    Menu()

    # Declare bool variable to determine if program terminates
    isTerminated = False

    # Prompt user
    option = input('Input Option: ')

    while(True):

      match(option):

        case "0":

          # Terminate program
          isTerminated = True

          # Print exit message
          print("\nProgram has been terminated.\n")

          print("Goodbye!\n")

          break

        case "1":

          # Implement sentence algorithm
          wordList = AnalyzeSentence()

          # Print confirmation message
          print('\nSentence has been sucessfully analyzed')

          break

        case "2":

          WordCount(wordList)

          break

        case "3":

          print(MostFrequentWord(wordList))

          break

        case "4":

          wordList.clear()

          print('\nList successfully cleared\n')

          break

        case _:

          # Alert user that invalid entry was enter
          print('\nInvalid entry - please re-enter option') 

          break

    # Break from loop if program is terminated
    if(isTerminated):
      break


main()