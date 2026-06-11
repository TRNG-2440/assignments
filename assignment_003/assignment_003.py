pending_tasks = []
completed_tasks = []

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
def add_task() -> None:
    """
    Adds a task to the pending task list
    """
    
if __name__ == "__main__":
    print("-" * 30)
    print("To do list manager")
    print("-" * 30)
    print("Please select an option\n1. Add a task\n2. View all tasks\n3. Mark a task as complete \n" \
            "4. Remove a completed task\n5. Exit")
    while True:
        user_choice = get_selection(5)
        if user_choice == 5:
            break
        