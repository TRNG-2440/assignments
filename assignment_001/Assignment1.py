import random
# Generate a random number between 1 and 20
guess_this = random.randint(1,20)
# Set a max of 8 guesses
max_guesses = 8
# Track the number of guesses using a counter variable
guess_count = 0
# Create a while loop that runs as long as the guess count is under the limit
while (guess_count < max_guesses):
    # Inside the loop, prompt the user to enter a guess using input() — remember to cast it to an integer
    user_input = int(input("Guess a number between 1 and 20\n"))
    # Increment the guess counter on each iteration
    guess_count += 1
    # Use if-elif-else to respond with:
    # "Too high!" if the guess is above the number
    if user_input > guess_this:
        print("Too high!")
    # "Too low!" if the guess is below the number
    elif user_input < guess_this:
        print("Too low!")
    # "Correct!" followed by a break if the guess matches
    else:
        print("Correct!")
        break
    # After the "Too high" / "Too low" response, print how many guesses the user has remaining
    print(f"You have {max_guesses-guess_count} remaining guesses!")

# After the loop ends, if the user never guessed correctly, print "No more guesses!" and reveal the number
if guess_count == max_guesses:
    print(f"No more guesses! The number is {guess_this}")