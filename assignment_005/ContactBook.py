"""
Build a console-based Contact Book that stores contacts 
as tuples and holds them in a list. The user can add contacts, 
view all contacts, search for a contact by name, and delete a contact. 
This activity focuses on **tuples** and **lists together**, and practices 
tuple packing, tuple unpacking, `for` loops, `while` loops, `if-elif-else`, and `input()`.

"""

# ---------------------------------------------------
# Display menu for user
def Menu() -> None:

  print("\n     Contact Book"\
  "\n----------------------------"\
  '\n1. Add a contact'\
  '\n2. View all contacts'\
  '\n3. Search for a contact'\
  '\n4. Delete a contact'
  '\n0. Exit\n')

# ---------------------------------------------------
# Display search option for user
def SearchMenu() -> str:
  print('\n--------- Search Contact ---------\n' \
  '1) Name       2) Phone Number\n\n' \
  '3) Email      4) Exit\n\n')

  # Return option
  return (input('Input option: '))

# ---------------------------------------------------
# Display search option for user
def DeleteMenu() -> str:
  print('\n--------- Delete Contact ---------\n' \
  '1) Name       2) Phone Number\n\n' \
  '3) Email      4) Exit\n\n')

  # Return option
  return (input('Input option: '))

# ---------------------------------------------------
# Select option
def Select() -> str:
   
   # Display menu
   Menu()

   # Return option
   return (input('Input option: '))
    
# ---------------------------------------------------
# Add a contact
def AddContact() -> tuple:

  print("\n----------------------------"\
  "\n     Add Contact"\
  "\n----------------------------\n")

  name = input('Input name: ').strip()

  if not name:
    raise ValueError('\nError - name cannot be empty, please re-enter\n')
  
  phone = input('\nInput phone #: ').strip()

  if not phone:
    raise ValueError('\nError - phone # cannot be empty, please re-enter\n')
  
  email = input('\nInput email address: ').strip()

  if not email:
    raise ValueError('\nError - email address cannot be empty, please re-enter\n')

  return (name, phone, email)

# ---------------------------------------------------
# Display all contacts
def ViewContacts(contactList) -> None:

  if not contactList:
    print('\nNo contacts found')

  else:
    print("\n------------------------------"\
  "\n     All Contacts"\
  "\n------------------------------\n")
    
    for i, (name,phone,email) in enumerate(contactList):
      print(f'{i+1}. Name : {name}\n'\
            f'{i+2}. Phone : {phone}\n'\
            f'{i+3}. Email : {email}\n')
      print('-----------------------------')

# ---------------------------------------------------
# Search for contact
def SearchContact(contactList):

  match SearchMenu():

      case "1":
            
            # Declare boolean to determine if desired result is found
            isFound = False

            # Prompt user input
            userName = input('\nInput user name: ').strip()
            
            # Confirm option
            option = input('\nAre you sure you want to continue (Y/N)? ').strip()

            if option.lower() == 'y':
                
                for name, phone, email in contactList:
                    if name.lower() == userName.lower():
                      print(f"\n------------------------------\n"
                            f"Name  : {name}\n"
                            f"Phone : {phone}\n"
                            f"Email : {email}\n"
                            f"------------------------------")

                      isFound = True

                if not isFound:
                    print("\n\nContact not found.\n")

            elif option.lower() == 'n':
                print('\nReturning to menu\n')

            else:
                print('\nInvalid option\n')

      case "2":
            
            # Declare boolean to determine if desired result is found
            isFound = False

            # Prompt user input
            userPhoneNumber = input('\nInput user phone #: ').strip()
            option = input('\nAre you sure you want to continue (Y/N)? ').strip()

            if option.lower() == 'y':
              for name, phone, email in contactList:
                if phone == userPhoneNumber:
                  print(
                    f"\n------------------------------\n"
                    f"Name  : {name}\n"
                    f"Phone : {phone}\n"
                    f"Email : {email}\n"
                    f"------------------------------")
                  isFound = True

                if not isFound:
                    print("\nContact not found.\n")

            elif option.lower() == 'n':
                print('\nReturning to menu\n')

            else:
                print('\nInvalid option\n')

      case "3":
            
            # Declare boolean to determine if desired result is found
            isFound = False

            # Prompt user input
            userEmail = input('\nInput user email: ').strip()

            # Confirm option
            option = input('\nAre you sure you want to continue (Y/N)? ').strip()

            if option.lower() == 'y':
                for name, phone, email in contactList:
                    if email.lower() == userEmail.lower():
                      print(
                      f"\n------------------------------\n"
                      f"Name  : {name}\n"
                      f"Phone : {phone}\n"
                      f"Email : {email}\n"
                      f"------------------------------")

                      isFound = True

                if not isFound:
                    print("\nContact not found.\n")

            elif option.lower() == 'n':
                print('\nReturning to menu\n')

            else:
                print('\nInvalid option\n')

      case "4":
            print('\nExiting menu')

# ---------------------------------------------------
# Delete a specific contact
def DeleteContact(contactList):

  match DeleteMenu():
     
      case "1":
            
            # Index used to delete option
            index = 0
            
            # Declare boolean to determine if desired result is found
            isFound = False

            # Prompt user input
            userName = input('\nInput user name: ').strip()
            
            # Confirm option
            option = input('\nAre you sure you want to continue (Y/N)? ').strip()

            if option.lower() == 'y':
                tempName = ""
                for i, (name, phone, email) in enumerate(contactList):
                    if name.lower() == userName.lower():
                      index = i
                      isFound = True
                      tempName = name
                      break

                if(isFound):
                  contactList.pop(index)
                  print(f'\n{tempName} was sucessfully deleted\n\n' )

                else:
                  print("\nContact not found.\n")

            elif option.lower() == 'n':
                print('\nReturning to menu\n')

            else:
                print('\nInvalid option\n')

      case "2":
            
            # Declare boolean to determine if desired result is found
            isFound = False

            # Prompt user input
            userPhoneNumber = input('\nInput user phone #: ').strip()
            option = input('\nAre you sure you want to continue (Y/N)? ').strip()

            if option.lower() == 'y':
              tempPhone = ""
              for i, (name, phone, email) in enumerate(contactList):
                    if phone.lower() == userPhoneNumber.lower():
                      index = i
                      isFound = True
                      tempPhone = phone
                      break

              if(isFound):
                contactList.pop(index)
                print(f'\n{tempPhone} was sucessfully deleted\n\n' )

              else:
                  print("\nContact not found.\n")

            elif option.lower() == 'n':
                print('\nReturning to menu\n')

            else:
                print('\nInvalid option\n')

      case "3":
            
            # Declare boolean to determine if desired result is found
            isFound = False

            # Prompt user input
            userEmail = input('\nInput user email: ').strip()

            # Confirm option
            option = input('\nAre you sure you want to continue (Y/N)? ').strip()

            if option.lower() == 'y':
              tempEmail = ""
              for i, (name, phone, email) in enumerate(contactList):
                    if email.lower() == userEmail.lower():
                      index = i
                      isFound = True
                      tempEmail = email
                      break

              if(isFound):
                contactList.pop(index)
                print(f'\n{tempEmail} was sucessfully deleted\n\n' )

              else:
                print("\nContact not found.\n")

            elif option.lower() == 'n':
                print('\nReturning to menu\n')

            else:
                print('\nInvalid option\n')

      case "4":
            print('\nExiting menu')

# ---------------------------------------------------

def main():
    
  # Declare list
  contactList =  []

  while(True):

    try:

      match(Select()):
         

        case "0":
            
          # Print exit message
          print("\nProgram has been terminated.\n")

          print("Goodbye!\n")

          # Terminate program
          break

        case "1":
          
          # Formulate tuple and list
          contactList.append(AddContact())

        case "2": 

          # View all contact information
          ViewContacts(contactList)

        case "3": 

          # Search for specific criteria
          SearchContact(contactList)

        case "4": 

          # Delete a specific contact
          DeleteContact(contactList)

        case _:

           # Alert user that invalid entry was enter
          print('\nInvalid entry - please re-enter option')

    except ValueError as error:
      print(error)

if __name__=="__main__":
  main()