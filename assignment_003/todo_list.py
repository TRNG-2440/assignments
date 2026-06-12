pending_tasks = []
completed_tasks = []

while True:
    print("\n======== TODO List Manager ========")
    print("1. Add a task")
    print("2. View all tasks")
    print("3. Mark task as completed")
    print("4. Remove a completed task")
    print("5. Exit")

    choice = input("Select an option: ")

    if choice == "1":
        task = input("Enter the task: ") 
        pending_tasks.append(task)
        print("Task added successfully!: ({task})")

    elif choice == "2":
        print("\nPending Tasks: ")

        if len(pending_tasks) == 0:
            print("No pending tasks.")
        else: 
            for i in range(len(pending_tasks)):
                print(f"{i + 1}. {pending_tasks[i]}")

        print("\nCompleted Tasks")

        if len(completed_tasks) == 0:
            print("No completed tasks yet.")
        else: 
            for i in range(len(completed_tasks)):
                print(f"{i + 1}. {completed_tasks[i]}")
    
    elif choice == "3":
        if len(pending_tasks) == 0:
            print("No pending tasks to mark as completed.")
        else:
            print("\nPending tasks: ")
            for i in range(len(pending_tasks)):
                print(f"{i+1}. {pending_tasks[i]}")

            task_number = int(input("\nEnter task number to complete: "))

            if 1 <= task_number <= len(pending_tasks):
                task = pending_tasks.pop(task_number - 1)
                completed_tasks.append(task)
                print(f"'{task}'marked as completed.")
            else:
                print("Invalid task number.")

    elif choice == "4":
        if len(completed_tasks) == 0:
            print("No completed tasks to remove.")
        else:
            print("\nCompleted tasks: ")
            for i in range(len(completed_tasks)):
                print(f"{i+1}. {completed_tasks[i]}")

            task_number = int(input("\nEnter task number to remove: "))

            if 1 <= task_number <= len(completed_tasks):
                task = completed_tasks.pop(task_number - 1)
                print(f"'{task}' removed from completed tasks.")
            else:
                print("Invalid task number.")
    
    elif choice == "5": 
        print("Goodbye!")
        break 

    else: 
        print("Invalid menu option. Please try again.")