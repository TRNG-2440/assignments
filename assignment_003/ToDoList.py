"""Build a console-based To-Do List Manager that 
allows a user to add tasks, view all tasks, mark 
tasks as complete, and remove completed tasks. 
This activity focuses on lists and practices 
while loops,if-elif-else, for loops, input(), 
and list methods including append, remove, and indexing."""

# Main menu
def Menu():

  print("\n------------------------------"\
  "\n     TO-DO LIST MANAGER"\
  "\n------------------------------"\
  '\n1. Add a Task'\
  '\n2. View all Tasks'\
  '\n3. Mark a task as Complete'\
  '\n4. Remove a completed task'\
  '\n5. Clear all tasks'\
  '\n0. Exit\n')

# Produce algorithm used to manage each task
def TaskManager(option, map, isMenu):
  
  while(True):

    if(isMenu):

      # Display menu
      Menu()

      # Prompt user
      option = input('Select an option: ')
    
    else:
      isMenu = True

    isTerminated = False

    match(option):

      case "0":
        
        print("\nProgram has been terminated.")

        print("\nGoodbye!\n")

        break

      case "1":

        isEmpty = True

        while isEmpty:
          task = input('\nInput a task: ')

          if not task:
            print('\nError - task is empty. Please re-enter task')

          else: 
            isEmpty = False
            map[task] = "Incomplete"
            print(f'\nTask successfully added: {task}')
        
      case "2":

        if(map):
          print("\n------------------------------"\
          "\n         View Tasks"\
          "\n------------------------------")
          for i, (key, value) in enumerate(map.items()):
            print(f'{i+1}. {key} | {value}')
          
        else:
          print("\nList is empty.  Please add a task.")

      case "3":

        if(map):
          task = input("\nMark task as complete: ")

          while(True):
            if map.get(task):
              map[task] = "Complete"
              print(f'\n{task} has been marked as complete!\n')
              break

            else:
              print("\nInvalid input - please re-enter\n")
              task = input("\nMark task as complete: ")

        else:
          print("\nList is empty.  Please add a task.")

   

      case "4":

        if(map):
            task = input("\nRemove task: ")

            while(True):
              if map.get(task):
                map.pop(task)
                print(f'\n{task} has been sucessfully removed')
                break
          

              else:
                print(f'\n{task} was not found\n')
                break
            
        else:
          print("\nList is empty.  Please add a task.")

        
      case "5":

        if(map):
          select = input('\nAre you sure to clear list (Y/N)? ')
          
          if select.lower() == 'y':
            map.clear()

          else:
            print("\nList has not been cleared\n")

          while(select.lower() != 'y' or select.lower() != 'n'):
            print("\nInvalid input - Please enter\n")
            select = input('\nAre you sure to clear list (Y/N)? ')
            
          else:
            print("\nList is empty.  Please add a task.")

      case _:
    
          # Alert user that invalid entry was enter
          print('\nInvalid entry - please re-enter option') 

          break

    if(isTerminated):
      break

# Display menu      
Menu()

# Declare dictionary.  
# key = task, value = boolean value determining if task is complete/incomplete
map = dict()

# Prompt user
task = input('Select an option: ')

# Execute task manager
TaskManager(task, map, False)

