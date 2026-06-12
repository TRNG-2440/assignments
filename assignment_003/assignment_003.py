import time

pending_tasks = []
completed_tasks = []
class EmptyListException(Exception):
    """
    This is for jumping back in the stack.
    The whole point of this exception is to use something other than a standard while loop.
    I know this is a strange way to implemen a loop but I wanted to practice using exceptions.
    """
    pass

def get_selection(num_selections: int) -> int:
    """
    Collects and validates users's Selection.
    Requires the number of selections passed as an int paramater
    """
    while True:
        try:
            selection = int(input())        
            if selection > num_selections or selection < 1:
                raise Exception("Invalid input detected")
        except Exception as ex:
            print("\nThat is not a valid input. Please try again\n")
        return selection
    
def print_list(list_num: int) -> bool:
    """
    Prints the selected list based on what int is passed, only pass an integer that is either number 1 or 2
    if 1 is passed the function will print the pending tasks list
    if 2 is passed the function will print the completed tasks list
    The function will return True if the selected list has items and False if there are no items
    """
    if list_num == 1 and pending_tasks:
        print(*(f"\n{num}. {pending_tasks}" for num, pending_tasks in enumerate(pending_tasks, start=1)), sep="\n")
        return True
    if list_num == 2 and completed_tasks: 
        print(*(f"\n{num}. {completed_tasks}" for num, completed_tasks in enumerate(completed_tasks, start=1)), sep="\n")

        return True
    return False

def remove_task() -> None:
    """
    Allows user to pick and remove a task from either the pending or completed tasks list.
    """
    print("Please select an option\n1. Pending tasks\n2. Completed tasks\n 3. Back")
    selection = get_selection(3)
    if selection == 3:
        return
    if not print_list(selection):
        print("The selected list has no tasks, please select something else")
        raise EmptyListException
    print("Select a task to remove from the above list")
    match selection:
        case 1:
            pending_tasks.pop(get_selection(2) - 1)
            print("Task removed from pending tasks")
        case 2:
            completed_tasks.pop(get_selection(2) - 1)
            print("Task removed from completed tasks")
    return graceful_menu_return()
    
def complete_task() -> None:
    if not print_list(1):
        return print("You have no tasks to complete")
    print("Select the task you would like to mark as complete")
    completed_tasks.append(pending_tasks.pop(get_selection(2) - 1))
    print("Task completed")
    return graceful_menu_return()

def add_task() -> None:
    """
    Adds a task to the pending task list
    """
    pending_tasks.append(input("Enter a small description of the task: "))
    print("Task added to your pending tasks\n")
    return graceful_menu_return()

def graceful_menu_return() -> None:
    print("Returning to main menu...")
    return time.sleep(3)

if __name__ == "__main__":
    print("-" * 30)
    print("To do list manager")
    print("-" * 30)
    while True:
        print("Please select an option\n1. Add a task\n2. View all tasks\n3. Mark a task as complete \n" \
              "4. Remove a task\n5. Exit")
        user_choice = get_selection(5)
        match user_choice:
            case 1:
                add_task()
            case 2:
                if len(pending_tasks) == 0:
                    print("You have no pending tasks")
                else:
                    print("Pending Tasks")
                    print("-" * 30)
                    print_list(1)
                if len(completed_tasks) == 0:
                    print("You have no completed tasks")
                else:
                    print("Completed Tasks")
                    print("-" * 30)
                    print_list(2)
                graceful_menu_return()
            case 3:
                complete_task()
            case 4:
                try:
                    remove_task()
                except EmptyListException:
                    remove_task()
            case 5:
                break
        