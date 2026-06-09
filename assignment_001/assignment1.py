import random

number = random.randint(1, 20) # number the user has to find

c = 0 # counter
max_guesses = 8

while c < max_guesses: 
    guess = int(input("Enter your guess: "))
    c += 1

    if guess > number:
        print("Too High!")
    elif guess < number:
        print("Too Low!")
    else:
        print("Correct!\n")
        break

    print (f"Guesses remaining: {max_guesses - c}\n")

if c >= max_guesses:
    print (f"No more guesses!\nCorrect answer: {number}")