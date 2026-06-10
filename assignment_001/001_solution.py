import random

def guessNumber():

    numGuesses = 8
    randomNum = random.randint(1, 20)
    guessedCorrectly = False

    while numGuesses > 0:
        guess = int(input("Enter your guess from 1-20: "))
        numGuesses -= 1
        if guess > randomNum:
            print(f"Too high! You have {numGuesses} left.")
        elif guess < randomNum:
            print(f"Too low! You have {numGuesses} left.")
        else:
            print(f"Correct!")
            guessedCorrectly = True
            break

    if guessedCorrectly != True:
        print(f"No more guesses! The number was {randomNum}.")


guessNumber()

