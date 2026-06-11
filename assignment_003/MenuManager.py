# Mark White
# 06/10/2026
# To-Do List Manager

# This program allows you to add, view, mark completed, and remove tasks from a to-do list.
# If no tasks are in the list, it will display a message indicating that there are no tasks or invalid number.
# Upon marking a task as completed, the program will move the task from the pending list to the completed list and display a confirmation message.
# The program will continue to run until the user chooses to exit by entering "5".


pending_task = []
completed_task = []

menu_options = ("""
      1. Add a task
      2. View tasks
      3. Mark a task as completed
      4. Remove a task
      5. Exit
      """)
        

def add_task():
    task = input("Enter the task: ")
    pending_task.append(task)


def view_tasks():
    if not pending_task:
        print("\nNo pending tasks in the list.")
    else:
        print("\nPending tasks:")
        for i, task in enumerate(pending_task, start=1):
            print(f"{i}. {task}")
        print("=" * 15)

    if not completed_task:
        print("\nNo completed tasks in the list.")
    else:
        print("\nCompleted tasks:")
        for i, task in enumerate(completed_task, start=1):
            print(f"{i}. {task}")
        print("=" * 15)


def mark_completed():
    if not pending_task:
        print("\nNo pending tasks to mark as completed.")
        return

    print("\nPending tasks:")
    for i, task in enumerate(pending_task, start=1):
        print(f"{i}. {task}")
    print("=" * 15)
    try:
        index = int(input("\nEnter the task number to mark as completed: ")) - 1
        if 0 <= index < len(pending_task):
            task = pending_task.pop(index)
            completed_task.append(task)
            print(f"\nTask '{task}' marked as completed.")
        else:
            print("\nInvalid task number.")
    except ValueError:
        print("\nPlease enter a valid number.")


def remove_task():
    if not pending_task and not completed_task:
        print("\nNo tasks to remove.")
        return

    print("\nPending tasks:")
    for i, task in enumerate(pending_task, start=1):
        print(f"{i}. {task}")   
    print("=" * 15)

    print("\nCompleted tasks:")
    for i, task in enumerate(completed_task, start=1):
        print(f"{i+len(pending_task)}. {task}")
    print("=" * 15)

    try:
        index = int(input("\nEnter the task number to remove: ")) - 1
        if 0 <= index < len(pending_task):
            removed = pending_task.pop(index)
            print(f"\nRemoved pending task '{removed}'.")
        elif len(pending_task) <= index < len(pending_task) + len(completed_task):
            removed = completed_task.pop(index - len(pending_task))
            print(f"\nRemoved completed task '{removed}'.")
        else:
            print("\nInvalid task number.")
    except ValueError:
        print("\nPlease enter a valid number.")

def MenuManager():

    print("Welcome to the To-Do List Manager")
    
    while True:
        print(menu_options)
        choice = input("Enter your choice: ")
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_completed()
        elif choice == "4":
            remove_task()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
  MenuManager()