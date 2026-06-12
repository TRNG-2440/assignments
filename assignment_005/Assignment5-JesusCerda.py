# Test Cases
# Bruce Wayne 8188188118 batman@email.com
# Super Man   2122122112 clarkKent@email.com
# Big Man Bob 6576576577 email@email.com

# Necessary variables
contact_list = []

# Necessary Functions
def addContactToList(p_contact_list):
    # Collect info from user, save to tuple
    contact_name =  input("Enter the contact's name:         ") # Get name of contact
    contact_phone = input("Enter the contact's phone number: ") # Get the Phone number
    contact_email = input("Enter the contact's email:        ") # Get the email
    
    # Create tuple and add to list
    p_contact_list.append((contact_name, contact_phone, contact_email))
    print(f"Contact {contact_name} added successfully!\n")

def viewAllContacts(p_contact_list):
    if not p_contact_list: # Check for null
        print("Contact list empty!")

    # Print the list
    print("--------------------------------\n" \
          "Contact List:")
    for contact in p_contact_list:
        print(f"{contact[0]:<20} {contact[1]:<12} {contact[2]:<20}")
    print(f"\nYou have {len(p_contact_list)} saved contacts")

def searchForContact(p_contact_list):
    if not p_contact_list: # Check for null
        print("\nContact list empty!\nAdd Contacts to search for\n")
        return
    user_input = input("What is the name you would like to search for: ")
    contacts_found = []
    for name, phone, email in p_contact_list:
        if user_input.lower() == name.lower():
            contacts_found.append((name, phone, email))
    if not contacts_found:
        print("\nNo matching contacts found!")
        return
    else:
        for name, phone, email in contacts_found:
            print(f"{name:<20} {phone:<12} {email:<20}")
    print(f"\nFound {len(contacts_found)} contacts\n")



def deleteContact(p_contact_list):
    contact_list_without_deletes = []
    if not p_contact_list: # Check for null
        print("\nContact list empty!\n")
        return
    user_input = input("What is the name you would like to delete for: ")
    contact_found = False
    for name, phone, email in p_contact_list:
        if user_input.lower() == name.lower():
            contact_found = True
            print(f"Deleting {name:<20} {phone:<12} {email:<20}")
        else:
            contact_list_without_deletes.append((name, phone, email))
    if not contact_found:
        print("\nNo matching contacts found!")
    else:
        print(f"\nDeleted {len(p_contact_list) - len(contact_list_without_deletes)} contacts")
        p_contact_list[:] = contact_list_without_deletes
    
    
        
# Menu
print(  "--------------------------------\n" \
        "          Contact Book          \n" \
        "--------------------------------\n" \
        "1. Add a contact\n" \
        "2. View all contacts\n" \
        "3. Search for a contact\n" \
        "4. Delete a contact\n" \
        "0. Exit\n")

while True:
    user_input = input( "\n--------------------------------\n" \
                        "Select an option: ")
    if user_input == "0":
        break
    elif user_input == "1": # Add a contact
        addContactToList(contact_list)
        continue
    elif user_input == "2": # View all contacts
        viewAllContacts(contact_list)
        continue
    elif user_input == "3": # Search for a contact
        searchForContact(contact_list)
        continue
    elif user_input == "4": # Delete a contact
        deleteContact(contact_list)
        continue
    else:
        print("Invalid Input!\n")