taskMenu = True

pending_tasks = []
completed_tasks = []

print("════════════════════════════════════════")
print("         TO-DO LIST MANAGER             ")
print("════════════════════════════════════════")
print("1. Add a Task")
print("2. View all tasks")
print("3. Mark a task as complete")
print("4. Remove a completed task")
print("0. Exit")
print("════════════════════════════════════════")
while taskMenu:
    choice = int(input("Select an option: "))
    print()

    if choice == 1:
        NewTask = input("Enter task: ")
        pending_tasks.append(NewTask)
        print()
        print(f"Task successfully added!: {NewTask}")
        print()
        print("════════════════════════════════════════")

    elif choice == 2:
        print("Pending Tasks:")
        if len(pending_tasks) > 0:
            for task in pending_tasks:
                index = pending_tasks.index(task) + 1
                print(f"{index}. {task}")

        else:
                print("No pending tasks.")    

        print()

        print("Completed Tasks:")
        if len(completed_tasks) > 0:
             for task in completed_tasks:
                 index = completed_tasks.index(task) + 1
                 print(f"{index}. {task}")

        else:
            print("No completed tasks.")
        print()
        print("════════════════════════════════════════")

    elif choice == 3:
        pending_tasks_menu = True

        while pending_tasks_menu:
            print("Pending Tasks:")
            if len(pending_tasks) > 0:
                for task in pending_tasks:
                    index = pending_tasks.index(task) + 1
                    print(f"{index}. {task}")

                task_to_complete = int(input("Enter task number to complete: "))
                if task_to_complete < 1 or task_to_complete > len(pending_tasks):
                    print("Invalid task number.")
                    break

                print(f"'{pending_tasks[task_to_complete - 1]}' marked as complete.")
                completed_tasks.append(pending_tasks[task_to_complete - 1])
                pending_tasks.remove(pending_tasks[task_to_complete - 1])
                break

            else:
                print("No pending tasks.")
                break

        print()
        print("════════════════════════════════════════")

    elif choice == 4:
        print("Completed Tasks:")

        if len(completed_tasks) > 0:
             for task in completed_tasks:
                 index = completed_tasks.index(task) + 1
                 print(f"{index}. {task}")

        else:
            print("No completed tasks.")
            break

        print()

        task_to_remove = int(input("Enter task number to remove: "))

        if task_to_remove < 1 or task_to_remove > len(completed_tasks):
            print("Invalid task number.")
            print()
            print("════════════════════════════════════════")
            continue

        print(f"'{completed_tasks[task_to_remove - 1]}' removed from task list.")
        completed_tasks.remove(completed_tasks[task_to_remove - 1])

        print()
        print("════════════════════════════════════════")

    elif choice == 0:
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")
        print()
        print("════════════════════════════════════════")