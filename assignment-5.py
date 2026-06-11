
def contact_book():
    fields = ["name", "phone", "email"]
    details = []
    contacts = zip(fields, details)



    while True:
        print("-" * 30)
        print("CONTACT BOOK")
        print("-" * 30)
        print("1. Add a contact")
        print("2. View all contacts")
        print("3. Search for a contact")
        print("4. Delete a contact")
        print("0. Exit")
        print("Select an option: ")
        option = input()

        if option == '0':
            print("Goodbye!")
            break

        elif option == '1':
            print("Enter name  :")
            name = input()
            print("Enter phone :")
            phone = input()
            print("Enter email :")
            email = input()
            x = list(contacts)
            x.append((name, phone, email))
            print(f'✔ Contact added: ("{name}", "{phone}", "{email}")')
            contacts = x

        elif option == '2':
            if not contacts:
                print("No contacts found.")
            else:
                for contact in contacts:
                    print(f'Name: {contact[0]}, \nPhone: {contact[1]}, \nEmail: {contact[2]}' + "\n------------------------------")

        elif option == '3':
            print("Enter name to search:")
            searched_name = input()
            found_contacts = [contact for contact in contacts if contact[0].lower() == searched_name.lower()]
            if found_contacts:
                for contact in found_contacts:
                    print(f'Name: {contact[0]}, \nPhone: {contact[1]}, \nEmail: {contact[2]}' + "\n------------------------------")
            else:
                print("Contact not found.")

        elif option == '4':
            for i in enumerate(contacts):
                print(f'{i[0]+1}. Name: {i[1][0]}, Phone: {i[1][1]}, Email: {i[1][2]}')
            print("Enter a name to delete the contact for:", end=' ')
            try:
                deletion = input()
                contacts = [contact for contact in contacts if contact[0].lower() != deletion.lower()]
                print(f'✔ Contact deleted: ("{deletion}")')
            except ValueError:
                print("Please enter a valid name.")

contact_book()