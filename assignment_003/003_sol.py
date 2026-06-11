#Code solution for Assignment 3
#Alex Tran

#To-Do Task Manager

pending_tasks = []
completed_tasks = []


while True:
    print("\n=== TO-DO TASK MANAGER ===")
    print("1. Add a task")
    print("2. View all tasks")
    print("3. Mark a task as complete")
    print("4. Remove a completed task")
    print("5. Exit")


    choice = input("Select your choice from the menu: ")
    
    #Control flow for choice handling
    if choice == "1":
        task = input("Enter a task description: ")
        pending_tasks.append(task)
        print(f"Task '{task}' successfully added to the queue.")
    
    #Handling for all other tasks:

    #Displaying pending and completed tasks
    elif choice == "2":
        print("\n=== PENDING TASKS ===")
        if len(pending_tasks) == 0:
            print("No pending tasks.")
        else: 
            for i  in range(len(pending_tasks)):
                print(f"{i+1}. {pending_tasks[i]}")
        
        print("\n=== COMPLETED TASKS ===")
        if len(completed_tasks) == 0:
            print("No completed tasks.")
        else:
            for i  in range(len(completed_tasks)):
                print(f"{i+1}. {completed_tasks[i]}")

    
    #If the user wants to mark this task as completed
    
    elif choice == "3":
        if len(pending_tasks) == 0:
            print("There are no pending tasks to complete.")
        else:
            print("\n=== PENDING TASKS ===")
            for i  in range(len(pending_tasks)):
                print(f"{i+1}. {pending_tasks[i]}")
            
            #Prompt user to enter the task to complete w/ exception handling 
            try:
                which_task = int(input("Enter the number of the task you want to complete: "))
                if 1 <= which_task <= len(pending_tasks):
                    completed_task = pending_tasks[which_task -1]
                    completed_tasks.append(completed_task)
                    pending_tasks.remove(completed_task)
                    print(f"Task '{completed_task}' marked as complete.")
                
                else:
                    print("Invalid task number.")

            
            except ValueError:
                print("Enter a valid number.")

    #If the user wants to remove completed tasks
    elif choice == "4":
        if len(completed_tasks) == 0:
            print("There are no completed tasks listed for removal.")
        else:
            print("\n=== COMPLETED TASKS ===")
            for i  in range(len(completed_tasks)):
                print(f"{i+1}. {completed_tasks[i]}")
            
            try:
                task_num = int(input("Enter the number of the completed task you want to remove: "))
                if 1 <= task_num <= len(completed_tasks):
                    removed_task = completed_tasks[task_num -1]
                    completed_tasks.remove(removed_task)
                    print(f"Task '{removed_task}' removed from the list of complted tasks.")
                
                else:
                    print("Invalid task number.")
            
            except ValueError:
                print("Enter a valid number.")


    elif choice == "5":
        print("Exiting process. Goodbye!")
        break

    else:
        print("Invalid choice. Please choose an option listed from the menu.")







