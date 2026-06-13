contact_list = []

def main_menu():
    print(f"\n{"=" * 10}\nContact Book\n{"=" * 10}\n1. Add a contact\n2. View all contacts\n3. Search for a contact\n4. Delete a contact\n5. Exit\n\n")

def Add_contact():
    name = input("Enter contact Name: ")
    phone = input("Enter contact phone number: ")
    email = input("Enter contact email: ")
    contact_list.append((name, phone, email))
    print(f"Contact {name} added successfully!")


def view_all_contacts():
    if len(contact_list) == 0:
        print("No contacts have been added yet!")
    else:
        num_contacts = 1
        for contact in contact_list:
            name, phone, email = contact
            print(f"{num_contacts}. Name: {name}\nPhone: {phone}\nEmail: {email}\n\n")
            num_contacts += 1

def contact_search(search_name):
    if len(contact_list) == 0:
        print("No contacts have been added yet!")
    else:
        contact_found = False
        for contacts in contact_list:
            name, phone, email = contacts
            if name.lower() == search_name.lower():
                contact_found = True
                print(f"Name: {name}\nPhone: {phone}\nEmail: {email}\n\n")
        if not contact_found:
            print(f"Sorry, contact matching {search_name} not found!")


def delete_contact():
    if len(contact_list) == 0:
        print("No contacts have been added yet!")
    else:
        view_all_contacts()
        try:
            to_be_deleted = int(input("Enter the contact number you would like to delete:  "))
            if 1 <= to_be_deleted <= len(contact_list):
                deleted_contact = contact_list[to_be_deleted-1]
                contact_list.pop(to_be_deleted-1)
            else:
                print("The contact number you are trying to delete does not exist.")
        except Exception:
            print("Invalid entry, please submit an integer.")


while True:
    main_menu()
    user_input = input("Select an option: ")

    match user_input:
        case '1':
            Add_contact()
        case '2':
            view_all_contacts()
        case '3':
            search_name = input("Enter name to search: ")
            contact_search(search_name)
        case '4':
            delete_contact()
        case '5':
            print("Thank you for using our program!\n")
            break
        case _:
            print("User input must be an integer, please re-try.\n\n")