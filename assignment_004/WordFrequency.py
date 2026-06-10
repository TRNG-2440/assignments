"""
Build a console-based Word Frequency Counter that takes a sentence from the user, 
counts how many times each word appears, and displays the results. 
The user should be able to analyse multiple sentences in a loop until 
they choose to exit. This activity focuses on dictionaries and practices string methods, 
for loops, while loops, if-else, and input().

"""

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

# Algorithm used to analyze sentence
def AnalyzeSentence() -> list:
  sentence = input('Enter sentence: ')

  return [w.strip() for w in sentence.split()]

# Determine the number of words within a sentence
def WordCount(wordList) -> None:

  # Declare dictionary to keep track of each word
  wordDictionary = dict()

  # Determine
  for w in wordList:
    wordDictionary[w] += 1

  # Determine word count for each word
  for w in wordList:
    print(f'{w} : {wordDictionary[w]}')
  
# Determine most frequent word
def MostFrequentWord(wordList) -> int:

# Declare dictionary to keep track of each word
  wordDictionary = dict()

  # Determine word count for each word
  for w in wordList:
    wordDictionary[w] += 1

  # Return most frequent word
  return list.max(wordDictionary.values())

# Clear word
def ClearWord(wordList) -> None:
  wordList.clear()

# Main menthod
def main():

  # Display main menu
  Menu()



main()