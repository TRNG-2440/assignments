class Contact:
    def __init__(self, name: str, phone: str, email: str):
        self.name = name
        self.phone = phone
        self.email = email
    
    def __str__(self):
        return self.name
    
    def __eq__(self, comp):
        if type(comp) == Contact:
            return self.name == comp.name
        if type(comp) == str:
            return self.name == comp
        return False

    def info(self):
        return f"name:  {self.name}\nphone: {self.phone}\nemail: {self.email}"

class ContactList:
    def __init__(self):
        self.contacts = []

    def add_contact(self, new):
        if type(new) != Contact:
            print("not a contact, no action")
            return None
        if new in self.contacts:
            print("contact exists")
        else:
            self.contacts.append(new)
            

    def display_contacts(self):
        if not len(self.contacts):
            print("no contacts to display")
            return None
        for c in sorted(self.contacts, key=lambda c: c.name):
            print(c.info(), end="\n\n")

    def lookup(self):
        name = input("enter a name to lookup: ")
        try:
            idx = self.contacts.index(name)
            print(self.contacts[idx].info())
        except ValueError:
            print("contact doesn't exist")
        except:
            raise

    def edit_contact(self):
        if not len(self.contacts):
            print("no contacts to display")
            return None
        
        print_menu(*self.contacts)
        s = get_selection(len(self.contacts))
        if not s:
            return None
        print(self.contacts[s-1])
        phone = input("edit phone: ").lower()
        email = input("edit email: ").lower()
        if phone:
            self.contacts[s-1].phone = phone
        else:
            print("no change to phone number")
        if email:
            self.contacts[s-1].email = email
        else:
            print("no change to email")
        
    def remove_contact(self):
        if not len(self.contacts):
            print("no contacts to display")
            return None
        
        print_menu(*self.contacts)
        s = get_selection(len(self.contacts))

        if not s:
            removed = self.contacts.pop(s-1)
            print(f"removing {removed} from your contacts")
        else:
            print("no contact removed")

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
        print()
        match sel:
            case sel if sel < 0 :
                print("value too low")
                valid = False
            case sel if sel > lim:
                print("value too high")
                valid = False
            case _:
                valid = True
    return sel

if __name__ == "__main__":

    menu_options = {1: "Add a contact",
                    2: "View all contacts",
                    3: "Search for a contact",
                    4: "Edit a contact",
                    5: "Delete a contact"}
    cl = ContactList()

    print_menu(*menu_options.values())
    while user_selection := get_selection(len(menu_options)):
        match user_selection:
            case 1: # add contact
                name = input("enter name: ").lower()
                phone = input("enter phone: ").lower()
                email = input("enter email: ").lower()
                if name:
                    cl.add_contact(Contact(name, phone, email))
                else:
                    print("no name entered, no contact added")
            case 2: # view all contacts
                cl.display_contacts()
            case 3: # search for a contact
                cl.lookup()
            case 4: # edit a contact
                cl.edit_contact()
            case 5: # delete a contact
                cl.remove_contact()
            case 0: # exit
                pass
        print_menu(*menu_options.values())
    print("exiting...")