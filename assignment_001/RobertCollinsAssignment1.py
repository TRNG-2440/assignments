import random

guesses = 0
current_guess = int(input("Welcome to the Random Number Guessing Game!\nPlease enter your first guess!  "))

def GenerateRandomNum():
    correct_number = random.randint(1, 20)
    return correct_number

answer = GenerateRandomNum()

while guesses < 7:
    if current_guess == answer:
        print(f"\nThe correct number was {answer}.\nYou guessed correctly!\nYou Win!\n")
        break
    elif current_guess < answer:
        current_guess = int(input(f"\nWomp Womp! That number is too low!\nYou have {7-guesses} guesses left!\nPlease input your next guess!  "))
        guesses += 1
    elif current_guess > answer:
        current_guess = int(input(f"\nWomp Womp! That number is too high!\nYou have {7-guesses} guesses left!\nPlease input your next guess!  "))
        guesses += 1
    else:
        pass

if guesses == 7:
    print(f"\nOut of guesses, You lost the game! The correct number was {answer}.\n")

print("Thanks for Playing!\n")