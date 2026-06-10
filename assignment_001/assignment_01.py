import random

num =random.randint(1,20) #Generates a random number between 1 and 20 each time
max_guesses = 8 
number_of_guesses = 0

while number_of_guesses < max_guesses:
     guess = int(input("Guess a number between 1 and 20: "))
     number_of_guesses += 1 #Increments the number of guesses after each attempt
     if guess < num:
         print("Too low!")
         print(f"You have {max_guesses - number_of_guesses} guesses left.") #Gives feedback on how many guesses are left after each attempt
     elif guess > num:
         print("Too high!")
         print(f"You have {max_guesses - number_of_guesses} guesses left.")
     else:
         print("Congratulations! You've guessed the number in", number_of_guesses, "guesses!")
         break
else:
    print("Sorry, you've used all your guesses. The number was", num)