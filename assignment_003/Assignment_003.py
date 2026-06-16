
completed_tasks= []
pending_tasks= []

def add_task():
    
    task = input("Enter the task: ")
    if not task.strip():
        print("Task cannot be empty")
        return
    pending_tasks.append(task)
    print("Task successfully added")
    
def view_tasks():
    
    if pending_tasks:
        for i, tasks in enumerate(pending_tasks, start=1):
            print(f"{i}. {tasks}")
    else:
        print("No tasks pending")
            
    
    if completed_tasks:
        for i, tasks in enumerate(completed_tasks, start=1):
            print(f"{i}. {tasks}")
    else:
        print("No completed tasks")

def complete_task():
    
    if pending_tasks:
        for i, tasks in enumerate(pending_tasks, start=1):
            print(f"{i}. {tasks}")
    else:
        print("No tasks pending")
        return
    try:
        task_number = int(input("Enter the task number to complete: "))
    except ValueError:
        print("Invalid input. Please enter a valid task number.")
        return
    if 0 <  task_number <= len(pending_tasks):
        completed_tasks.append(pending_tasks[task_number - 1])
        pending_tasks.pop(task_number - 1)
        print("Task marked as complete")
    else:
        print("Invalid task number")
        

def remove_task():
    
    if completed_tasks:
        for i, tasks in enumerate(completed_tasks, start=1):
            print(f"{i}. {tasks}")
    else:
        print("No completed tasks")
        return
    try:
        task_number = int(input("Enter the task number to remove"))
    except ValueError:
        print("Invalid input. Please enter a valid task number.")
        return
    if 0 < task_number <= len(completed_tasks):
        completed_tasks.pop(task_number - 1)
        print("Task successfully removed")
    else:
        print("Invalid task number")
    


while True:
    
    # print("```")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Remove Task")
    print("5. Exit")
    # print("```")
    choice = input("Enter your choice: ")
    
    if(choice == "1" or choice == "Add Task"):
        add_task()
    elif(choice == "2" or choice == "View Tasks"):
        view_tasks()
    elif(choice == "3" or choice == "Complete Task"):
        complete_task()
    elif(choice == "4" or choice == "Remove Task"):
        remove_task()
    elif(choice == "5" or choice == "Exit"):
        print("Goodbye!! Come again")
        break
    else:
        print("Invalid choice")
        