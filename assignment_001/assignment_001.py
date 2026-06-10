import random

secret_number = random.randint(1, 20)
guess_limit = 8
attempts = 0

while attempts < guess_limit:
    guess = int(input("Guess the number I generated, it is a number between 1 and 20 "))
    attempts +=1
    
    if guess < secret_number:
        print(f"That is too low, you have {guess_limit - attempts} attempts left")
    elif guess > secret_number:
        print(f"That is too high, you have {guess_limit - attempts} attempts left")
    else:
        print(f"Congratulations! You guessed the number {secret_number} correctly in {attempts} attempts.")
        break
else:
    print(f"You used up all your attempts. The number was {secret_number}.")