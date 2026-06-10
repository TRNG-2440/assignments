# lists
pending_tasks = []
completed_tasks = []

while True:
    print ("1. Add a task")
    print ("2. View all tasks")
    print ("3. Mark a task as complete")
    print ("4. Remove a completed task")
    print ("5. Exit\n")

    choice = input("Pick an option: ")

    match choice:
        case "1":
            new_task = input("Add your new task: ")
            pending_tasks.append(new_task)
            print("Task added")

        case "2":
            if (pending_tasks):
                print ("Your pending Tasks: ")
                for x in range(len(pending_tasks)):
                    print(f"{x + 1}. {pending_tasks[x]}")
            else:
                print("No pending tasks")
            
            if (completed_tasks):
                print ("Your completed Tasks: ")
                for x in range(len(completed_tasks)):
                    print(f"{x + 1}. {completed_tasks[x]}")
                print("")
            else:
                print("No completed tasks\n")
            
        case "3":
            if (pending_tasks):
                print ("Your pending tasks: ")
                for x in range (len(pending_tasks)):
                    print(f"{x + 1}. {pending_tasks[x]}")
                print("0. Back")
            else:
                print("No pending tasks\n")
                continue

            while True: 
                task_completed = int(input("Choose the number of the task you want to complete: "))
                if task_completed == 0:
                    break
                if task_completed > 0 and task_completed <= len(pending_tasks):
                    completed_tasks.append(pending_tasks[task_completed - 1])
                    pending_tasks.remove(pending_tasks[task_completed - 1])
                    print ("Task completed!")
                    break
                else:
                    print ("Number invalid\n")

            
        case "4":
            if (completed_tasks):
                print ("Your completed tasks: ")
                for x in range (len(completed_tasks)):
                    print(str(x + 1) + ". " + completed_tasks[x])
                print("0. Back")
            else:
                print("No completed tasks\n")
                continue

            while True: 
                task = int(input("Choose the number of the task you want to remove: "))
                if task == 0:
                    break
                if task > 0 and task <= len(completed_tasks):
                    completed_tasks.remove(completed_tasks[task - 1])
                    print ("Task removed")
                    break
                else:
                    print ("Number invalid\n")

        case "5":
            print ("Goodbye!")
            break