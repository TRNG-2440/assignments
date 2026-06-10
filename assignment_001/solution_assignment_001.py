import random

def numberGuesser():
    num = random.randint(1, 20)
    MAX_GUESSES = 8
    guess_counter = 0

    while guess_counter < MAX_GUESSES:
        curr_guess = int(input("Guess a number between 1 and 20: "))
        guess_counter += 1

        if curr_guess < 1 or curr_guess > 20:
            print("Invalid guess!")
            print(f"{MAX_GUESSES - guess_counter} guesses remaining ...")
        elif curr_guess > num:
            print("Too high!")
            print(f"{MAX_GUESSES - guess_counter} guesses remaining ...")
        elif curr_guess < num:
            print("Too low!")
            print(f"{MAX_GUESSES - guess_counter} guesses remaining ...")
        else:
            print("Correct!")
            break
        
    if guess_counter == MAX_GUESSES:
        print("No more guesses!")
        print(f"The correct number was {num}.")
        
numberGuesser()