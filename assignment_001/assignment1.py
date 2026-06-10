import random

if __name__ == "__main__":
    # Generate a random number between 1 and 20
    winning_number = random.randint(1, 20)
    # Set a maximum guess limit of 8 guesses
    MAX_GUESSES = 8
    # Track the number of guesses using a counter variable
    used_guesses = 0
    # Flag to track if winning number was found
    found = False

    # Create a while loop that runs as long as the guess count is under the limit
    while used_guesses < MAX_GUESSES:
        # prompt the user to enter a guess
        guess = int(input("Guess a number between 1 and 20:"))
        # Check that guessed number is within specified range
        if not 1 <= guess <= 20:
            print("Guess must be between 1 and 20. Try again!")
            continue

        if guess == winning_number:
            print("Correct!")
            found = True
            break
        elif guess > winning_number:
            print("Too high!")
        else:  # guess < winning_number
            print("Too low!")
        # Increment the guess counter on each iteration
        used_guesses += 1
        # Display number of remaining guesses
        print(f"Guesses Remaining:{MAX_GUESSES - used_guesses}")
    # User did not guess the number
    if not found:
        print(f"No more guesses! The correct number was {winning_number}")
