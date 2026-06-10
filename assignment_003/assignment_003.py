# lists for pending and completed tasks
pending_tasks = []
completed_tasks = []

# main loop for to-do manager
while True:
    # options
    print("════════════════════════════════════════")
    print("         TO-DO LIST MANAGER")
    print("════════════════════════════════════════")
    print(f"Pending tasks: {len(pending_tasks)}")
    print(f"Completed tasks: {len(completed_tasks)}")
    print("════════════════════════════════════════")
    print("1. Add a task")
    print("2. View all tasks")
    print("3. Mark a task as complete")
    print("4. Remove a completed task")
    print("5. Clear all completed tasks")
    print("0. Exit")

    choice = int(input("Select an option: "))

    match choice:
        case 1: # add task
            print("")
            while True:
                task = input("Enter a task: ")
                if not task.strip():
                    print("Cannot add an empty task. Please try again.")
                    continue
                else:
                    pending_tasks.append(task)
                    print(f"Task successfully added: {task}.")
                    print("")
                    break

        case 2: # view tasks
            print("")
            print("Pending Tasks:")
            if len(pending_tasks) == 0:
                print(" No pending tasks yet.")
            else:
                for i, task in enumerate(pending_tasks, 1):
                    print(f" {i}. {task}")
            print("")
            print("Completed Tasks:")
            if len(completed_tasks) == 0:
                print(" No completed tasks yet.")
            else:
                for i, task in enumerate(completed_tasks, 1):
                    print(f" {i}. {task}")
            print("")

        case 3: # mark task as complete
            print("")
            if len(pending_tasks) == 0:
                print("No pending tasks yet. Returning to main menu.\n")
                continue
            else:
                print("Pending Tasks:")
                for i, task in enumerate(pending_tasks, 1):
                    print(f" {i}. {task}")
            
            # loop to mark task complete
            while True:
                task_num = int(input("Enter task number to mark as complete: "))

                if task_num < 1 or task_num > len(pending_tasks):
                    print("Invalid task number. Please try again.\n")
                    continue
                else:
                    completed_tasks.append(pending_tasks.pop(task_num - 1))
                    print(f"'{completed_tasks[-1]}' marked as complete.")
                    print("")
                    break
            
            # TODO: FINISH SWAP TASK PORTION
        
        case 4: # remove completed task
            print("")
            if len(completed_tasks) == 0:
                print("No completed tasks yet. Returning to main menu.\n")
                continue
            else:
                print("Completed Tasks:")
                for i, task in enumerate(completed_tasks, 1):
                    print(f" {i}. {task}")
                    
            # loop to remove completed task
            while True:
                task_num = int(input("Enter task number to remove: "))

                if task_num < 1 or task_num > len(completed_tasks):
                    print("Invalid task number. Please try again.\n")
                    continue
                else:
                    removed_task = completed_tasks.pop(task_num - 1)
                    print(f"'{removed_task}' removed from completed tasks.")
                    print("")
                    break

        case 5: # clear completed tasks
            print("")
            if len(completed_tasks) == 0:
                print("No completed tasks to clear. Returning to main menu.")
            else: # populated list
                completed_tasks.clear()
                print("All completed tasks cleared.")
                print("")

        case 0: # exit
            print("")
            print("Goodbye!")
            break