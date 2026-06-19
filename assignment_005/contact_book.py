"""
Loop through asking the user waht option they want

DS: Tuple, List

    Tuple = (name - str , phone - str , email - str)
    List = [(Tuple1), (Tuple2)]

Menu
    1. Add a contact
        - ask user for name, phone number, email
            - if the name and email combination is already there in the DS, 
        - add to tuple
        - add this tuple to list

    2. View all the contacts
        - If the list is empty, print message
        - display all contacts

    3. Search Contact
        - user gives name
            - loop over list
            - if name matches given name
            - print out that value
            - don't break out of loop until all items seen because then there might be multiple people with name name
        - no match --> let user know

    4. Delete contact
        - display all contacts in numbered list
            - enummerate!!
        - ask which contact to delete --> remove that
        - confirm deletion
        - try error block if thta number is out of range

    5. Edit contact
        - list out all the contacts, ask user which contact to edit
        - prompt user to provide name, phone, address of said person
        - DELETE that existing contact, replace it with the changed one

    0. Exit
        - break out of loop and say bye

"""

from time import sleep


def clear_console():
    print("\033[2J\033[H", end="", flush=True)


def add_contact(contacts):
    """
        1. Add a contact
        - ask user for name, phone number, email
            - if the name and email combination is already there in the DS, 
        - add to tuple
        - add this tuple to list
    """
    print("Seems like you want to add a person. I'm going to need their name, phone, and email.")

    name = input("Enter name: ").upper()
    phone = input("Enter phone number: ").upper()
    email = input("Enter email: ").upper()

    """TODO: Logic for editing contact"""
    # while True:
    #     name = input("Enter name: ")
    #     phone = input("Enter phone number: ")
    #     email = input("Enter email: ")

    #     if contacts:
    #         found = find_contact(contacts, email)
    #         if found:
    #             clear_console()
    #             edit = input("Sorry, this person already exists. Would you like to edit this person?")
    #             if edit.upper() == "yes":
    #                 return
    #     break
    
    person = (name, phone, email)
    contacts.append(person)
    print(f"{name} had been added to your contact book!")


def view_all_contacts(contacts):
    if not contacts:
        print("No contacts to show yet!")
        return

    print("Here are all your contacts:")
    for idx, contact in enumerate(contacts, start=1):
        name, phone, email = contact
        print("_________________________")
        print(f"{idx}. Name  : {name}")
        print(f"       Phone : {phone}")
        print(f"       Email : {email}")
    print("_________________________")


def search_contact(contacts):
    # handle the case that the person wants to look up be either name, number, or email
    if not contacts:
        clear_console()
        print("No contacts yet to show!!")
        verdict = input("But would you like to start creating new contacts?(yes or no)").upper()
        if verdict == "YES":
            add_contact()
            return
        elif verdict == "NO":
            clear_console()
            print("No worries! Taking you back to the main menu...")
            sleep(2)
            return
        else:
            print("\nSorry I didn't catch that... Taking you back to the main menu!")
            sleep(2)
            return
            
    target = input("Who would you like to look up? ").upper()
    
    i = 1
    found = False
    for name, phone, email in contacts:
        if target == name or target == phone or target == email:
            print("_________________________")
            print(f"{i}. Name  : {name}")
            print(f"     Phone : {phone}")
            print(f"     Email : {email}")
            i += 1
            found = True

    if not found:
        print("Sorry, I can't find that person. Try their name, phone, or email!")    


def delete_contact(contacts):
    if not contacts:
        print("Sorry, there aren't any contacts to delete at the moment!")
        return

    view_all_contacts(contacts)

    while True:
        try:
            to_delete = int(input("Which of these contacts would you like to delete? ")) - 1
        except ValueError:
            print("Please enter a number!")
            continue

        if 0 <= to_delete < len(contacts):
            removed = contacts.pop(to_delete)
            print(f"Deleted {removed[0]}!")    # removed is the whole tuple; [0] is the name
            break
        else:
            print("That's not a valid contact number!")


    
def main():
    contacts = []   # stores all our contacts

    while True:
        print("\nHi! Here is our Contacts menu:")
        print("1. Add a contact \n2. View all the contacts \n3. Search Contact \n4. Delete contact \n0. Exit")

        try:
            user_choice = int(input("How would you like to proceed? (enter a number)  "))
        except ValueError:
            print("Please enter a number!")
            continue
        
        if user_choice == 1:
            clear_console()
            add_contact(contacts)
        
        elif user_choice == 2:
            clear_console()
            view_all_contacts(contacts)
        
        elif user_choice == 3:
            clear_console()
            search_contact(contacts)
        
        elif user_choice == 4:
            clear_console()
            delete_contact(contacts)
        
        elif user_choice == 0:
            clear_console()
            print("Bye for now!!")
            break


if __name__ == "__main__":
    main()