"""
To-Do List Manager that allows a user to add tasks,
view all tasks, mark tasks as complete, and remove completed tasks
"""

def main():
   pending_tasks = [] # tasks that have not yet been completed
   completed_tasks = [] # tasks that have been completed
   while True:
            try:
                
                print()
                print("=========================================================================")

                print("To Do List Manager: ")
                print("1. Add a task")
                print("2. View all tasks")
                print("3. Mark a task as complete")
                print("4. Remove a completed task")
                print("5. Exit")

                print()
                to_do_choice = int(input("Please select an option(1-5): "))

                print("\n=========================================================================")
                print()

                match to_do_choice:
                    case 1:
                          add_task(pending_tasks)
                    case 2:
                          view_tasks(pending_tasks, completed_tasks)
                    case 3:
                          mark_complete(pending_tasks, completed_tasks)
                    case 4:
                          remove_completed(completed_tasks)
                    case 5:
                          print("Exiting program")
                          break
                    case _:
                          print("Invalid selection")
                          continue

            except Exception as e:
                print(f"Exception: {e}")  
                print("Invalid Selection. Please try again.") 
                continue

def add_task(pending_list):
    # - Prompt the user to enter a task description
    # - Add the task to the `pending_tasks` list
    # - Print a confirmation message
    while True:
        try:
            task_desc = input("Enter a task description: ")
            pending_list.append(task_desc)
            print("Task successfully added to Pending Task List!")
            return
        except Exception as e:
             print(f"Exception: {e}")
             print("Please enter a valid task description(ie. 'Do Laundry')")
             continue
  


        
def view_tasks(pending_list, completed_list):
    # - Display all items in `pending_tasks`, numbered from 1 to n
    # - Display all items in `completed_tasks`, numbered from 1 to n
    # - If either list is empty, print a message saying so
    if pending_list: #if list has items
        print("Pending Tasks:")
        count = 0
        for pending in pending_list:
            count+=1
            print(f"{count:>5}. {pending}")
    else:
        print("Pending Task List is Empty!")

    if completed_list:
        print("Completed Tasks:")
        count = 0
        for completed in completed_list:
            count+=1
            print(f"{count:>5}. {completed}")
    else:
        print("Completed Task List is Empty!")
    return
    

def mark_complete(pending_list, completed_list):
    # - Display the current `pending_tasks` list, numbered from 1 to n
    # - Prompt the user to enter the number of the task they want to complete
    # - Move that task from `pending_tasks` to `completed_tasks`
    # - Print a confirmation message
    # - Handle the case where the user enters an invalid number

    while True:
        count  = 0
        if pending_list: # checking if list has tasks
            print("Pending Tasks:")
            for pending in pending_list:
                count +=1
                print(f"{count:>5}. {pending}")
            try:
                task_num = int(input("Please enter the number of the task you would like to complete: "))
                #zero indexed so -1
                removed_task = pending_list.pop(task_num-1) #returns value of removed
                completed_list.append(removed_task) # adding to completed_list
                print("Successfully added '{removed_task}' to Completed Task List")
                return
            except Exception as e:
                 print(f"Exception: {e}")
                 print(f"Please enter a valid number between 1 and {count}")
                 continue
        else:
            print("No Pending Tasks. Please add a task to complete.")
            return



def remove_completed(completed_list):
    #- Display the current `completed_tasks` list, numbered from 1 to n
    #- Prompt the user to enter the number of the task they want to remove
    #- Remove that task from `completed_tasks`
    #- Print a confirmation message when a task is removed from completed tasks
    #- Handle the case where the user enters an invalid number
    while True:
        count = 0
        if completed_list:
            for completed in completed_list:
                count +=1
                print(f"{count:>5}. {completed}")
            try:
                task_num = int(input("Please enter the number of the task you would like to remove from Completed Task List: "))
                removed_task = completed_list.pop(task_num-1)
                print(f"Task: '{removed_task}' was removed from the Completed Task List")
                return
            except Exception as e:
                 print(f"Exception: {e}")
                 print(f"Please enter a valid task number between 1 and {count}.")
                 continue
        
        else:
            print("There are no tasks in Completed Task List to remove")
            return
          

if __name__ == "__main__":
    main()