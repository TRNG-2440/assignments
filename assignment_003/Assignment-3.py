pending_tasks = []
completed_tasks = []

print('''
════════════════════════════════════════
TO-DO LIST MANAGER
════════════════════════════════════════
1. Add a task
2. View all tasks
3. Mark a task as complete
4. Remove a completed task
0. Exit
''')


while True:
    choose = input('''════════════════════════════════════════
    Select an Option: ''')

    match choose:
        case "1": 
            task = input("Enter Task: ")
            if task:
                print(f"Task successfuly added! {task}")
                pending_tasks.append(task)
            else:
                print("Please give a valid input!")
        case "2":
            if not pending_tasks:
                print("No pending tasks")
    
            else:
                print("Pending Tasks:")
                for i, p in enumerate(pending_tasks):
                    print(f"{i + 1}. {p}")
                        
            if not completed_tasks:
                print("\nNo completed tasks")
            else:
                print("\nCompleted Tasks:")
                for i, c in enumerate(completed_tasks):
                    print(f"{i + 1}. {c}")
                
        case "3":
            if not pending_tasks:
                print("No pending tasks")
                
            else:
                print("Pending Tasks:")
                for i, p in enumerate(pending_tasks):
                    print(f"{i + 1}. {p}")

            option = input("Enter task number to complete: ")
            try:
                option = int(option)
                temp = pending_tasks.pop(option - 1)
                completed_tasks.append(temp)
            except:
                print("Invalid task entry entered")
        case "4":
            print("\nCompleted Tasks:")
            for i, c in enumerate(completed_tasks):
                print(f"{i + 1}. {c}")
            choice = input("Enter task number to remove: ")
            choice = int(choice)
            try:
                completed_tasks.pop(choice - 1)
            except:
                print("Invalid task entry entered")
        case "0":
            print("Bye!")
            break
        case _: print("Please select a valid input!")