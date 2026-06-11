"""TODO:
    - loop menu for user to choose
    
    1. Add Task
        - add task description
        - add task to pending
        - comfirm adding to list

        
    2. View Tasks
        - display pending NUMBERED (index + 1)
        - display copleted NUMBERED (index + 1)
        - if any empty, print message


    3. Mark task as complete
        - display pending tasks first
        - ask user to enter hte number of the task they want to delete
        - move that task to completed
        - print a confirm adding 
        - throw an error if user enters invalid number


    4. Removed a completed task
        - display completed tasks NUMBERED
        - ask for which task to remove
        - remove the task
        - print confirm message
        - throw error if user enters invalid number


    5. Exit
        - print goodbye and exit
    

    IF ANY INPUT INVALID, HANDLE WITH GRACE

    - 2 lists
        - pending lists --> not completed yet
        - completed --> completed tasks
"""


def add_task(pending):
    """Prompt for a task description and add it to the pending list."""
    while True:
        task_description = input("What's the description of your task?  ").strip()
        
        if not task_description:
            print("Task can't be empty, try again!")
        elif task_description in pending:
            print("Sorry! This task is already in your to-do!")
        else:
            break
    
    pending.append(task_description)
    
    print("\nTask added! Your pending list:")
    # for i in range(len(pending)):
    #     print(f" {i+1}. {pending[i]}")
    print("\nTask added to your pending list!")



def view_task(pending, completed):
    """
    2. View Tasks
        - display pending NUMBERED (index + 1)
        - display copleted NUMBERED (index + 1)
        - if any empty, print message
    """
    if pending:
        print("\nHere are the pending tasks:")
        for i in range(len(pending)):
            print(f" {i+1}. {pending[i]}")
    else:
        print("No pending tasks!")

    if completed:
        print("\nHere are the completed tasks:")
        for i in range(len(completed)):
            print(f" {i+1}. {completed[i]}")
    else:
        print("No completed tasks!")
    

def complete_task(pending, completed):
    """
    3. Mark task as complete
        - display pending tasks first
        - ask user to enter hte number of the task they want to delete
        - move that task to completed
        - print a confirm adding 
        - throw an error if user enters invalid number
    """

    if not pending:
        print("\nThere are no pending tasks. Cannot mark anyhting for completion!\n")
        return
    
    
    print("Here is your current pending task list:")
    for i, task in enumerate(pending, start=1):
        print(f" {i}. {task}")
    print()

    while True:
        try:
            user_complete = int(input("Enter the number of the task to mark completed: ")) - 1
        except ValueError as e:
            print(f"Your entered {e}, Please enter a valid number!")
            continue

        if (0 <= user_complete < len(pending)):
            break

        print(f"Please choose a number from 1 to {len(pending)}")

    task = pending.pop(user_complete)
    completed.append(task)

    print(f"The '{task}' has been marked as completed!")




def remove_completed(completed):
    """
    4. Removed a completed task
        - display completed tasks NUMBERED
        - ask for which task to remove
        - remove the task
        - print confirm message
        - throw error if user enters invalid number
    """
    if not completed:
        print("\nThere are no pending tasks. Cannot mark anyhting for completion!\n")
        return
    
    print("Here is your current pending task list:")
    for i, task in enumerate(completed, start=1):
        print(f" {i}. {task}")
    print()

    while True:
        try:
            remove_completed = int(input("Enter the number of the task you want to delete: ")) - 1
        except ValueError as e:
            print(f"Your entered {e}, Please enter a valid number!")
            continue

        if (0 <= remove_completed < len(completed)):
            break
        
        print(f"Please choose a number from 1 to {len(completed)}")
    
    task = completed.pop(remove_completed)
    print(f"The '{task}' task has been deleted.")



def main():

    pending = []
    completed = []

    while True:
        print ("\nWelcome to your list manager!!")
        print ("Here are the options: \n1. Add a task \n2. View all tasks \n3. Mark a task as complete \n4. Remove a completed task \n5. Exit")
        
        user_option = input("Which action would you like to do?  ")

        if user_option == "1" or user_option.upper() == "ADD A TASK":
            add_task(pending)
        elif user_option == "2" or user_option.upper() == "VIEW ALL TASKS":
            view_task(pending, completed)
        elif user_option == "3" or user_option.upper() == "MARK A TASK AS COMPLETE":
            complete_task(pending, completed)
        elif user_option == "4" or user_option.upper() == "REMOVE A COMPLETED TASK":
            remove_completed(completed)
        elif user_option == "5" or user_option == "0":
            break
        else:
            print("Invalid option! Please choose 1-5.\n")



if __name__ == "__main__":
    main()