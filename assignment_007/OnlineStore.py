"""
In this activity, you will design and implement an inventory management system for an online store. 
You will practice core OOP concepts including:

Abstract base classes and interface design
Inheritance with specialized subclass behavior
Encapsulation and property validation
Polymorphism through shared methods with type-specific logic
Composition (a Store class that owns and manages product objects)
Exception handling for invalid inventory operations
Basic CLI interaction via a menu-driven loop

"""

from datetime import datetime
import random

# Base class
class Product:

  # Constructor
  def __init__(self, productID, name, price, stockQuantity):
    self.productID = productID
    self.name = name
    self.price = price
    self.stockQuantity = stockQuantity
  
  # Calculate price of product
  def CalculatePrice(self, quantity) -> int:

    if quantity > self.stockQuantity:
      raise ValueError(f'\nError - Quantity cannot exceed stock quantity of {self.stockQuantity}\n\nPlease re-enter option\n\n')

    return (self.price * quantity)
  
  # Display product details
  def Display(self):

    # Display criteria
    print(f'\n------- {self.name} -------\n')
    print(f'Product ID: {self.productID}')
    print(f'Stock Quantity: {self.stockQuantity}')
    print(f'Price: {self.price:.2f}')
  
# -------------------------------------------------------------------------------------
# Physical product class
class PhysicalProduct(Product):

  def __init__(self, productID, name, price, stockQuantity, weight, pricePerWeight):
    super().__init__(productID, name, price, stockQuantity)

    self.weight = weight

    self.pricePerWeight = pricePerWeight

  # Calculate shipping cost
  def CalculateShipping(self, quantity) -> int:
    return self.weight * self.pricePerWeight * quantity
  
  # Calculate total cost
  def CalculatePrice(self,quantity) -> int:

    if quantity > self.stockQuantity:
      raise ValueError(f'\nError - Quantity cannot exceed stock quantity of {self.stockQuantity}\n\nPlease re-enter option\n\n')

    return self.CalculateShipping(quantity) + (self.price * quantity)
  
  # Display product details
  def Display(self):

    # Display criteria
    super().Display()

    # Print weight
    print(f"Weight (LB's) {self.weight}")
  
# -------------------------------------------------------------------------------------
# Digital Product class
class DigitalProduct(Product):

  def __init__(self, productID, name, price, stockQuantity, fileSize, url):

    super().__init__(productID, name, price, stockQuantity)

    self.fileSize = fileSize

    self.url = url

  # Determine total price
  def CalculatePrice(self, quantity) -> int:
    return (self.price * quantity)
  
  # Determine shipping
  def CalculateShipping(self, quantity) -> int:
    return 0
  
   # Display product details
  def Display(self):

    # Display criteria
    super().Display()

    print(f'File Size: {self.fileSize}')

    print(f'Url: {self.url}')

# -------------------------------------------------------------------------------------
# Perishable Product class
class PerishableProduct(Product):

  def __init__(self, productID, name, price, stockQuantity, expirationDate):

    super().__init__(productID, name, price, stockQuantity)

    self.expirationDate = datetime.strptime(expirationDate, "%Y-%m-%d")

  # Check if product is expired on today's date
  def isExpired(self) -> bool:
     return datetime.today().date() > self.expirationDate.date()
  
  # Calculate shipping cost
  def CalculateShipping(self, quantity) -> int:

    # Declare flat rate
    FLAT_RATE = 5.99

    # if total exceed $25 shipping cost is $0.00
    if (self.price * quantity) > 25:
      return 0.00
    
    return FLAT_RATE
  
  # Display perishable product information
  def Display(self):

    # Execute base class Display() function
    super().Display()

    # Print expiration date
    print(f'Expiration Date: {self.expirationDate.strftime("%Y-%m-%d")}')
  
  # Calculate price of perishable item(s)
  def CalculatePrice(self, quantity):

    if self.isExpired():
      raise ValueError(f'\nError - Product {self.productID} has expired\n\n')
    
    return (self.price * quantity) + self.CalculateShipping(quantity)
  
  # -------------------------------------------------------------------------------------
  # Store class which contains product inventory
class Store:

  # Constructor
  def __init__(self):
    self.inventory = dict()

  # Add product to inventory
  def InsertProduct(self, product) -> None:

    # Throw exception if product is missing
    if(not product):
      raise ValueError('\nError - Product is empty.  Please re-enter\n\n')
    
    # Add product to inventory if product is found
    self.inventory[product.productID] = product
    
  # Re-stock quantity within inventory
  def RestockQuantity(self, productID, quantity)  -> None:

    # Throw exception if product is not found
    if productID not in self.inventory:
      raise ValueError("\nProduct not found\n")
      
    # Modify quantity in inventory if product is found
    self.inventory[productID].stockQuantity += quantity

  # Search for product in inventory
  def SearchProduct(self, productName)  -> None:

    # Declare bool to determine if product is found
    isFound = False

    # Traverse through each instance to determine if product is found
    for inventory in self.inventory.values():

      # If product is found display content
      if productName.lower() in inventory.name.lower():
        inventory.Display()
        isFound = True

    # Execute If product is not found 
    if not isFound:
      print(f"No products found matching {productName}")

  # Remove product
  def RemoveProduct(self, productID) -> None:

    # Throw exception if productID is not found in inventory map
    if productID not in self.inventory:
      raise ValueError(f"Error - product ID {productID} not found")

    # Remove product from inventory map
    self.inventory.pop(productID)

  # List all product in inventory
  def ListAllProducts(self) -> None:

    print('\n---------------- Products: ----------------\n')
    for product in self.inventory.values():
      product.Display()

  # Modify inventory stock once customer places order
  def ModifyStock(self, inventoryMap, productID, quantity) -> None:

    # Determine if product is perishable and has expired
    if isinstance(inventoryMap, PerishableProduct) and inventoryMap.isExpired():
      raise ValueError(f"Error - {inventoryMap.name} has expired and cannot be ordered")

    # Execute if quantity is a negative number
    if quantity <= 0:
      raise ValueError("Error - quantity must be greater than 0")

    # Execute if product is current out of stock
    if self.inventory[productID].stockQuantity == 0 and not isinstance(inventoryMap, DigitalProduct):
      raise ValueError(f"Error - {inventoryMap.name} is currently out of stock")

    # Execute if quantity exceeds stock quantity
    if not isinstance(inventoryMap, DigitalProduct):
      if quantity > inventoryMap.stockQuantity:
        raise ValueError(f"Error - {inventoryMap.name} only has {inventoryMap.stockQuantity} items left")
      
    # If product is in Digital product, deduct quantity from stock
    if not isinstance(inventoryMap, DigitalProduct):
      inventoryMap.stockQuantity -= quantity

  # Print Order
  def PrintOrder(self, inventoryMap, quantity) -> None:

    # Declare subtotal
    subtotal = inventoryMap.price * quantity

    # Declare shipping cost
    shippingCost = inventoryMap.CalculateShipping(quantity)

    # Declare total price
    total = subtotal + shippingCost

    # Display order summary
    # --------------------------------------

    print("-" * 15)

    print(f"{'\n\nORDER SUMMARY':^15}\n\n")

    print("-" * 25)

    print(f"{inventoryMap.name} x {quantity}")

    print(f"{'Unit Price:':<15} ${inventoryMap.price:.2f}")

    print(f"{'Subtotal:':<15} ${subtotal:.2f}")

    print(f"{'Shipping:':<15} ${shippingCost:.2f}")

    print(f"{'-' * 10:^20}")

    print(f"{'Total:':<15}{total:.2f}")

    print("-" * 25)

    print(f'\nOrder Placed!  Remaining stock: {inventoryMap.stockQuantity}')

  # Implement when customer places order
  def Order(self, productID, quantity) -> None:

    # Execute condition if product id is found
    if(self.inventory.get(productID)):
      inventoryMap = self.inventory[productID]

    # Display error message if product id is not found
    else:
      print(f'\n{productID} was not found\n\n')
      return
    
    # Modify inventory stock once customer places order
    self.ModifyStock(inventoryMap, productID, quantity)
    
    # Print Order
    self.PrintOrder(inventoryMap, quantity)

# -------------------------------------------------------------------------------------
# Display main menu
def MainMenu() -> str:
  while True:
    print("\n" + "-" * 20)

    print("   PyStore Inventory System")

    print("\n" + "-" * 20)

    print("[1] Manager Menu")

    print("[2] Customer Menu")

    print("[3] Quit")
    
    return input("\n> ")
# -------------------------------------------------------------------------------------
# Display manager menu
def ManagerMenu() -> str:
  while True:
    print("\n--- Manager Menu ---")

    print("[1] Add product")

    print("[2] Remove product")

    print("[3] Restock product")

    print("[4] List all inventory")

    print("[5] Back")

    return input("\n> ")

# -------------------------------------------------------------------------------------
# Display customer menu
def CustomerMenu() -> str:

  print("\n--- Customer Menu ---")

  print("[1] Browse all products")

  print("[2] Search by name")

  print("[3] Place an order")

  print("[4] Back")

  return input("\n> ")

# -------------------------------------------------------------------------------------
# Display product type
#   
def ProductTypeMenu() -> str:

  print("\nProduct type:")

  print("[1] Physical")

  print("[2] Digital")

  print("[3] Perishable")
  return input("> ")
  
# -------------------------------------------------------------------------------------
# Function designated for manager portal
def ManagerPortal(storeObj) -> None:

  while(True):

    match(ManagerMenu()):

      case "1":

        match(ProductTypeMenu()):

          case "1":

            productID = str(random.randint(1, 1000000000000))

            name = input("\nName: ")

            price = float(input("\nPrice: "))

            stockQuantity = int(input("\nStock quantity: "))

            weight = float(input("\nWeight: "))

            pricePerWeight = 0.50

            productObj = PhysicalProduct(productID, name, price, stockQuantity, weight, pricePerWeight)

          case "2":

            productID = str(random.randint(1, 1000000000000))

            name = input("\nName: ")

            price = float(input("\nPrice: "))

            stockQuantity = int(input("\nStock quantity: "))

            fileSize = input("\nFile size: ")

            url = input("\nDownload URL: ")

            productObj = DigitalProduct(productID, name, price, stockQuantity, fileSize, url)

          case "3":

            productID = str(random.randint(1, 1000000000000))

            name = input("\nName: ")

            price = float(input("\nPrice: "))

            stockQuantity = int(input("\nStock quantity: "))

            expirationDate = input("\nExpiration date (YYYY-MM-DD): ")

            productObj = PerishableProduct(productID, name, price, stockQuantity, expirationDate)

          case _:
            print('\nInvalid option - please re-enter\n')
            continue

        storeObj.InsertProduct(productObj)

        print("\nProduct added.")

      case "2":

        productID = input("\nProduct ID to remove: ")

        if(not productID):
          raise ValueError("\nError - product ID cannot be empty")

        store.RemoveProduct(productID)

        print("\nProduct removed.")

      case "3":

        productID = input("\nProduct ID to restock: ")

        quantity = int(input("\nQuantity to add: "))

        storeObj.RestockQuantity(productID, quantity)

        print("\nProduct restocked.")

      case "4":

        storeObj.ListAllProducts()

      case "5":

        print('\nNavigating back to main menu\n')

        break

      case _:

          print('\nError - Invalid option.  Please re-enter\n')
          continue



# -------------------------------------------------------------------------------------
# Function designated for customer portal
def CustomerPortal(storeObj) -> None:

  while(True):

    match(CustomerMenu()):
      case "1":

        storeObj.ListAllProducts()

      case "2":

        productName = input("\nSearch: ")

        storeObj.SearchProduct(productName)

      case "3":

        productID = input("\nProduct ID: ")

        quantity = int(input("\nQuantity: "))

        storeObj.Order(productID, quantity)

      case "4":

        print("\nNavigating back to main menu")
        break
    
      case _:

        print('\nError - Invalid option. Please re-enter\n')

        continue
# -------------------------------------------------------------------------------------

# Main function
def main():
  
  # Instantiate store object
  storeObj = Store()

  while(True):

    # Display main menu
    match(MainMenu()):

      case "1":

        # Provide features for management
        ManagerPortal(storeObj)
    
      case "2":

        # Provide features for management
        CustomerPortal(storeObj)

      case "3":

        # Exit program
        print('\nExiting program\n')

        break

      case _:
          
          # Notify user invalid option was selected
          print('\nError - Invalid option.  Please re-enter\n')
          continue


if __name__=="__main__":

  try:

    main()

  except ValueError as error:

    print(error)

  



