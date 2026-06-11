def task_manager():

    pending_tasks = []
    completed_tasks = []

    while True:

        print(f"════════════════════════════════════════\nTO-DO LIST MANAGER\n════════════════════════════════════════")
        print(f"1. Add a task\n2. View all tasks\n3. Mark a task as complete\n4. Remove a completed task\n5. Clear completed tasks\n0. Exit")
        print(f"════════════════════════════════════════=")

        choice = int(input("Select an option: "))

        match choice:
            case 1:
                task = input("Enter task: ").strip()

                if not task:
                    print(f"The task cannot be empty.")
                
                else:
                    pending_tasks.append(task)
                    print(f"Task successfully added!: {task}")

            case 2: 

                print(f"Pending tasks: {len(pending_tasks)}")
                print(f"Completed tasks: {len(completed_tasks)}")

                if not pending_tasks:
                    print(f"No Pending tasks.")
                else:
                    print(f"Pending tasks:")
                    for num, task in enumerate(pending_tasks, start = 1):
                        print(f"{num}. {task}")
                
                if not completed_tasks:
                    print(f"No completed tasks.")
                else:
                    print(f"Completed tasks:")
                    for num, task in enumerate(completed_tasks, start = 1):
                        print(f"{num}. {task}")
            
            case 3:
                if not pending_tasks:
                    print("Add a task first to complete it!")
                else:
                    print(f"Mark a task to complete:")
                    for num, task in enumerate(pending_tasks, start = 1):
                        print(f"{num}. {task}")

                    task_num = int(input("Select: "))



                    if task_num <= 0 or task_num > len(pending_tasks):
                        print(f"Please put a valid number (1-{len(pending_tasks)})")
                    else:
                        print(f"'{pending_tasks[task_num - 1]}' marked as completed.")
                        task = pending_tasks[task_num - 1]
                        completed_tasks.append(task)
                        pending_tasks.remove(task)

            case 4:
                if not completed_tasks:
                    print(f"You have no completed tasks.")
                
                else:
                    print(f"Completed tasks:")
                    for num, task in enumerate(completed_tasks, start = 1):
                        print(f"{num}. {task}")

                    task_num = int(input("Enter the number of the task you would like to remove: "))

                    if task_num <= 0 or task_num > len(completed_tasks):
                        print(f"Please put a valid number.")
                    
                    else:
                        print(f"'{completed_tasks[task_num - 1]}' removed from task list.")

                        task = completed_tasks[task_num - 1]
                        completed_tasks.remove(task)

            case 5:
                if not completed_tasks:
                    print(f"You have no completed tasks.")

                else:
                    completed_tasks.clear()
                    print(f"Completed tasks cleared!")

            case 0:
                print(f"Goodbye!")
                break

            case _:
                print(f"Please put a valid choice number (0-5)")


task_manager()







