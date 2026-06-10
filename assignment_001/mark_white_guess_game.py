# Mark White
# 06/09/2026 
# Guess the Number Game

# This program implements a simple "Guess the Number" game. The computer generates a random number between 1 and 20,
# the user has 8 attempts to guess it. After each guess, the program provides feedback on whether the guess is too low, 
# too high, or correct. If the user fails to guess the number within 8 attempts, the program reveals the secret number.

import random

secret_number = random.randint(1, 20)
max_attempts = 8
attempts = 0

while attempts < max_attempts:
    user_guess = (input("Guess the number between 1 and 20: "))
    

    if not user_guess.isdigit():
        print("Invalid input. Please enter a whole number between 1 and 20.")
        continue

    guess = int(user_guess)

    if guess < 1 or guess > 20:
        print("Invalid input. Please enter a whole number between 1 and 20.")
        continue
    
    attempts +=1
    
    if guess < secret_number:
        print("Too low! Try again.")
    elif guess > secret_number:
        print("Too high! Try again.")
    else:
        print(f"Congratulations! You guessed the number {secret_number} correctly in {attempts} attempts.")
        break
else:
    print(f"Sorry, you've used all {max_attempts} attempts. The number was {secret_number}.")
