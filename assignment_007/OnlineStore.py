"""
Python Coding Activity 7 - Online Store Inventory System
Objective
In this activity, you will design and implement an inventory management system for an online store. You will practice core OOP concepts including:

Abstract base classes and interface design
Inheritance with specialized subclass behavior
Encapsulation and property validation
Polymorphism through shared methods with type-specific logic
Composition (a Store class that owns and manages product objects)
Exception handling for invalid inventory operations
Basic CLI interaction via a menu-driven loop
Instructions
You will build an inventory system that supports three types of products: Physical, Digital, and Perishable. Each product type shares a common interface but has unique behaviors and attributes.

Create a base Product class that holds common attributes such as product ID, name, price, and stock quantity. It should support a method to display product details and a method to calculate a total price for a given quantity.

Create a PhysicalProduct subclass with the following unique behavior:

Has a weight attribute (in kg or lbs) used to calculate a shipping cost. Shipping cost should scale with weight.
Overrides the total price calculation to include the calculated shipping cost.
Create a DigitalProduct subclass with the following unique behavior:

Has a file size attribute and a download URL.
Has no shipping cost — its total price is always just the item price.
Stock is not limited in the traditional sense; purchasing a digital product does not reduce available stock.
Create a PerishableProduct subclass with the following unique behavior:

Has an expiration date attribute.
Includes a method to check if the product is expired based on today's date. You will need to import the datetime module.
Expired products cannot be added to a customer order.
Has a flat-rate shipping cost applied to all orders. However, if the pre-shipping order total exceeds $25.00, shipping is free.
Create a Store class that manages the full product inventory. It should support:

Adding a new product of any supported type to the inventory
Removing a product by ID
Restocking an existing product (increasing its quantity)
Searching for products by name (partial matches count)
Listing all in-stock products
Create a simple Order system — when a customer places an order, the store should:

Verify the product exists and is in stock (and not expired, if perishable)
Deduct the appropriate quantity from inventory (except for digital products)
Return an order summary with the total cost including any applicable shipping
Build a CLI menu loop that lets the user interact with the store as either a store manager (add, remove, restock products) or a customer (browse, search, and place orders).

Example Interaction
==============================
   PyStore Inventory System
==============================

[1] Manager Menu
[2] Customer Menu
[3] Quit

> 1

--- Manager Menu ---
[1] Add product
[2] Remove product
[3] Restock product
[4] List all inventory
[5] Back

> 1

Product type:
[1] Physical
[2] Digital
[3] Perishable
> 3

Name: Organic Strawberries
Price: 4.99
Stock quantity: 30
Expiration date (YYYY-MM-DD): 2025-06-15

Perishable product added.
   ID: PRD-0041  |  Organic Strawberries  |  $4.99  |  Expires: 2025-06-15

------------------------------

> 2

--- Customer Menu ---
[1] Browse all products
[2] Search by name
[3] Place an order
[4] Back

> 2
Search: straw

Results:
  [PRD-0041]  Organic Strawberries  |  $4.99  |  In Stock: 30  |  Expires: 2025-06-15

> 3
Product ID: PRD-0041
Quantity: 5

==============================
         Order Summary
==============================
  Organic Strawberries x5
  Unit Price : $4.99
  Subtotal   : $24.95
  Shipping   : $3.99  (flat-rate)
  ---------------------
  Total      : $28.94
==============================
Order placed! Remaining stock: 25

------------------------------

> 3
Product ID: PRD-0041
Quantity: 6

==============================
         Order Summary
==============================
  Organic Strawberries x6
  Unit Price : $4.99
  Subtotal   : $29.94
  Shipping   : $0.00  (free over $25)
  ---------------------
  Total      : $29.94
==============================
Order placed! Remaining stock: 19

------------------------------

> 3
Product ID: PRD-0041
Quantity: 2

Error: Organic Strawberries has expired and cannot be ordered.
NOTE: The example above is for illustrative purposes - either the order would succeed, or it would fail for expired products, not both.

Requirements Checklist
 A base Product class exists with shared attributes and a price calculation method
 PhysicalProduct calculates shipping cost based on weight and includes it in the total
 DigitalProduct has no shipping cost and its stock is unaffected by purchases
 PerishableProduct stores an expiration date and correctly identifies expired products
 PerishableProduct applies a flat-rate shipping cost to all orders
 PerishableProduct shipping is waived when the pre-shipping order total exceeds $25.00
 Expired PerishableProduct items are blocked from being ordered
 A Store class manages a collection of products and supports add, remove, restock, and search
 Product IDs are auto-generated and unique
 Searching by name supports partial, case-insensitive matches
 Placing an order correctly deducts stock (except for digital products)
 Orders for out-of-stock items are rejected with a clear error message
 Orders for quantities exceeding available stock are rejected
 Restocking a non-existent product ID raises an appropriate error
 Removing a product that does not exist raises an appropriate error
 The CLI handles invalid input (bad product IDs, non-numeric quantities, invalid dates) without crashing
 Each product type overrides the detail display method to show its unique attributes
Stretch Goals
Discount System — Add a apply_discount(percent) method to the base Product class that temporarily reduces a product's price. Add a manager menu option to apply a store-wide sale to all products of a given type.

Persistence — Save and load the full inventory to/from a JSON file so product data survives between sessions. You will need to handle serialization carefully to preserve each subclass's unique attributes and restore the correct type on load.

Expiration Sweep — Add a manager menu option that scans the inventory and automatically removes all expired PerishableProduct items, printing a report of what was removed.

Order History — Track all placed orders in memory with a timestamp, product name, quantity, and total cost. Add a customer menu option to view past orders from the current session.

Low Stock Alerts — After every order or restock operation, check if any product's stock has fallen below a defined threshold (e.g. 5 units) and print a warning to the manager view.

"""

from datetime import datetime


# -------------------------------------------------------------------------------------
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
    print(f'Price: {self.price}')
  
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
    print(f'\n------- {self.name} -------\n')
    super().Display()
    print(f'Weight: {self.weight}')
  
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
    print(f'\n------- {self.name} -------\n')
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

    if (self.price * quantity) > 25:
      return 0.00
    
    return FLAT_RATE
  
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
    self.inventory[product.productID] = product
    
  # Re-stock quantity within inventory
  def RestockQuantity(self, productID, quantity)  -> None:

    if productID not in self.inventory:
          print("Product not found")
          return

    self.inventory[productID].stockQuantity += quantity

  # Search for product in inventory
  def SearchProduct(self, productID)  -> None:

    if productID in self.inventory:
          dictionary = self.inventory[productID]

          print("Product found\n")
          print(f"Product: {dictionary.productID}")
          print(f"Quantity: {dictionary.stockQuantity}")

    else:
        print(f"{productID} is not found")

  # Remove product
  def RemoveProduct(self, productID) -> None:

    # Throw exception if productID is not found in inventory map
    if productID not in self.inventory:
      raise ValueError(f"Error - product ID {productID} not found")

    # Remove product from inventory map
    self.inventory.pop(productID)

  # List all product in inventory
  def ListAllProducts(self) -> None:

    print('\n---------------- Products: ----------------\n\n')
    for key, value in self.inventory.items():
      print(f'Product: {key} | Quantity: {value}\n')

  # Implement when customer places order
  def Order(self, productID, quantity) -> None:

    if(self.inventory.get(productID)):
      inventoryMap = self.inventory[productID]
    else:
      print(f'\n{productID} was not found\n\n')
      return
    
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

    # Display order summary
    print("-" * 15)
    print(f"{'\n\nORDER SUMAMARY':^15}\n\n")
    print("-" * 25)
    print(f"{inventoryMap.name} x {quantity}")
    print(f"{'Unit Price:':<15}{inventoryMap.price}")
    print(f"{'Subtotal:':<15}{inventoryMap.CalculatePrice(quantity)}")
    print(f"{'Shipping:':<15}{inventoryMap.CalculateShipping(quantity)}")
    print(f"{'-' * 10:^20}")
    print(f"{'Total:':<15}{inventoryMap.CalculateShipping(quantity)} + {inventoryMap.CalculatePrice(quantity)}")
    print("-" * 25)
    print(f'\nOrder Placed!  Remaining stock: {inventoryMap.stockQuantity}')


# -------------------------------------------------------------------------------------

  



