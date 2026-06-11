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
