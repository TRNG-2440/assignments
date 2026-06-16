import random


randNumber = random.randint(1, 20)
maxGuesses = 8
remainingGuesses = maxGuesses
countGuesses = 0

while(remainingGuesses > 0):
    
    userGuess = int(input("Enter your guess: "))
    
    if(userGuess == randNumber):
        print("Correct!")
        break
    elif(userGuess < randNumber):
        print("Too low!")
    else:
        print("Too high!")
        
    remainingGuesses -= 1
    countGuesses += 1
    
    print("You have", remainingGuesses, "guesses remaining.")

print("You have run out of guesses. The number was", randNumber)