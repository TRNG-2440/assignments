pending_tasks = []
completed_tasks = []
user_input = ""

# Modified function from last assignment, designed to work for this one
def printOptions(options):
    output = ""
    current_option = 1
    for option in options:
        output += f"{str(current_option)}. {option}\n"
        current_option+= 1
    print(output)

# Other functions to facilitate the logic
# Option 1
def addATask():
    task = input("\nEnter Task: ")
    if task:
        pending_tasks.append(task)
        print(f"\nTask successfully added!: {task}\n")
    else:
        print("\nCannot insert empty task!")

# Option 2
def viewAllTasks():
    print("\nPending tasks:")
    if pending_tasks:
        printOptions(pending_tasks)
    else:
        print("  No pending tasks yet.\n")

    print("Completed Tasks: ")
    if completed_tasks:
        printOptions(completed_tasks)
    else:
        print("  No completed tasks yet.\n")

# Option 3
def markTaskComplete():
    print("\nPending Tasks:")
    if not pending_tasks: # Check if the pending tasks list is empty or not
        print("  No pending tasks yet.\n")
        return
    
    printOptions(pending_tasks)
    user_input = input("Enter task number to complete: ")
    
    if not user_input.isdigit(): # Validate user input is number
        print("Invalid Input! You may only enter numbers\n")
        return
    user_input = int(user_input)-1 # Convert user input to index
    if user_input < 0 or user_input>=len(pending_tasks): #validate user input is within range
        print(f"Invalid Input! This number does not correspond to any tasks\n")
        return

    # All checks successful, complete and confirm to user
    completed_tasks.append(pending_tasks[user_input])
    task_name = pending_tasks[user_input]
    pending_tasks.pop(user_input)
    print(f"'{task_name}' marked as complete.\n")

# Option 4
def removeCompletedTask():
    print("\nCompleted Tasks: ")
    if not completed_tasks: # Check there are tasks in list
        print("No completed tasks yet.\n")
        return
    
    printOptions(completed_tasks)
    user_input = input("Enter task number to remove: ")

    if not user_input.isdigit(): # Validate user input is number
        print("Invalid Input! You may only enter numbers\n")
        return
    user_input = int(user_input)-1 # Convert user input to index
    if user_input < 0 or  user_input>=len(completed_tasks): #validate user input is within range
        print("Invalid Input! This number does not correspond to any tasks\n") 
        return
    
    # All checks successful, complete and confirm to user
    task_name = completed_tasks[user_input]
    completed_tasks.pop(user_input)
    print(f"'{task_name}' removed from task list.\n")

# Option 5
def clearAllCompleted():
    completed_tasks.clear()
    print("\nThe completed task list is clear!\n")


main_menu = ["Add a task", "View all tasks", "Mark a task as complete", "Remove a completed task", "Exit"]

# Main program starts here
print(  "--------------------------------------------\n" \
        "            To-Do List Manager             \n" \
        "--------------------------------------------")
printOptions(main_menu)
# While true loop to activate menu
while True:
    user_input = input( "--------------------------------------------\n" \
                       f" Pending Tasks {len(pending_tasks)}         Completed Tasks {len(completed_tasks)}    \n" \
                        " Select an option! Just enter the number: ")
    
    if user_input == "1":
        addATask()
    elif user_input == "2":
        viewAllTasks()
    elif user_input == "3":
        markTaskComplete()
    elif user_input == "4":
        removeCompletedTask()
    elif user_input == "5":
        clearAllCompleted()
    elif user_input == "6":
        break
    else:
        print("Invalid Input!\n")
