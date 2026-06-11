to_do_tasks = []
finished_tasks = []

def main_menu():
    print("\n***To-Do List Manager***\n1. Add a task\n2. View all tasks\n3. Mark a task as complete\n4. Remove a completed task\n5. Exit\n\n")

def add_task(task:str, task_list:list):
    task_list.append(task)

def remove_task(task_num:int, task_list:list):
    task_list.pop(task_num - 1)

def view_tasks(td_list:list):
    count = 1
    for t in td_list:
        print(f"{count}. {t}")
        count += 1
    count = 1
    print("\n")

def view_all_tasks():
    print("\nPending Tasks:")
    if len(to_do_tasks) == 0:
        print("You're all caught up on your tasks!")
    else:
        view_tasks(to_do_tasks)
    
    print("\n\nCompleted Tasks:")
    if len(finished_tasks) == 0:
        print("You have no completed tasks! Get going!!")
    else:
        view_tasks(finished_tasks)

def complete_task(task_num:int):
    task_done = to_do_tasks[task_num - 1]
    finished_tasks.append(task_done)
    remove_task(task_num, to_do_tasks)


while True:
    main_menu()
    user_input = input(f"Select an option:  ")

    match user_input:
        case '1':   #Add task to todo list
            new_task = str(input(f"Please enter the task you need to complete!\n"))
            add_task(new_task, to_do_tasks)
            
        case '2': #view all tasks
            view_all_tasks()
            
        case '3': #mark task as completed
            print("\nPending Tasks:")
            if len(to_do_tasks) == 0:
                print("You're all caught up on your tasks!")
            else:
                view_tasks(to_do_tasks)

                try:
                    num_task_completed = int(input(f"\nPlease enter the task number you would like marked as complete:   "))
                    if 1 <= num_task_completed <= len(to_do_tasks):
                        print(f"'{to_do_tasks[num_task_completed - 1]}' is marked as complete!")
                        complete_task(num_task_completed)
                        
                    else:
                        print("The task number entered does not exist.")
                except ValueError:
                    print("Invalid entry, please submit a valid number.")
            
        case '4': #delete completed tasks
            print("\nCompleted Tasks:")
            if len(finished_tasks) == 0:
                print("You have no tasks completed.")
            else:
                view_tasks(finished_tasks)

                try:
                    task_to_delete = int(input(f"\nPlease enter the task number you would like deleted:   "))
                    if 1 <= task_to_delete <= len(finished_tasks):
                        print(f"'{finished_tasks[task_to_delete - 1]}' was removed successfully!")
                        remove_task(task_to_delete, finished_tasks)
                    else:
                        print("The task number entered does not exist.")
                except ValueError:
                    print("Invalid entry, please submit a valid number.")
            
        case '5':
            print("Thank you for using our program!\n")
            break
            
        case _:
            print("User input must be an integer, please re-try.\n\n")