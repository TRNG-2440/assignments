# Activity 2 — Console Menu Selection System

## Objective:

Practice nested while loops, match statements, if-else, break, continue, and formatted output using only what you have learned so far

## Instructions:

* Create a while True outer loop for the top-level category menu
* Inside the outer loop, use print() statements to display a menu with 3 categories and an option to exit the program. For example:
1. Electronics
2. Clothing
3. Food
4. Exit
* Use input() to collect the user's category selection
* Use a match statement or if-elif-else to handle the category selection:

  * A valid category selection should enter an inner while True loop for the item menu
  * 0 / exit should break out of the outer loop and end the program
  * Any invalid input should continue and reprint the category menu

Inside each inner while True loop, use print() statements to display at least 2 items for that category, plus an option to go back. For example:

1. Laptop
2. Phone
3. Back
* Use input() to collect the user's item selection
* Use a match statement or if-elif-else to handle the item selection:

  * A valid item selection should print the item's details using print() and f-strings — each item should display a name, price, quantity, and inventory hardcoded as variables or directly in the print statement
  * 0 / back should break out of the inner loop and return to the category menu
  * Any invalid input should continue and reprint the item menu

Requirements checklist:

* Outer while True loop for the category menu
* Inner while True loop for each category's item menu
* match statements or if-elif-else for handling menu selections
* break to exit or navigate back
* continue to handle invalid inputs
* At least 3 categories and 2 items per category
* Each item should display name, price, quantity, and inventory when selected
* Output should be neatly formatted using f-strings

