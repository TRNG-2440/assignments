import random 

number = random.randint(1, 20)
guess_limit = 8
guess_count = 0

while guess_count < guess_limit:
    guess = int(input("Enter a number between 1 and 20: "))
    guess_count += 1

    if guess > number:
        print("Too high!")
        print(f"You have {guess_limit - guess_count} guesses remaining.")

    elif guess < number:
        print("Too low!")
        print(f"You have {guess_limit - guess_count} guesses remaining.")
    
    else:
        print("Correct!")
        break

    if guess_count == guess_limit and guess != number:
        print("No more guesses!")
        print(f"The number was {number}.")
        