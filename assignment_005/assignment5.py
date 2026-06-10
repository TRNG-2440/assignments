"""
Assignment 5
# Python Coding Activity 5 — Contact Book

## Objective

Build a console-based Contact Book that stores contacts as tuples and holds them in a list. The user can add contacts, view all contacts, search for a contact by name, and delete a contact. This activity focuses on **tuples** and **lists together**, and practices tuple packing, tuple unpacking, `for` loops, `while` loops, `if-elif-else`, and `input()`.

---

## Background

A tuple is the good choice for storing an individual contact because:

- A contact's fields (name, phone, email) are **fixed** — they belong together as a unit and a tuple enforces that structure
- Tuples are **immutable** — a contact record should not be partially edited in place; instead it is removed and re-added if changes are needed
- Tuples support **unpacking** — you can cleanly extract name, phone, and email in one line

A list is used to hold all contacts because:

- The collection of contacts needs to **grow and shrink** as contacts are added and removed
- Contacts need to be **iterated over** for viewing and searching

---

## Requirements

### Data

- Maintain a single list called `contacts`
- Each entry in `contacts` should be a **tuple** with exactly three values:
  - `name` (str)
  - `phone` (str)
  - `email` (str)

### Menu Options

The program should present the following menu in a loop until the user exits:

```
1. Add a contact
2. View all contacts
3. Search for a contact
4. Delete a contact
0. Exit
```

### Feature Instructions

**1. Add a contact**
- Prompt the user to enter a name, phone number, and email address
- Store the input into a Tuple
- Add this tuple to the `contacts` list
- Print a confirmation message

**2. View all contacts**
- If the list is empty, print a message saying so
- Otherwise display each contact's details in a formatted, numbered list

**3. Search for a contact**
- Prompt the user to enter a name to search for
- If a contact's name matches (case-insensitive), display their full details
- If no match is found, print a message saying the contact was not found

**4. Delete a contact**
- Display all contacts in a numbered list
- Prompt the user to enter the number of the contact to delete
- Remove the selected conntact from the `contacts` list
- Print a confirmation message
- Handle the case where the user enters an invalid number

**0. Exit**
- Print a goodbye message and exit the loop

---

## Requirements Checklist

- A `contacts` list holding contact tuples
- Each contact stored as a **tuple**
- A menu with selectable options
- Feature to add new contacts
- Feature to remove existing contacts
- A feature to search for a contact by name (case insensitive)
- Handles invalid input selection

---

## Example Interaction

```
════════════════════════════════════════
           CONTACT BOOK
════════════════════════════════════════
1. Add a contact
2. View all contacts
3. Search for a contact
4. Delete a contact
0. Exit
════════════════════════════════════════
Select an option: 1

Enter name  : Joseph Smith
Enter phone : 555-123-4567
Enter email : joseph@email.com
✔ Contact added: Joseph Smith

════════════════════════════════════════
Select an option: 2

All Contacts:
────────────────────────────────────────
1. Name  : Joseph Smith
   Phone : 555-123-4567
   Email : joseph@email.com
────────────────────────────────────────
2. Name  : Alice Jones
   Phone : 555-987-6543
   Email : alice@email.com
────────────────────────────────────────

════════════════════════════════════════
Select an option: 3

Enter name to search: alice
────────────────────────────────────────
Name  : Alice Jones
Phone : 555-987-6543
Email : alice@email.com
────────────────────────────────────────

════════════════════════════════════════
Select an option: 0
Goodbye!
```

---

## Stretch Goals

Once the core program is working, try adding:

- An **"Edit a contact"** option — remember that tuples are immutable
- A check that prevents adding a **duplicate name**
- **Sort contacts** - feature to display contacts by name either alphabetically or reverse alphabetically
- **Classes** - Create a class to represent Contact entries and refactor your code to use class instead.

"""

MENU: list[str] = [
    "Add a contact",
    "View all contacts",
    "Search for a contact",
    "Delete a contact",
]

DIVIDER: str = "════════════════════════════════════════"
MINOR_DIVIDER: str = "────────────────────────────────────────"
NO_CONTACTS: str = "There are no contacts currently."


def main() -> None:
    """
    The main control flow
    :return:
    """

    #name, phone, email
    contacts: list[tuple[str, str, str]] = []

    print_header()
    while(True):
        try:
            print_menu()
            print("0. Exit")
            print(DIVIDER)
            selection: int = int(input("Select an option: "))
            print("")
            if selection > len(MENU) or selection < 0:
                #only allow valid options
                raise ValueError

            match selection:
                case 1:
                    add_contact(contacts)
                case 2:
                    view_contacts(contacts)
                case 3:
                    search_contact(contacts)
                case 4:
                    delete_contact(contacts)
                case 0:
                    print("Goodbye!")
                    return

        except ValueError:
            continue

        except KeyboardInterrupt:
            break

def print_header() -> None:
    """
    Prints the header
    :return:
    """
    print(DIVIDER)
    print("\t\t\tCONTACT BOOK\t\t\t")
    print(DIVIDER)

def print_menu() -> None:
    """
    Prints the menu
    :return:
    """
    for i in range (0, len(MENU)):
        item = MENU[i]
        print(f"{i+1}. {item}")

def add_contact(contacts: list[tuple[str, str, str]]) -> None:
    """
    Prompts the user for a new contact, and then adds it to the contacts
    :param contacts:
    :return:
    """
    #TODO no duplicate names
    name: str = input("Enter name: ")
    phone: str = input("Enter phone: ")
    email: str = input("Enter email: ")
    new_contact: tuple[str, str, str] = (name, phone, email)
    contacts.append(new_contact)
    print(f"✔ Contact added: {name}")
    print("")
    print(DIVIDER)

def view_contacts(contacts: list[tuple[str, str, str]]) -> None:
    """
    Shows all contacts
    :param contacts:
    :return:
    """

    if len(contacts) == 0:
        print(NO_CONTACTS)
        print("")
        print(DIVIDER)
        return
    print(MINOR_DIVIDER)
    for i in range(0, len(contacts)):
        contact: tuple[str, str, str] = contacts[i]
        print_contact(contact, str(i+1) + ".")
        print(MINOR_DIVIDER)

    print("")
    print(DIVIDER)

def search_contact(contacts: list[tuple[str, str, str]]):
    """
    Searches for a contact by name (case-insensitive)
    :param contacts:
    :return:
    """
    if len(contacts) == 0:
        print(NO_CONTACTS)
        print("")
        print(DIVIDER)
        return

    search: str = input("Enter name to search: ")

    for contact in contacts:
        if search.lower() == contact[0].lower():
            print(MINOR_DIVIDER)
            print_contact(contact)
            print(MINOR_DIVIDER)
            print("")
            print(DIVIDER)
            return

    print(f"No contact with the name {search} found.")
    print("")
    print(DIVIDER)

def delete_contact(contacts: list[tuple[str, str, str]]):
    """
    Prompts a user to delete a contact
    :param contacts:
    :return:
    """

    if len(contacts) == 0:
        print(NO_CONTACTS)
        print("")
        print(DIVIDER)
        return
    print(MINOR_DIVIDER)
    for i in range(0, len(contacts)):
        contact: tuple[str, str, str] = contacts[i]
        print_contact(contact, str(i+1) + ".")
        print(MINOR_DIVIDER)

    while True:
        try:
            selection: int = int(input("Choose a contact to delete: "))

            if selection > len(contacts) or selection < 1:
                raise ValueError

            selection -= 1
            to_delete: tuple[str, str, str] = contacts.pop(selection)

            print(f"Deleted Contact: {to_delete[0]}")
            print("")
            print(DIVIDER)
            break

        except ValueError:
            pass

def print_contact(contact: tuple[str, str, str], prefix = "") -> None:
    """
    Prints a contract
    :param contact:
    :param prefix:
    :return:
    """
    print(f"{prefix}\tName: {contact[0]}")
    print(f"\tPhone: {contact[1]}")
    print(f"\tEmail: {contact[2]}")

if __name__ == "__main__":
    main()
