# libraries 
from random import randint

# generate answer (1-20)
answer = randint(1, 20)

# max number of guesses and guess counter
max_guesses = 8
counter = 0

while counter < max_guesses:
    # user guess
    guess = int(input("Guess a number between 1 and 20: "))

    if guess > answer:
        print("Too high!")
    elif guess < answer:
        print("Too low!")
    else:
        print("Correct!")
        break

    counter += 1

    print(f"You have {max_guesses - counter} guesses left.")

if counter == max_guesses:
    print(f"No more guesses! The number was {answer}.")