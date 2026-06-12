# Assignment 5 by Ariyan Shaikh

# This contacts list stores contacts each contact is a tuple
# Structure of stored tuples
# First index name
# Second index phone
# third index email
contacts = []

def get_selection(num_selections: int) -> int:
    """
    Collects and validates users's Selection.
    Requires the number of selections passed as an int paramater
    """
    while True:
        try:
            selection = int(input("Select an option: "))        
            if selection > num_selections or selection < 1:
                raise Exception("Invalid input detected")
        except Exception as ex:
            print("\nThat is not a valid input. Please try again\n")
            return get_selection(num_selections)
        return selection

def add_contact() -> None:
    """
    Prompts user to create a contact then stores it as a tuple in the
    contacts list
    """
    contacts.append((input(f'{"Enter name":<12}: '), input(f'{"Enter phone":<12}: '), input(f'{"Enter email":<12}: ')))
    print(f"✔ Contact added: {contacts[-1][0]}\n")

def show_contacts() -> None:
    if not contacts:
        print("\nYou have not added any contacts yet.\n")
        return
    print("\nAll Contacts:")
    for i, contact in enumerate(contacts, start=1):
        print("-" * 40)
        print(f'{i}.{"Name":<6}: {contact[0]}')
        print(f'  {"Phone":<6}: {contact[1]}')
        print(f'  {"Email":<6}: {contact[2]}')
    print("-" * 40)
    print()
    return

def search_contact() -> None:
    user_query = input("Enter name to search: ")
    contacts_to_print = []
    for contact in contacts:
        if any(word in contact[0].lower() for word in user_query.lower().split()):
            contacts_to_print.append(contact)
    if not contacts_to_print:
        print("Not found")
        return
    for i, contact in enumerate(contacts_to_print, start=1):
        print("-" * 40)
        print(f'{i}.{"Name":<6}: {contact[0]}')
        print(f'  {"Phone":<6}: {contact[1]}')
        print(f'  {"Email":<6}: {contact[2]}')
    print("-" * 40)
    return

def remove_contact() -> None:
    if not contacts:
        print("\nYou have not added any contacts yet.\n")
        return
    show_contacts()
    contacts.pop(get_selection(len(contacts)) - 1)
    print("Done\n")


if __name__ == "__main__":
    print("=" * 40)
    print(f'{"CONTACT BOOK":^40}')
    print("=" * 40)
    print("1. Add a contact")
    print("2. View all contacts")
    print("3. Search for a contact")
    print("4. Delete a contact")
    print("5. Exit")
    
    while True:
        selected_option = get_selection(5)
        match selected_option:
            case 1:
                print("=" * 40)
                add_contact()
                print("=" * 40)
            case 2:
                print("=" * 40)
                show_contacts()
                print("=" * 40)
            case 3:
                print("=" * 40)
                search_contact()
                print("=" * 40)
            case 4:
                print("=" * 40)
                remove_contact()
                print("=" * 40)
            case 5:
                print("Goodbye")
                break