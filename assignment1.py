import random


number_to_guess = random.randint(1, 20)



def guessing_game():
    max_guesses = 8
    count = 0
    print("Welcome to the guesssing game! Guess a number between 1 and 20: ")
    guess = int(input())
    
    while count < max_guesses:
         

        if guess > number_to_guess:
            print("Too high!")
            count += 1

        # track guesses, if 0 return answer 
            print("Guesses remaining " + str(max_guesses - count))
            if (max_guesses - count) == 0:
                print("No more guesses! The number was: " + str(number_to_guess))
                break
            print("Guess again!: ")
            guess = int(input())

    # check for low number, includes the 0 guesses remaining case as well

        elif guess < number_to_guess:
            print("Too Low!")
            count += 1
            print("Guesses remaining " + str(max_guesses - count))
            if (max_guesses - count) == 0:
                print("No more guesses! The number was: " + str(number_to_guess))
                break
            print("Guess again!: ")
            guess = int(input())


        elif(guess == number_to_guess):
            print("Correct!")
            break

        
            
        

guessing_game()