class Task:
    """
    task object
    - name -- string
    - desc -- string
    - status -- string - pending, completed
    """
    def __init__(self, name:str="", desc:str="", status:str="pending"):
        self.name = name
        self.desc = desc
        self.status = status

    def __str__(self):
        return self.name
    
    def describe(self):
        return f"\tName: {self.name}\n\tDescription: {self.desc}\n\tStatus: {self.status}"

class TaskList:
    def __init__(self):
        self.pending = []
        self.completed = []
    def add_task(self, task:Task):
        if type(task) == Task:
            self.pending.append(task)
        else:
            raise Exception("not a task")
    def view_all(self):
        if len(self.pending) + len(self.completed) < 1:
            print("no tasks")
            return None
        print("Pending:")
        for p in self.pending:
            print(p.describe() + "\n")
        print("Completed:")
        for c in self.completed:
            print(c.describe() + "\n")
    def mark_complete(self):
        if not len(self.pending):
            print("nothing pending")
            return None
        print_menu(*self.pending)
        s = get_selection(len(self.pending))
        if not s:
            print("no change")
        else:
            temp = self.pending.pop(s-1)
            self.completed.append(temp)
            print(f"Completed {temp}")
    def remove_completed(self):
        if not len(self.completed):
            print("nothing to remove")
            return None
        print_menu(*self.completed)
        s = get_selection(len(self.completed))
        if not s:
            print("nothing removed")
        else:
            print(f"removed completed task: {self.completed.pop(s-1)}")

def print_menu(*args:str) -> None:
    """
    print main menu from list
    """
    print()
    for idx, item in enumerate(args, 1):
        print(f"{idx}. {item}")
    print(f"0. exit")

def get_selection(lim:int = 0) -> int:
    """
    get selection from user, return int within limit
    - repeat on ValueError
    """
    valid = False
    while not valid:
        try:
            sel = int(input(f"select a number between 1-{lim}: "))
        except ValueError:
            print("bad value")
            continue
        except Exception as e:
            raise e

        match sel:
            case sel if sel < 0 :
                print("value too low")
                valid = False
            case sel if sel > lim:
                print("value too hight")
                valid = False
            case _:
                valid = True
    return sel

if __name__ == "__main__":
    menu_options = {1: "Add a task", 
                    2: "View All tasks", 
                    3: "Mark a task as complete", 
                    4: "Remove a completed task"}
    statuses = {1: "pending", 2: "completed"}
    tasks = TaskList()

    print_menu(*menu_options.values())
    while user_selection := get_selection(len(menu_options)):
        match user_selection:
            case 1: # add task
                name = input("enter the name of your task: ")
                desc = input("describe your task: ")
                tasks.add_task(Task(name, desc))
            case 2: # view all
                tasks.view_all()
            case 3: # mark complete
                tasks.mark_complete()
            case 4: # remove complete
                tasks.remove_completed()
            case 0: # exit
                pass
        print_menu(*menu_options.values())
