#Code Solution for assignment 5
#Alex Tran

#Contact Book



contacts = []
#Display Menu
while True:
    print("\n=== CONTACT BOOK MENU ===")
    print("1. Add a contact")
    print("2. View all contacts")
    print("3. Search for contacts")
    print("4. Delete a contact")
    print("5. Exit")


    option = input("Select your option from the menu: ")

    # Adding a contact
    if option == "1":
        name = input("Enter a name: ") 
        phone = input("Enter a phone number: ")
        email = input("Enter an email address: ")

        #group together in a tuple

        contact = (name, phone, email)

        contacts.append(contact)
        print(f"Contact {name} added successfully.")
    
    #View all contacts
    elif option == "2":
        if len(contacts) == 0:
            print("No contacts available.")
        
        else:
            print("---List of Contacts---")
            for i, (name, phone, email) in enumerate(contacts, start = 1):
                print(f"{i}. {name} | {phone} | {email}")
    
    #Search contacts
    elif option == "3":
        if len(contacts) == 0:
            print("No contacts available to search. ")
        search_contact = input("Enter the name you want to find: ")

        found = False
        for contact in contacts:
            #unpack the tuple

            name, phone, email = contact
            if name.lower() == search_contact.lower():
                print("\n Contact Found")
                print(f"Name: {name}")
                print(f"Phone: {phone}")
                print(f"Email: {email}")

                found = True
                break
        
        if found == False:
            print("Contact not found.")

    #Delete contact
    elif option == "4":
        if len(contacts) == 0:
            print("No contact to delete")
        else:
            print("---List of Contacts---")
            for i, contact in enumerate(contacts, start = 1):
                name, phone, email = contact
                print(f"{i}. {name} | {phone} | {email}")
            
            try:
                contact_num = input("Enter the number of the contact you want to delete: ")
                
                if 1 <= contact_num <= len(contacts):
                    deleted_contact = contacts.pop(contact_num -1)

                    name, phone, email = deleted_contact
                    print(f"Contact {name} deleted successfully.")
                else:
                    print("Invalid contact number.")
            except ValueError:
                print("Please enter a valid number")
    
    #Exit program
    elif option == "5":
        print("Exiting program. Goodbye!")
        break

    #Invalid menu option
    else:
        print("Invalid menu choice. Please enter a valid number from the menu.")


