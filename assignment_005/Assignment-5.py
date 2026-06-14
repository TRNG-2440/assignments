contacts = []

while True:

    choose = input('''
════════════════════════════════════════
Contact Book
════════════════════════════════════════
1. Add a contact
2. View all contacts
3. Search for a contact
4. Delete a contact
0. Exit
════════════════════════════════════════      
Select an option!
''')
    
    match choose:
        case "1":
            name = input("Please enter a name: ")
            phone = input("Please give a phone number: ")
            email = input("Please provide an email address: ")

            contacts.append((name, phone, email))
        case "2":
            if not contacts:
                print("Your phonebook is empty!  Get some friends")

            else:
                print("Here is your phonebook:\n")
                for i, (n, p, e) in enumerate(contacts):
                    
                    print(f"{i + 1}. [Name]: {n} [Phone Number]: {p} [E-mail]: {e}")
        case "3":
            search = input("Search for a contact's name!")

            results = [t for t in contacts if search.lower() in t[0].lower()]
            if not results:
                print("No results found!")
            
            else:
                print("Matches:")
                for r in results:
                    print(r)

        case "4":
            if not contacts:
                print("You have no contacts to delete!")
            
            else:
                for i, (n, p, e) in enumerate(contacts):
                    print(f"{i + 1}. Name: {n} Phone Number: {p} E-mail: [e]")

                remove = int(input("Type the number of the contact you want gone!"))


                try:
                    temp = contacts.pop(remove - 1)
                    print(f"Successfully removed {temp} from your contacts!")
                except:
                    print("Invalid number entered")
        case "0":
            print("See ya later alligator!")
            break

        case _:
            print("I can't understand whatever you are saying")
