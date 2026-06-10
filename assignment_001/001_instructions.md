# Python Coding Activity 1 — Number Guessing Game

Objective: Practice while loops, if-else statements, input(), and random
Instructions:

- Import the random module
- Generate a random number between 1 and 20 using random.randint()
- Set a maximum guess limit of 8 guesses
- Track the number of guesses using a counter variable
- Create a while loop that runs as long as the guess count is under the limit
- Inside the loop, prompt the user to enter a guess using input() — remember to cast it to an integer
- Increment the guess counter on each iteration
- Use if-elif-else to respond with:
  - "Too high!" if the guess is above the number
  - "Too low!" if the guess is below the number
  - "Correct!" followed by a break if the guess matches
- After the "Too high" / "Too low" response, print how many guesses the user has remaining
- After the loop ends, if the user never guessed correctly, print "No more guesses!" and reveal the number

Requirements checklist:

- random.randint() to generate the number
- while loop with a guess counter
- int(input()) to collect and cast user input
- if-elif-else for the high / low / correct logic
- break to exit the loop on a correct guess
- A message revealing the number if all guesses are used
