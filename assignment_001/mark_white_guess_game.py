import random

secret_number = random.randint(1, 20)
max_attempts = 8
attempts = 0

while attempts < max_attempts:
    guess = int(input("Guess the number between 1 and 20: "))
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
