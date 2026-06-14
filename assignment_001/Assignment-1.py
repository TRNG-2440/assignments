import random

answer = random.randint(1, 20)

counter = 0

while counter < 8:

    guess = int(input("Input a random number! "))

    if guess > answer:
        print("Too High! ")
    elif guess < answer:
        print("Too Low! ")
    else:
        print("Correct! ")
        break
    
    counter += 1

    print(f"You have {8 - counter} guesses left! ")

if counter == 8:
    print(f"No more guesses! The correct number was {answer}")
