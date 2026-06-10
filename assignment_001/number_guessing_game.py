import random

def get_random_num():
    return random.randint(1, 20)

def main():
    print("Welcome to the Number Guessing Game!")
    attempts = 8

    random_num = get_random_num()   # get a random number    

    print ("Okay I'm ready! Try to guess my number between 1-20.")
    
    tries = 0

    while (tries < attempts):
        tries += 1
        guess = int(input("\nEnter your guess: "))

        if guess == random_num:
            print("\nCongratulations! You've guessed the number \nThanks for Playting...")
            break
        elif guess < random_num:
            print("\nToo low! Try again.")
        else:
            print("\nToo high! Try again.")
        
        print ("You have " + str(attempts - tries) + " tries left.")
        
        if tries == attempts:
            print("You're at your guess limit! Thanks for playing the number was: " + str(random_num))



"""Uncomment the code below if you would like to play with different difficulty levels :)"""
# def main():
#     print("Welcome to the Number Guessing Game!")
#     userInput = input("Choose your difficulty: \n1. Easy \n2. Medium \n3. Hard \n\n")

#     while(userInput != "1" and userInput != "2" and userInput != "3"):
#         userInput = userInput("Please enter a valid difficulty level (1, 2, or 3): ")
        
#     if userInput == "1":
#         attempts = 10
#     elif userInput == "2":
#         attempts = 5
#     elif userInput == "3":
#         attempts = 3
    
#     random_num = get_random_num()
#     print("Thinking of a number...")

#     print ("Okay I'm ready! Try to guess my number between 1-20.")
    
#     tries = 0

#     while (tries < attempts):
#         tries += 1
#         guess = int(input("\nEnter your guess: "))

#         if guess == random_num:
#             print("\nCongratulations! You've guessed the number \nThanks for Playting...")
#             break
#         elif guess < random_num:
#             print("\nToo low! Try again.")
#         else:
#             print("\nToo high! Try again.")
        
#         print ("You have " + str(attempts - tries) + " tries left.")
#         if tries == attempts:
#             print("You're at your try limit! Thanks for playing the number was: " + str(random_num))


if __name__ == "__main__":
    main()