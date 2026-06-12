def main():
     
    contacts = []

    while True:
        print("=========================================")
        print("Contact Book")
        print("=========================================")
        print("1. Add a contact")
        print("2. View all contacts")
        print("3. Search for a contact")
        print("4. Delete a contact")
        print("0. Exit")

        try:
                print("=========================================")
                user_input = int(input("Please select an option(1-4) or 0 to exit: "))
                print()
                match user_input:
                    case 1:
                        case_1(contacts)
                        print()
                        
                    case 2:
                        case_2(contacts)
                        print()
                        
                    case 3:
                        case_3(contacts)
                        print()
                    case 4:
                        case_4(contacts)
                        print()
                    case 0:
                        print("exiting program...Goodbye.")
                        break
                    case _:
                        print("Invalid selection.")
                        continue
        except ValueError:
            print("Invalid selection. Please type an integer.")
            continue


def case_1(contacts):
    input_name = input("Enter name: ")
    input_phone = input("Enter phone number: ")
    input_email = input("Enter email")

    contact_tuple = (input_name,input_phone,input_email)
    contacts.append(contact_tuple)
    print(f"Contact added: {input_name}")

    return

def case_2(contacts):
    """- If the list is empty, print a message saying so
- Otherwise display each contact's details in a formatted, numbered list"""
    pass
def case_3(comtacts):
    """- Prompt the user to enter a name to search for
- If a contact's name matches (case-insensitive), display their full details
- If no match is found, print a message saying the contact was not found"""
    pass
def case_4(contacts):
    """ Display all contacts in a numbered list
- Prompt the user to enter the number of the contact to delete
- Remove the selected conntact from the `contacts` list
- Print a confirmation message
- Handle the case where the user enters an invalid number"""
    
    pass


if __name__ == "__main__":
     main()
