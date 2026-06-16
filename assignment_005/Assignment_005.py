contacts = []

def add_contact():
    name = input("Enter the name of the contact: ")
    phone_number = input("Enter the phone number of the contact: ")
    email = input("Enter the email of the contact: ")
    contacts.append((name, phone_number, email))
    
def view_contacts():
    if not contacts:
        print("No contacts found.")
    else:
        for i, contact in enumerate(contacts, start=1):
            print(f"{i}. Name: {contact[0]}, Phone: {contact[1]}, Email: {contact[2]}")

def search_contact():
    name_to_search = input("Enter the name of the contact to search for: ")
    name_to_search = name_to_search.lower()
    for contact in contacts:
        if contact[0].lower() == name_to_search:
            print(f"Contact found: Name: {contact[0]}, Phone: {contact[1]}, Email: {contact[2]}")
            return
    print("Contact not found.")

def delete_contact():
    view_contacts()
    try:
        number = int(input("Enter the number of the contact to delete: "))
        if 0 < number <= len(contacts):
            del contacts[number - 1]
            print("Contact deleted.")
        else:
            print("Invalid contact number.")
    except ValueError:
        print("Please enter a valid number.")

while True:
    
    print("1. Add a contact\n2. View all contacts")
    print("3. Search for a contact\n4. Delete a contact\n0. Exit")
    
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
        break
    else:
        print("Invalid choice. Please try again.")