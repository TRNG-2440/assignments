pending_tasks = []
completed_tasks = []
while True:
    print("========================================")
    print("         TO-DO LIST MANAGER")
    print("=")
    print("1. Add a task")
    print("2. View all tasks")
    print("3. Mark a task as complete")
    print("4. Remove a completed task")
    print("0. Exit")
    print("========================================")
    choice = input("Select an option: ")
    match choice:
        case "1":
            task = input("Enter a new task: ")
            if task:  # Making sure no empty tasks are added
                pending_tasks.append(task)
                print(f"Task added successfully!: ({task})")
            else:
                print("Task cannot be empty.")
        case "2":
            print(f"\nPending tasks: {len(pending_tasks)} | Completed: {len(completed_tasks)}")
            print("\nPending Tasks:")
            if pending_tasks:
                for i, task in enumerate(pending_tasks, 1):  #using enumerate to create a numbered list
                    print(f"  {i}. {task}")
            else:
                print("  No pending tasks.")
            print("\nCompleted Tasks:")
            if completed_tasks:
                for i, task in enumerate(completed_tasks, 1):
                    print(f"  {i}. {task}")
            else:
                print("  No completed tasks yet.")
        case "3":
            if not pending_tasks:
                print("No pending tasks to complete.")
            else:
                print("\nPending Tasks:")
                for i, task in enumerate(pending_tasks, 1):
                    print(f"  {i}. {task}")
                try:
                    num = int(input("Enter task number to complete: "))
                    task = pending_tasks[num - 1]
                    pending_tasks.remove(task)
                    completed_tasks.append(task)
                    print(f"'{task}' marked as complete.")
                except (ValueError, IndexError): # In case an invalid number is entered
                    print("Invalid number")
        case "4":
            if not completed_tasks:
                print("No completed tasks to remove")
            else:
                print("\nCompleted Tasks:")
                for i, task in enumerate(completed_tasks, 1):
                    print(f"  {i}. {task}")
                try:
                    num = int(input("Enter task number to remove: "))
                    task = completed_tasks[num - 1]
                    completed_tasks.remove(task)
                    print(f"'{task}' removed from task list")
                except (ValueError, IndexError):
                    print("Invalid number")
        case "0":
            print("Exit")
            break
        case _:
            print("Invalid option")