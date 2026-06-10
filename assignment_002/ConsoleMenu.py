""" Activity 2 — Console Menu Selection System """

# Main menu
def Menu():
  print('\n-------------- Menu --------------\n' \
  '1) Electronics       2) Clothing\n\n' \
  '3) Food              4) Exit\n\n')

# Electronics menu
def ElectronicsMenu():
  print('\n-------------- Menu --------------\n' \
  '1) Computer              2) Hard Drive\n\n' \
  '3) TV                    4) Headphones\n\n' \
  '5) Back\n\n')

# Clothing menu
def ClothingMenu():
  print('\n-------------- Menu --------------\n' \
  '1) Sweater              2) Jacket\n\n' \
  '3) Shirt                4) Shoes\n\n' \
  '5) Pants                6) Back\n\n')

# Food menu
def FoodMenu():
  print('\n-------------- Menu --------------\n' \
  '1) Taco              2) Burrito\n\n' \
  '3) Vampiro           4) Sopa\n\n' \
  '5) Mulita            6) Back\n\n')
  
# Source code
while(True):

# Display Menu
  Menu()
  
  selection = input(f'Input Selection: ')

  # Display list based on user's selection
  match selection:

    case "1":

      while(True):
      
      # Display electronics menu
        ElectronicsMenu()

        while(True):

          isTerminate = False

          selection = input(f'Input Selection: ')

          match selection:

            case "1": 
              print('Name: Computer\n\n'\
                  'Price: $1,000\n\n'\
                  'Quantity: 1,000\n\n'\
                  'Inventory: In stock\n')
              break 
            
            case "2": 
              print('Name: Hard drive\n\n'\
                  'Price: $1,000\n\n'\
                  'Quantity: 570\n\n'\
                  'Inventory: In stock\n')
            
              break 
          
            case "3": 
              print('Name: TV\n\n'\
                  'Price: $300\n\n'\
                  'Quantity: 200\n\n'\
                  'Inventory: Out of stock\n')
            
              break 
          
            case "4": 
              print('Name: Head phones\n\n'\
                  'Price: $50\n\n'\
                  'Quantity: 300\n\n'\
                  'Inventory: In stock\n')
            
              break 

            case "5": 
              print('\nRedirecting back to main menu\n')
              isTerminate = True
              break 

        if(isTerminate == True):
          break

  
  # ----------------------------------------------------------------

    case "2":

      while(True):
      
       # Display clothing menu
        ClothingMenu()

        while(True):

          isTerminate = False

          selection = input(f'Input Selection: ')

          match selection:

            case "1": 
              print('\nName: Sweater\n\n'\
                  'Price: $700\n\n'\
                  'Quantity: 20\n\n'\
                  'Inventory: In stock\n')
              break 
            
            case "2": 
              print('\nName: Jacket\n\n'\
                  'Price: $150\n\n'\
                  'Quantity: 51\n\n'\
                  'Inventory: Out of stock\n')
            
              break 
          
            case "3": 
              print('\nName: Shirt\n\n'\
                  'Price: $20\n\n'\
                  'Quantity: 200\n\n'\
                  'Inventory: In stock\n')
            
              break 
          
            case "4": 
              print('\nName: Shoes\n\n'\
                  'Price: $220\n\n'\
                  'Quantity: 10\n\n'\
                  'Inventory: In stock\n')
              
              break 
              
            case "5": 
              print('\nName: Pants\n\n'\
                  'Price: $120\n\n'\
                  'Quantity: 15\n\n'\
                  'Inventory: In stock\n')
            
              break 

            case "6": 
              print('\nRedirecting back to main menu\n')
              isTerminate = True
              break 

            case _:
                # Alert user that invalid entry was enter
                print('\nInvalid entry - please re-enter option')

                break 

          if(isTerminate == True):
            break

  # ----------------------------------------------------------------

    case "3":

      while(True):
      
       # Display food menu
        FoodMenu()

        while(True):

          isTerminate = False

          selection = input(f'Input Selection: ')

          match selection:

            case "1": 
              print('\nName: Taco\n\n'\
                  'Price: $8\n\n'\
                  'Quantity: 20\n\n'\
                  'Inventory: In stock\n')
              break 
            
            case "2": 
              print('\nName: Burrito\n\n'\
                  '\nPrice: $10\n\n'\
                  '\nQuantity: 51\n\n'\
                  '\nInventory: In stock\n')
            
              break 
          
            case "3": 
              print('\nName: Vampiro\n\n'\
                  '\nPrice: $10\n\n'\
                  '\nQuantity: 100\n\n'\
                  '\nInventory: In stock\n')
            
              break 
          
            case "4": 
              print('\nName: Sopa\n\n'\
                  '\nPrice: $8\n\n'\
                  '\nQuantity: 10\n\n'\
                  '\nInventory: In stock\n')
              
              break 
              
            case "5": 
              print('\nName: Mulita\n\n'\
                  '\nPrice: $10\n\n'\
                  '\nQuantity: 16\n\n'\
                  '\nInventory: In stock\n')
            
              break 

            case "6": 
              print('\nRedirecting back to main menu\n')
              isTerminate = True

              break
              
            case _:
                # Alert user that invalid entry was enter
                print('\nInvalid entry - please re-enter option')

                break 

        if(isTerminate == True):
          break

  # ----------------------------------------------------------------

    case "4":

    # Alert user that program is exiting
      print('\nExiting\n')
      
      break

    case _:
    
    # Alert user that invalid entry was enter
      print('\nInvalid entry - please re-enter option')

   
  

        
    


