contacts = []

def display_contacts():
    if contacts:
        print("All Contacts\n")
        for i in range(len(contacts)):
            print (f"{i+1}. Name: {contacts[i][0]}")
            print (f"   Phone Number: {contacts[i][1]}")
            print (f"   Email: {contacts[i][2]}")
            print()
        return True    
    else:
        print("There are no contacts in this list.\n")
        return False

while True: # menu
    print ("1. Add a contact")
    print ("2. View all contacts")
    print ("3. Search for a contact")
    print ("4. Delete a contact")
    print ("0. Exit")

    choice = input("Choose an option: ")
    print()

    match choice:
        case "1": # add contact
            new_name = input("Enter Name: ")
            new_phone = input("Enter Phone Number: ")
            new_email = input("Enter Email Address: ")

            contacts.append((new_name, new_phone, new_email)) # adding to contact list
            print(f"New contact added: {new_name}")

        case "2": # view all contacts
            display_contacts()

        case "3": # Search for a contact
            searched_name = input("Enter a name to search for: ")
            searched_name = searched_name.lower()

            flag = 0 # for contact found status
            for contact in contacts:
                if contact[0].lower() == searched_name:
                    print(f"Name: {contact[0]}\nPhone Number: {contact[1]}\nEmail: {contact[2]}\n")
                    flag = 1
                    break
            
            if not flag:
                print("Contact not found.")

        case "4": # Delete a contact
            if not display_contacts():
                continue

            while True:
                number = int(input("Enter the number of the contact you want to delete or press " \
                "0 if you want to go back: "))
                
                if number > 0 and number <= len(contacts):
                    contact = contacts.pop(number - 1)
                    print (f"{contact[0]} Deleted")
                    break
                elif number == 0:
                    break
                else:
                    print("Invalid number.")

        case "0": # exit
            break
