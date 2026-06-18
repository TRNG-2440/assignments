contacts []

while True:
   print("\nCONTACT BOOK")
   print("1. Add Contact")
   print("2. View all Contacts")
   print("3. Search for a contact")
   print("4. Delete a contact")
   print("5. Exit")

   choice = input("Select an option: ")

   if choice == "1":
      name = input("Enter your name:")
      phone = input("Enter phone: ")
      email = input("Enter email: ")
      
      contact = (name, phone, email)
      contacts.append(contact)

      print(f"Contact added: {name}")

    elif choice == "2":
      if not contacts:
         print("No contacts found.")
      else:
         print(\n"All Contacts: ")
               
         for i, contact in enumerate(contacts, start=1):
            name, phone, email = contact

            print(f"{i}. Name  : {name}")
                print(f"   Phone : {phone}")
                print(f"   Email : {email}")

    elif choice == "3":
        search_name = input("Enter the name to search for: ")

        found = False

        for contact in contacts:
           name, phone, email = contact

           if name.lower() == search_name.lower():
               print(f"Name : {name}")
               print(f"Phone : {phone}")
               print(f"Email : {email}")
               found = True
            
        if not found: 
            print("Contact not found.")
        
        elif choice == "4":
        if not contacts:
            print("No contacts available to delete.")
        else:
            print("\nContacts:")

            for i, contact in enumerate(contacts, start=1):
                name, phone, email = contact
                print(f"{i}. {name}")

            try:
                delete_num = int(input("Enter contact number to delete: "))

                if 1 <= delete_num <= len(contacts):
                    removed_contact = contacts.pop(delete_num - 1)
                    print(f"Contact deleted: {removed_contact[0]}")
                else:
                    print("Invalid contact number.")

            except ValueError:
                print("Please enter a valid number.")

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid selection. Please try again.")