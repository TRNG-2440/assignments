import random

# Generate random number
randomNumber = random.randint(1,20)

# Declare counter variable
count = 1

# Declare boolean to determine if guess is correct
guessBool = False

# Prompt user to guess number 8 times
while (count - 1) < 8:
  guessedNumber = int(input(f'\n{count}) Guess random number: '))

  if(guessedNumber == randomNumber):
    print('Congratulations ', guessedNumber, 'is the correct number!\n')
    guessBool = True
    break

  elif guessedNumber > randomNumber:
    print(guessedNumber, ' is too high, please try again\n')
    count += 1

  elif guessedNumber < randomNumber:
    print(guessedNumber, ' is too low, please try again\n')
    count += 1

  if(guessBool == False):
    print(f'\nYou have {8-(count-1)} guesses left')

if(guessBool == False):
  print(f'No more guesses!  The number is {randomNumber}')

