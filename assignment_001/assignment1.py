import random

def generate_random_number(start, stop):
    return random.randint(start, stop)

def main():
    print("""
      INSTRUCTIONS:This is a number guessing game.
      Guess a randomly generated number between 1 and 20.
      You have a maximum of 8 guesses to find the correct number.
    """)

    # Generate a random number between 1 and 20 using random.randint()
    secret_number = generate_random_number(1,20)

    # Set a maximum guess limit of 8 guesses
    MAX_GUESSES = 8
    guess_count = 0
    guess = False
    while guess_count < MAX_GUESSES:
        #Inside the loop, prompt the user to enter a guess using input() — remember to cast it to an integer
        guess = int(input("Please enter your guess: "))
        guess_count += 1
        guesses_left = MAX_GUESSES - guess_count
        if(guess < secret_number):
            print("Too low!") 
            print(f"You have {guesses_left} guesses left.")
        elif(guess > secret_number):
            print("Too high")
            print(f"You have {guesses_left} guesses left.")
        else:
            print("Correct")
            guess = True
            break
     #if the user never guessed correctly   
    if(guess == False):
        print(f"No more guesses! The correct number was {secret_number}.")

main()