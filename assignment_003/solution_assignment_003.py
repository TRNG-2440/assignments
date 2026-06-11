def TasksPrinter(lst):
    for i, t in enumerate(lst):
        print(f"{i + 1}: {t}")

def ToDoListManager():
    pending_tasks = []          # not completed
    completed_tasks = []        # completed

    while True:
        print("--------------------------------------")
        print("                 MENU                 ")
        print("--------------------------------------")
        print(f" PENDING TASKS: {len(pending_tasks)}, COMPLETED TASKS: {len(completed_tasks)}")
        print("--------------------------------------")
        print("1. Add a task")
        print("2. View all tasks")
        print("3. Mark a task as complete")
        print("4. Remove a completed task")
        print("5. Remove all completed tasks")
        print("0. Exit")
        inp = input("Choose an option to continue: ")

        match inp:
            case "1" | "1. Add a task":
                print("--------------------------------------")
                inp1 = input("Add a task description: ")
                if not inp1: print("Empty description. Going back to menu.")
                else:
                    pending_tasks.append(inp1)
                    print("Task successfully added to pending:", inp1)
            case "2" | "2. View all tasks":
                print("--------------------------------------")
                print("PENDING:")
                if len(pending_tasks) == 0: print("Pending tasks are empty.")
                else: TasksPrinter(pending_tasks)
                print("\nCOMPLETED:")
                if len(completed_tasks) == 0: print("Completed tasks are empty.")
                else: TasksPrinter(completed_tasks)
            case "3" | "3. Mark a task as complete":
                print("--------------------------------------")
                if len(pending_tasks) == 0: print("Pending tasks are empty.")
                else: 
                    print("PENDING:")
                    TasksPrinter(pending_tasks)
                    inp3 = input("Enter number of task you want to complete: ")
                    
                    # error handling
                    if not inp3.isdigit():
                        print("Invalid input. Going back to menu.")
                    else:
                        inp3 = int(inp3)
                        if inp3 < 1 or inp3 > len(pending_tasks):
                            print("Index out of bounds. Going back to menu.")
                        else:
                            task = pending_tasks.pop(inp3 - 1)
                            completed_tasks.append(task)
                            print("Task successfully moved to completed:", task)
            case "4" | "4. Remove a completed task":
                print("--------------------------------------")
                if len(completed_tasks) == 0: print("Completed tasks are empty.")
                else: 
                    print("COMPLETED:")
                    TasksPrinter(completed_tasks)
                    inp4 = input("Enter number of task you want to remove: ")
                    
                    # error handling
                    if not inp4.isdigit():
                        print("Invalid input. Going back to menu.")
                    else:
                        inp4 = int(inp4)
                        if inp4 < 1 or inp4 > len(completed_tasks):
                            print("Index out of bounds. Going back to menu.")
                        else:
                            completed_tasks.pop(inp4 - 1)
                            print("Task successfully removed from completed:", task)
            case "5" | "5. Remove all completed tasks":
                print("--------------------------------------")
                if len(completed_tasks) == 0: print("Completed tasks are empty.")
                else: 
                    print("COMPLETED:")
                    TasksPrinter(completed_tasks)
                    completed_tasks.clear()
                    print("All tasks successfully removed from completed.")
            case "0" | "0. Exit":
                print("--------------------------------------")
                print("Exiting menu.")
                print("--------------------------------------")
                break

ToDoListManager()