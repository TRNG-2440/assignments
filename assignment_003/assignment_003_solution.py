pending_tasks = []
completed_tasks = []  # moved here so lists persist across the loop
while True:
    print("════════════════════════════════════════")
    print("         TO-DO LIST MANAGER")
    print("════════════════════════════════════════")
    print("1. Add a task")
    print("2. View all tasks")
    print("3. Mark a task as complete")
    print("4. Remove a completed task")
    print("0. Exit")  # changed from 5 to 0 to match spec
    print("════════════════════════════════════════")
    choice = input("Select an option: ")
    match choice:
        case "1":
            task = input("Enter a new task: ")
            if task:  # prevents adding empty tasks (stretch goal)
                pending_tasks.append(task)
                print(f"Task added successfully!: ({task})")
            else:
                print("Task cannot be empty.")
        case "2":
            print(f"\nPending tasks: {len(pending_tasks)} | Completed: {len(completed_tasks)}")
            print("\nPending Tasks:")
            if pending_tasks:
                for i, task in enumerate(pending_tasks, 1):  # numbered list
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
                    task = pending_tasks[num - 1]  # convert 1-based to 0-based index
                    pending_tasks.remove(task)
                    completed_tasks.append(task)
                    print(f"'{task}' marked as complete.")
                except (ValueError, IndexError):
                    print("Invalid number. Please try again.")
        case "4":
            if not completed_tasks:
                print("No completed tasks to remove.")
            else:
                print("\nCompleted Tasks:")
                for i, task in enumerate(completed_tasks, 1):
                    print(f"  {i}. {task}")
                try:
                    num = int(input("Enter task number to remove: "))
                    task = completed_tasks[num - 1]
                    completed_tasks.remove(task)
                    print(f"'{task}' removed from task list.")
                except (ValueError, IndexError):
                    print("Invalid number. Please try again.")
        case "0":  # changed from "5" to "0"
            print("Goodbye!")
            break
        case _:
            print("Invalid option. Please try again.")