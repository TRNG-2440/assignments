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
def addATask():
    task = input("\nEnter Task: ")
    if task:
        completed_tasks.append(task)
        print(f"\nTask successfully added!: {task}\n")
    else:
        print("\nCannot insert empty task!")

def viewAllTasks():
    print("\nPending tasks:")
    if pending_tasks:
        for task in pending_tasks:
            printOptions(pending_tasks)
    else:
        print("  No pending tasks yet.\n")

    print("\nCompleted Tasks: ")
    if completed_tasks:
        for task in completed_tasks:
            printOptions(completed_tasks)
    else:
        print("  No completed tasks yet.\n")

def markTaskComplete():
    print("\nPendingTasks:")
    if not pending_tasks: # Check if the pending tasks list is empty or not
        print("  No pending tasks yet.\n")
        return
    
    
    printOptions(pending_tasks)
    user_input = input("Enter task number to complete: ")-1
    
    if not user_input.isdigit(): # Validate user input is number
        print("Invalid Input!\n")
        return
    user_input = int(user_input) # Convert user input to number
    if not (user_input >= 0) or not (user_input<completed_tasks.count): #validate user input is within range
        print("Invalid Input!\n")
        return

    # All checks successful, complete and confirm to user
    completed_tasks.append = pending_tasks[user_input]
    task_name = pending_tasks[user_input]
    pending_tasks.remove[user_input]
    print(f"'{task_name}' marked as complete.\n")


def removeCompletedTask():
    print("\nCompleted Tasks: ")
    if not completed_tasks: # Check there are tasks in list
        print("No completed tasks yet.\n")
        return
    
    printOptions(completed_tasks)
    user_input = input("Enter task number to remove: ")

    if not user_input.isdigit(): # Validate user input is number
        print("Invalid Input!\n")
        return
    user_input = int(user_input) # Convert user input to number
    if not (user_input >= 0) or not (user_input<completed_tasks.count): #validate user input is within range
        print("Invalid Input!\n") 
        return
    
    # All checks successful, complete and confirm to user
    task_name = completed_tasks[user_input]
    completed_tasks.remove[user_input]
    print(f"'{task_name}' removed from task list.\n")


main_menu = ["Add a task", "View all tasks", "Mark a task as complete", "Remove a completed task", "Exit"]

# Main program starts here
print(  "--------------------------------------------\n" \
        "            To-Do List Manager             \n" \
        "--------------------------------------------")
printOptions(main_menu)
# While true loop to activate menu
while True:
    user_input = input( "--------------------------------------------" \
                        " Select an option! Just enter the number: ")
