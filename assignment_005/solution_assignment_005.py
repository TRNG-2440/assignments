class ContactEntries:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

def PrintContacts(lst):
    print("CONTACTS:")
    for i, c in enumerate(lst):
        name, phone, email = c.name, c.phone, c.email
        print(f"{i + 1}. Name  : {name}")
        print(f"   Phone : {phone}")
        print(f"   Email : {email}")

def SortContacts(lst):
    sort_lst = sorted(lst, key=lambda l: l.name.lower())
    return sort_lst

def ContactBook():
    contacts = []

    while True:
        print("--------------------------------------")
        print("                 MENU                 ")
        print("--------------------------------------")
        print("1. Add a contact")
        print("2. View all contacts")
        print("3. View all contacts by name alphabetically")
        print("4. View all contacts by name reverse alphabetically")
        print("5. Search for a contact")
        print("6. Delete a contact")
        print("7. Edit a contact")
        print("0. Exit")
        inp = input("Choose an option to continue: ")

        match inp:
            case "1" | "1. Add a contact":
                print("--------------------------------------")
                name = input("Enter a name: ")
                phone_num = input("Enter a phone number: ")
                email = input("Enter an email address: ")
                info = ContactEntries(name, phone_num, email)
                contacts.append(info)
                print("Contact has been successfully added:", {name}, {phone_num}, {email})            
            case "2" | "2. View all contacts":
                print("--------------------------------------")
                if len(contacts) == 0: print("Contacts list is empty.")
                else: PrintContacts(contacts)
            case "3" | "3. View all contacts by name alphabetically":
                print("--------------------------------------")
                if len(contacts) == 0: print("Contacts list is empty.")
                else:
                    temp = SortContacts(contacts)
                    PrintContacts(temp)
            case "4" | "4. View all contacts by name reverse alphabetically":
                print("--------------------------------------")
                if len(contacts) == 0: print("Contacts list is empty.")
                else:
                    temp = SortContacts(contacts)
                    temp.reverse()
                    PrintContacts(temp)
            case "5" | "5. Search for a contact":
                print("--------------------------------------")
                if len(contacts) == 0: print("Contacts list is empty.")
                else:
                    search_name = input("Enter a name to search for: ").lower()
                    found = False
                    for i in contacts:
                        if search_name == i.name.lower():
                            name, phone, email = i.name, i.phone, i.email
                            print(f"Name  : {name}")
                            print(f"Phone : {phone}")
                            print(f"Email : {email}")
                            found = True
                            break
                    if not found:
                        print("No match was found. Going back to menu.")
            case "6" | "6. Delete a contact":
                print("--------------------------------------")
                if len(contacts) == 0: print("Contacts list is empty.")
                else:
                    PrintContacts(contacts)
                    search_num = input("Enter an index number to delete: ")
                    
                    # error handling
                    if not search_num.isdigit():
                        print("Invalid input. Going back to menu.")
                    else:
                        search_num = int(search_num)
                        if search_num < 1 or search_num > len(contacts):
                            print("Invalid index number. Going back to menu.")
                        else:
                            contacts.pop(search_num - 1)
                            print(f"Contact has been deleted from contacts list.") 
            case "7" | "7. Edit a contact":
                print("--------------------------------------")
                if len(contacts) == 0: print("Contacts list is empty.")
                else:
                    PrintContacts(contacts)
                    search_num = input("Enter an index number to edit: ")
                    
                    # error handling
                    if not search_num.isdigit():
                        print("Invalid input. Going back to menu.")
                    else:
                        search_num = int(search_num)
                        if search_num < 1 or search_num > len(contacts):
                            print("Invalid index number. Going back to menu.")
                        else:
                            name = input("Enter a name: ")
                            phone_num = input("Enter a phone number: ")
                            email = input("Enter an email address: ")
                            info = ContactEntries(name, phone_num, email)
                            contacts[search_num - 1] = info
                            print("Contact has been successfully changed:", {name}, {phone_num}, {email})
            case "0" | "0. Exit":
                print("--------------------------------------")
                print("Exiting menu.")
                print("--------------------------------------")
                break

ContactBook()