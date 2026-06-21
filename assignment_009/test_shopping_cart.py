import unittest
from unittest.mock import patch, MagicMock
from cart import ShoppingCart
from cart_exceptions import CartError
from unittest.mock import Mock
from cart_exceptions import InsufficientStockError

# Test methods located in cart.py
class TestItemManagement(unittest.TestCase):
  
  # Instantiate cart object each time test case is conducted
  def setUp(self):
        self.cart = ShoppingCart()

  # -----------------------------------------------------------
  # Unit test - determines if use can add item to cart
  def test_add_cart(self):
      
      # Add wireless keyboard (SKU-001) to inventory multiple times
      self.cart.add_item("SKU-001",4)

      self.cart.add_item("SKU-001",4)

      self.cart.add_item("SKU-001",4)

      # Ensure wireless keyboard is found in dictionary
      self.assertIn("SKU-001", self.cart._items)

      # Ensure the quantity is correct
      self.assertEqual(self.cart._items["SKU-001"]["quantity"],12)

  # -----------------------------------------------------------
  # Unit test - determines if item has been successfully removed from cart
  def test_remove_from_cart(self):
      
      # Add wireless keyboard (SKU-001) to inventory
      self.cart.add_item("SKU-001",10)

      # Remove a quantity of 4 wireless keyboard (SKU-001) from inventory
      self.cart.remove_item("SKU-001")

      # Ensure the quantity is correct
      self.assertNotIn("SKU-001",self.cart._items)

  # -----------------------------------------------------------

  # Unit test - determines if item quantity has been successfully updated
  def test_update_cart(self):
      
      # Add wireless keyboard (SKU-001) to inventory
      self.cart.add_item("SKU-001",15)

      # Add wireless keyboard (SKU-001) to inventory
      self.cart.update_quantity("SKU-001",10)

      # Ensure wireless keyboard is found in dictionary
      self.assertIn("SKU-001", self.cart._items)

      # Ensure the quantity is correct
      self.assertEqual(self.cart._items["SKU-001"]["quantity"],10)

  # -----------------------------------------------------------

# Test methods located in cart.py and inventory.py
class TestInventory(unittest.TestCase):
  
  def setUp(self):

    # Instantiate mock object
    self.MockObject = Mock()

    # Instantiate shopping cart object
    self.cart = ShoppingCart(inventory_service=self.MockObject)

  # Determine if there is a sufficient stock
  def test_sufficient_stock(self):

    # Call GetStock() function
    self.MockObject.get_stock.return_value = 50

    # Add item into cart
    self.cart.add_item("SKU-001", 5)

    # Determine if item is currently in cart
    self.assertIn("SKU-001", self.cart._items)

  # Ensure input validation properly works when item is out of stock 
  def test_no_stock_available(self):

    # Call GetStock() function
    self.MockObject.get_stock.return_value = 0

    # Add item into cart
    with self.assertRaises(InsufficientStockError):
        self.cart.add_item("SKU-001", 20)

  # Ensure input validation properly works when request quantity is greater than amount in stock
  def test_lower_stock_than_requested_quantity(self):
     
    # Call GetStock() function
    self.MockObject.get_stock.return_value = 10

    # Add item into cart
    with self.assertRaises(InsufficientStockError):
        self.cart.add_item("SKU-001",20)
  
  # Determine if add_item method was called
  def test_add_item_called(self):
     
     # Call add_item method
     self.MockObject.add_item("SKU-001",20)

     # Determine if add_item object was successfully called
     self.MockObject.add_item.assert_called_once()

     




     


    
      
if __name__ == "__main__":
    unittest.main()

  # -----------------------------------------------------------

  