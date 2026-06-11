main_menu = True
contacts = []


print("════════════════════════════════════════")
print("           CONTACT BOOK")
print("════════════════════════════════════════")
print("1. Add a contact")
print("2. View all contacts")
print("3. Search for a contact")
print("4. Delete a contact")
print("0. Exit")
print("════════════════════════════════════════")

while main_menu:

    choice = int(input("Select an option: "))
    print()

    match choice:
        case 1:
            name = input("Enter a name: ")
            phone_number = input("Enter phone : ")
            email = input("Enter email: ")
            contact = (name, phone_number, email)
            contacts.append(contact)
            print(f"✔ Contact added: {name}")
            print()
            print("════════════════════════════════════════")

        case 2:
            if len(contacts) > 0:

                print()
                print("All Contacts:")
                print("────────────────────────────────────────")

                for i, (name, phone_number, email) in enumerate(contacts, start=1):
                    print(f"{i}.  Name : {name}")
                    print(f"    Phone: {phone_number}")
                    print(f"    Email: {email}")
                    print("────────────────────────────────────────")

            else:
                print("No contacts found.")

            print()
            print("════════════════════════════════════════")
        
        case 3:
            if len(contacts) > 0:
                search_name = input("Enter a name to search: ")
                for contact in contacts:
                    if search_name in contact[0]:
                        print(f"Name : {contact[0]}")
                        print(f"Phone: {contact[1]}")
                        print(f"Email: {contact[2]}")
                        break
                else:
                    print("Contact not found.")
            
            else:
                print("No contacts found.")

            print()
            print("════════════════════════════════════════")
        
        case 4:
            if len(contacts) > 0:
                print()
                print("All Contacts:")
                print("────────────────────────────────────────")

                for i, (name, phone_number, email) in enumerate(contacts, start=1):
                    print(f"{i}.  Name : {name}")
                    print(f"    Phone: {phone_number}")
                    print(f"    Email: {email}")
                    print("────────────────────────────────────────")

                contact_to_delete = int(input("Enter the number of the contact to delete: "))
                if contact_to_delete < 1 or contact_to_delete > len(contacts):
                    print("Invalid contact number.")

                else:
                    print(f"✔ Contact deleted: {contacts[contact_to_delete - 1][0]}")
                    contacts.pop(contact_to_delete - 1)


            else:
                print("No contacts found.")
            
            print()
            print("════════════════════════════════════════")

        case 0:
            print("Goodbye!")
            break