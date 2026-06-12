# contact class
class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

# contact list
contacts: list[Contact] = []

# outer loop for contact book
while True:
    # options 
    print("════════════════════════════════════════")
    print("           CONTACT BOOK")
    print("════════════════════════════════════════")
    print("1. Add a contact")
    print("2. View all contacts")
    print("3. Search for a contact")
    print("4. Delete a contact")
    print("5. Edit a contact")
    print("6. View Contacts Alphabetically")
    print("0. Exit")
    print("════════════════════════════════════════")
    
    choice = int(input("Select an option: "))
    
    match choice:
        case 0: # exit
            print("Goodbye!")
            break

        case 1: # add contact 
            print("")
            while True:
                name = input("Enter a name: ")
                duplicate = False
                for contact in contacts:
                    if contact.name.lower() == name.lower():
                        duplicate = True
                if duplicate:
                    print(f"Contact with {name} already exists. Please enter a different name.")
                    print("")
                else:
                    break
            phone = input("Enter a phone number: ")
            email = input("Enter an email address: ")
            contacts.append(Contact(name, phone, email))
            print(f"\nContact added: {name}")
            print("")
            
        case 2: # view contacts
            print("")
            if not contacts:
                print("No contacts found. Returning to main menu.")
                print("")
            else:
                print("All Contacts:")
                print("────────────────────────────────────────")
                for i, contact in enumerate(contacts, 1):
                    print(f"{i}. Name: {contact.name}\n   Phone: {contact.phone}\n   Email: {contact.email}\n────────────────────────────────────────")
                print("")

        case 3: # search for contact
            print("")
            if not contacts:
                print("No contacts found. Returning to main menu.")
                print("")
            else:
                name = input("Enter name to search for: ")
                for contact in contacts:
                    if contact.name.lower() == name.lower():
                        print(f"────────────────────────────────────────")
                        print(f"Name: {contact.name}")
                        print(f"Phone: {contact.phone}")
                        print(f"Email: {contact.email}")
                        print(f"────────────────────────────────────────")
                        print("")
                        break
                else:
                    print(f"Contact not found: {name}. Returning to main menu.")
                    print("")

        case 4: # delete contact
            print("")
            if not contacts:
                print("No contacts found. Returning to main menu.")
                print("")
            else:
                print("All Contacts:")
                print("────────────────────────────────────────")
                for i, contact in enumerate(contacts, 1):
                    print(f"{i}. Name: {contact.name}\n   Phone: {contact.phone}\n   Email: {contact.email}\n────────────────────────────────────────")
                print("")

                while True: # repeat until valid number entered
                    number = int(input("Enter the number of the contact to delete: "))
                    if 1 <= number <= len(contacts):
                        deleted_contact = contacts.pop(number - 1)
                        print(f"\nContact deleted: {deleted_contact.name}")
                        print("")
                        break
                    else:
                        print(f"Invalid number: {number}. Please try again.")
                        print("")

        case 5: # edit a contact
            print("")
            if not contacts:
                print("No contacts found. Returning to main menu.")
                print("")
            else:
                print("All Contacts:")
                print("────────────────────────────────────────")
                for i, contact in enumerate(contacts, 1):
                    print(f"{i}. Name: {contact.name}\n   Phone: {contact.phone}\n   Email: {contact.email}\n────────────────────────────────────────")
                print("")
            
                while True: # repeat until valid number entered
                    number = int(input("Enter the number of the contact to edit: "))
                    if 1 <= number <= len(contacts):
                        print(f"Contact to edit: {contacts[number - 1].name}")
                        contacts.pop(number - 1)
                        print("")
                        name = input("Enter new name: ")
                        phone = input("Enter new phone number: ")
                        email = input("Enter new email address: ")
                        contact = Contact(name, phone, email)
                        contacts.insert(number - 1, contact)

                        print(f"\nContact edited: {name}")
                        print("")
                        break
                    else:
                        print(f"Invalid number: {number}. Please try again.")
                        print("")

        case 6:
            print("")
            if not contacts:
                print("No contacts found. Returning to main menu")
                print("")
            else:
                print("All Contacts:")
                print("────────────────────────────────────────")
                sorted_contacts = sorted(contacts, key=lambda x: x.name)
                for i, contact in enumerate(sorted_contacts, 1):
                    print(f"{i}. Name: {contact.name}\n   Phone: {contact.phone}\n   Email: {contact.email}\n────────────────────────────────────────")
                print("")
            
