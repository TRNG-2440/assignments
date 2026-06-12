class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email


def display_contact(num, contact):
    print(f"{num}. Name: {contact.name}")
    print(f"   Phone: {contact.phone}")
    print(f"   Email: {contact.email}")
    print("────────────────────────────────────────")


def contact_book():
    contacts = []

    while True:
        print("════════════════════════════════════════")
        print("           CONTACT BOOK")
        print("════════════════════════════════════════")
        print("1. Add a contact")
        print("2. View all contacts")
        print("3. Search for a contact")
        print("4. Delete a contact")
        print("5. Edit a contact")
        print("6. View contacts sorted A-Z")
        print("7. View contacts sorted Z-A")
        print("0. Exit")
        print("════════════════════════════════════════")

        user_menu = int(input("Select an option: "))

        match user_menu:
            case 1:
                name = input("Input your contact name: ").strip()
                phone = input("Input your phone number: ").strip()
                email = input("Input your email: ").strip()

                duplicate_found = False

                for contact in contacts:
                    if contact.name.lower() == name.lower():
                        duplicate_found = True
                        break

                if duplicate_found:
                    print(f"A contact named '{name}' already exists.")
                else:
                    new_contact = Contact(name, phone, email)
                    contacts.append(new_contact)
                    print(f"Contact added: {name}")

            case 2:
                if not contacts:
                    print("No contacts available.")
                else:
                    print("Contact list:")
                    for num, contact in enumerate(contacts, start=1):
                        display_contact(num, contact)

            case 3:
                if not contacts:
                    print("No contacts available.")
                else:
                    name_to_search = input("Input a name to search: ").strip()
                    found = False

                    for contact in contacts:
                        if contact.name.lower() == name_to_search.lower():
                            print("Contact found!")
                            print(f"Name: {contact.name}")
                            print(f"Phone: {contact.phone}")
                            print(f"Email: {contact.email}")
                            found = True
                            break

                    if not found:
                        print("There's no contact by that name.")

            case 4:
                if not contacts:
                    print("No contacts available.")
                else:
                    print("Contact list:")
                    for num, contact in enumerate(contacts, start=1):
                        display_contact(num, contact)

                    contact_to_del = int(input("Put the number of the contact to delete: "))

                    if contact_to_del < 1 or contact_to_del > len(contacts):
                        print("Please put a valid number.")
                    else:
                        deleted_contact = contacts[contact_to_del - 1]
                        contacts.remove(deleted_contact)
                        print(f"Deleted contact: {deleted_contact.name}")

            case 5:
                if not contacts:
                    print("No contacts available.")
                else:
                    print("Contact list:")
                    for num, contact in enumerate(contacts, start=1):
                        display_contact(num, contact)

                    contact_to_edit = int(input("Put the number of the contact to edit: "))

                    if contact_to_edit < 1 or contact_to_edit > len(contacts):
                        print("Please put a valid number.")
                    else:
                        contact = contacts[contact_to_edit - 1]

                        new_name = input("Input new contact name: ").strip()
                        new_phone = input("Input new phone number: ").strip()
                        new_email = input("Input new email: ").strip()

                        duplicate_found = False

                        for existing_contact in contacts:
                            if existing_contact.name.lower() == new_name.lower() and existing_contact != contact:
                                duplicate_found = True
                                break

                        if duplicate_found:
                            print(f"A contact named '{new_name}' already exists.")
                        else:
                            contact.name = new_name
                            contact.phone = new_phone
                            contact.email = new_email
                            print(f"Contact edited: {new_name}")

            case 6:
                if not contacts:
                    print("No contacts available.")
                else:
                    sorted_contacts = sorted(contacts, key=lambda contact: contact.name.lower())

                    print("Contacts sorted A-Z:")
                    for num, contact in enumerate(sorted_contacts, start=1):
                        display_contact(num, contact)

            case 7:
                if not contacts:
                    print("No contacts available.")
                else:
                    sorted_contacts = sorted(contacts, key=lambda contact: contact.name.lower(), reverse=True)

                    print("Contacts sorted Z-A:")
                    for num, contact in enumerate(sorted_contacts, start=1):
                        display_contact(num, contact)

            case 0:
                print("Goodbye!")
                break

            case _:
                print("Give a valid input (0-7)")


contact_book()