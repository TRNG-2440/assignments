# Mark White
# 06/12/2026
# Assignment 5

# Contact Book

# This program allows users to create a contact book where they can add, remove, and display contacts. 
# Each contact consists of a name, phone number, and email address. The program includes input validation 
# to ensure that the name contains only letters and spaces, the phone number is a 10-digit number, and 
# the email address is in a valid format. The user can also exit the program with a confirmation prompt.

import re

contacts_list = []

def add_contact(name, phone, email):
    
    
    contact = (name, phone, email)
    contacts_list.append(contact)

def remove_contact(name):
    for contact in contacts_list:
        if not contact[0] == name in contacts_list:
            print(f"\nContact {name} not found.")
            return
        if contact[0] == name:
            contacts_list.remove(contact)
            return
def display_contacts():
    for contact in contacts_list:
        name, phone, email = contact
        print(f"Name: {name}\nPhone: {phone}\nEmail: {email}\n")


def contact_book():
            while True:
                #Welcome message and menu options
                print("\n====Welcome to the Contact Book!====\n")
                try:
                    print("1. Add Contact\n2. Remove Contact\n3. Display Contacts\n4. Exit\n")

                    choice = input("Enter your choice: \n")
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if choice == '1':

                    try:
                        name = input("Enter name: ")
                        if not re.match(r"^[a-zA-Z\s]+$", name): #check if name contains only letters and spaces
                            print("Invalid name. Please enter a valid name.")
                            continue
                        phone = input("Enter phone number: ")
                        if not re.match(r"^\d{10}$", phone):  #check if phone number is 10 digits long and contains only numbers
                            print("Invalid phone number. Please enter a valid 10-digit phone number.")
                            continue
                        email = input("Enter email: ")
                        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email): #check if email is in valid format
                            print("Invalid email. Please enter a valid email address.")
                            continue
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                        continue

                    add_contact(name, phone, email)
                    print(f"\nContact {name} added successfully!")
                elif choice == '2':
                    #checks for any contacts to remove before asking for name input and displaying contact list for reference.
                    if not contacts_list:
                            print("\nNo contacts to remove.")
                            continue
                    else:
                        print("\n====Contact List====")
                        for contact in contacts_list: print("Name:{0}\n".format(contact[0]))
                    
                    name = input("Enter name to remove: ")
                    if name not in [contact[0] for contact in contacts_list]:
                        print(f"\nContact {name} not found.")
                        continue
                    if name in [contact[0] for contact in contacts_list]:
                        remove_contact(name)
                    print(f"\nContact {name} removed successfully!")
                elif choice == '3':
                    print("\n====Contact List====")
                    display_contacts()
                elif choice == '4':
                    prompt = input("Are you sure you want to exit? (yes/no): ")
                    if prompt.lower() == "yes":
                        print("Goodbye!")
                        break
                    else:
                        continue
                else:
                    print("Invalid choice. Please try again.")

if __name__ == "__main__":
    contact_book()
