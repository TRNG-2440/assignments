#Solution for Assignment 001
#Alex Tran

import random

random_num = random.randint(1,20)
num_guesses, max_guesses = 8, 8
counter = 0

while counter < max_guesses:
    ans = int(input("Enter your guess: "))
    counter += 1
    num_guesses -= 1 
    #check the answer 
    if ans > random_num:
        print("Too high!")
        print(f"Remaning guesses: {num_guesses}")
    elif ans < random_num:
        print("Too low!")
        print(f"Remaning guesses: {num_guesses}")
    else:
        print("Correct!")
        break

if num_guesses == 0 and ans != random_num:
    print("No more guesses!")
    print(f"The number is {random_num}")
