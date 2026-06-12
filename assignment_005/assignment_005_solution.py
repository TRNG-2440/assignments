contacts = []

def print_menu():
    print("================================")
    print("Contact Book")
    print("================================")
    print("1. Add a contact")
    print("2. View all contacts")
    print("3. Search for a contact")
    print("4. Delete a contact")
    print("0. Exit")
    print("================================")

def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email address: ")
    contact = (name, phone, email)
    contacts.append(contact)
    print(f"Contact added : {name}")

def view_contacts():
    if not contacts:
        print("No contacts found.")
        return
    print("\nAll contacts:")
    for i, (name, phone, email) in enumerate(contacts, 1):
        print("---------------------------------")
        print(f"{i}. Name: {name}")
        print(f"    Phone: {phone}")
        print(f"    Email: {email}")  
    print("---------------------------------")

def search_contact():
    query = input("Enter Name for search: ").lower()
    found = False
    for name, phone, email in contacts:
        if query in name.lower().split()[0]:
            print("---------------------------------")
            print(f"Name: {name}")
            print(f"Phone: {phone}")
            print(f"Email: {email}")
            print("---------------------------------")
            found = True
    if not found:
        print("Contact not found.")

# def delete_contact():
#     if not contacts:
#         print("No contacts to delete.")
#         return
#     view_contacts()
#     try:
#         num = int(input("Enter the number of the contact to delete: "))
#         if 1 <= num <= len(contacts):
#             removed = contacts.pop(num - 1)
#             print(f"Contact deleted : {removed[0]}")
#         else:
#             print("Invalid contact number.")
#     except ValueError:
#         print("Please enter a valid number.")

def delete_contact():
    if not contacts:
        print("No contacts to delete.")
        return
    print("\nAll Contacts:")
    for i, (name, phone, email) in enumerate(contacts, 1):
        print("────────────────────────────────────────")
        print(f"{i}. Name  : {name}")
        print(f"   Phone : {phone}")
        print(f"   Email : {email}")
    print("────────────────────────────────────────")
    try:
        num = int(input("Enter the number of the contact to delete: "))
        if 1 <= num <= len(contacts):
            removed = contacts.pop(num - 1)
            print(f"✔ Contact deleted: {removed[0]}")
        else:
            print("Invalid number.")
    except ValueError:
        print("Please enter a valid number.")

while True:
    print_menu()
    choice = input("Enter your choice: ")
    if choice == "1":
        add_contact()
    elif choice == "2":
        view_contacts()
    elif choice == "3":
        search_contact()
    elif choice == "4":
        delete_contact()
    elif choice == "0":
        print("Exit")
        break
    else:
        print("Invalid choice. Please try again.")