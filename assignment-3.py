def to_do():
    pending_tasks = []
    completed_tasks = []

    while True:
        print("-" * 30)
        print("TO-DO LIST MANAGER")
        print("-" * 30)
        print("1. Add a task")
        print("2. View all tasks")
        print("3. Mark a task as complete")
        print("4. Remove a completed task")
        print("5. Exit")
        print("Select an option: ")
        option = input()


        if option == '5' or option == '0':
            print("Goodbye!")
            break

        elif option == '1':
            print("Enter a task:", end=' ')
            task = input()
            pending_tasks.append(task)
            print(f'Task successfully added!: ("{task}")')

        elif option == '2':
            if not pending_tasks:
                print("No pending tasks.")
            if not completed_tasks:
                print("No completed tasks.")

            for i, n  in enumerate(pending_tasks):
                print(f'Pending: {i+1}. {n}')
            for i, n in enumerate(completed_tasks):
                print(f'Completed: {i+1}. {n}')

        elif option == '3':
            for i, n  in enumerate(pending_tasks):
                print(f'Pending: {i+1}. {n}')
            print("Enter task number to complete:", end=' ')
            try:
                task_index = int(input())
                if 0 < task_index <= len(pending_tasks):
                    completed = pending_tasks.pop(task_index - 1)
                    completed_tasks.append(completed)
                    print(f'Successfully marked as complete: ("{completed}")')
            except ValueError:
                print("Please enter a valid task number.")

        elif option == '4':
            for i, n  in enumerate(completed_tasks):
                print(f'Completed: {i+1}. {n}')
            print("Enter task number to remove:", end=' ')
            try:
                task_index = int(input())
                if 0 < task_index <= len(completed_tasks):
                    removed = completed_tasks.pop(task_index - 1)
                    print(f'Successfully removed: ("{removed}")')
            except ValueError:
                print("Please enter a valid task number.")





to_do()