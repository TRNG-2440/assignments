# Necessary variables
contact_list = []

# Necessary Functions
def addContactToList(contactList):
    # Collect info from user, save to tuple
    contact_name =  input("What is the contact's name?") # Get name of contact
    contact_phone = input("What is the contact's phone number?") # Get the Phone number
    contact_email = input("What is the contact's email?") # Get the email
    
    # Create tuple and add to list
    contact_list.append((contact_name, contact_phone, contact_email))

def viewAllContacts():
    if not contact_list: # Check for null
        print("Contact list empty!")

    # Print the list
    print("--------------------------------\n" \
          "Contact List:")
    for contact in contact_list:
        print(f"{contact[0]:<20} {contact[1]:<12} {contact[2]:<20}")
    print(f"You have {len(contact_list)} saved")

def searchForContact():
    if not contact_list: # Check for null
        print("Contact list empty!\nAdd Contacts to search for\n")

        
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
        continue # TODO
    elif user_input == "2": # View all contacts
        continue # TODO
    elif user_input == "3": # Search for a contact
        continue # TODO
    elif user_input == "4": # Delete a contact
        continue # TODO
    else:
        print("Invalid Input!\n")