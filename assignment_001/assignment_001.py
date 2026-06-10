import random

max_guess = 8
number_to_guess = random.randint(1, 20)
number_of_guesses = 0
while number_of_guesses < max_guess:
    guess = int(input("Guess a number between 1 and 20: "))
    number_of_guesses += 1
    guesses_remaining = max_guess - number_of_guesses

    if guess < number_to_guess:
        print("Too low!")
        print(f"Guesses remaining: {guesses_remaining}")
    elif guess > number_to_guess:
        print("Too high!")
        print(f"Guesses remaining: {guesses_remaining}")
    else:
        print("Correct!")
        break
else:
    print("No more guesses!")
    print(f"The number was: {number_to_guess}")