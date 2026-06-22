import unittest
from unittest.mock import patch, MagicMock
from cart import ShoppingCart
from cart_exceptions import CartError
from unittest.mock import Mock
from cart_exceptions import InsufficientStockError
from cart_exceptions import InvalidDiscountCodeError
from cart_exceptions import EmptyCartError
from cart_exceptions import InvalidQuantityError
from cart_exceptions import CartItemNotFoundError
from cart_exceptions import ItemNotFoundError


# ------------------------------------------------------------------------------------
# Test cases located in cart.py used to test Item Management functionality
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

# ------------------------------------------------------------------------------------
# Test cases located in cart.py and inventory.py used to test inventory 
class TestInventory(unittest.TestCase):
  
  # Instantiate mock object each time test case is conducted
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

    # Throw assertion when 20 items of SKU-001 is added to cart 
    with self.assertRaises(InsufficientStockError):
        self.cart.add_item("SKU-001", 20)

  # Ensure input validation properly works when request quantity is greater than amount in stock
  def test_lower_stock_than_requested_quantity(self):
     
    # Call GetStock() function
    self.MockObject.get_stock.return_value = 10

    # Throw assertion when 20 items of SKU-001 is added to cart 
    with self.assertRaises(InsufficientStockError):
        self.cart.add_item("SKU-001",20)
  
  # Determine if add_item method was called
  def test_add_item_called(self):
     
     # Call add_item method
     self.MockObject.add_item("SKU-001",20)

     # Determine if add_item object was successfully called
     self.MockObject.add_item.assert_called_once()

# ------------------------------------------------------------------------------------
# Test methods located in catalogue.py and cart.py used to test discount codes
class TestDiscountCodes(unittest.TestCase): 
   
   # Instantiate cart object each time test case is conducted
   def setUp(self):
      self.cart = ShoppingCart()

   # Test percentage of discount code
   def test_percentage_of_discount_code(self):
      
      # Add item into shopping cart
      self.cart.add_item("SKU-001",1)

      # Apply discount code
      self.cart.apply_discount_code("SAVE10")

      # Execute assertion
      self.assertEqual(self.cart.get_discount_amount(), 5.00)

   # Test percentage of discount code
   def test_flat_rate_of_discount_code(self):
    
      # Add item into shopping cart
      self.cart.add_item("SKU-001",1)

      # Apply discount code
      self.cart.apply_discount_code("FLAT5")

      # Execute assertion
      self.assertEqual(self.cart.get_discount_amount(), 5.00)

   # Test for codes not currently stored in catalogue
   def test_unrecognized_codes(self):
      with self.assertRaises(InvalidDiscountCodeError):
         self.cart.apply_discount_code("LSKDFJLKDSJF")

   # Test for expired discount codes
   def test_for_expired_codes(self):
      with self.assertRaises(InvalidDiscountCodeError):
         self.cart.apply_discount_code("EXPIRED50")

    # Test for expired discount codes
   def test_for_removed_discount_code(self):

    # Add item into shopping cart
    self.cart.add_item("SKU-001",1)

    # Apply discount code
    self.cart.apply_discount_code("SAVE10")

    # Remove discount code from current item in cart
    self.cart.remove_discount_code()

    # Confirm discounted amount is equivalent to zero
    self.assertEqual(self.cart.get_discount_amount(),0.0)

# ------------------------------------------------------------------------------------
# Test pricing and tax calculations
class TestPricingAndTaxes(unittest.TestCase): 

  # Instantiate cart object each time test case is conducted
  def setUp(self):

    # Call default constructor
    self.cart = ShoppingCart()

    # Add SKU-001 into function
    self.cart.add_item("SKU-001",1)

  # Test get_subtotal() function of wireless keyboard (SKU-001)
  def test_subtotal(self):
    
    # Determine if discounted amount matches get_subtotal()
     self.assertEqual(self.cart.get_subtotal(),49.99)

  # Test discounted amount of wireless keyboard (SKU-001)
  def test_discounted_amount(self):

     # Apply discount code
     self.cart.apply_discount_code("SAVE10")

     # Determine if discounted amount matches get_discount_amount()
     self.assertEqual(self.cart.get_discount_amount(),5)

  # Test getTax() function
  def test_get_tax(self):

   # Determine if tax matches get_tax() function
   self.assertEqual(self.cart.get_tax(),4.0)

  # Test get_total() function
  def test_get_total(self):
     
   # Determine if total amount matches get_total() function
   self.assertEqual(self.cart.get_total(),53.99)

  # ------------------------------------------------------------------------------------

  # Test pricing and tax calculations
class TestCheckOutAndEdgeCases(unittest.TestCase): 

    # Instantiate cart object each time test case is conducted
    def setUp(self):

      self.cart = ShoppingCart()
      
    def test_cart(self):
        
        # Add item in cart
        self.cart.add_item("SKU-001", 1)

        # Declare summary dictionary
        summary = self.cart.checkout()

        # Declare set of keys  
        keys = {
        "customer_id",
        "timestamp",
        "items",
        "subtotal",
        "discount_code",
        "discount_amount",
        "tax",
        "total",
        "item_count",}

        # Confirms keys match
        self.assertEqual(summary.keys(),keys)

    # Test for empty cart during checkout    
    def test_empty_cart(self):

      # Confirm exception is throw when checkout is made with an empty cart
      with self.assertRaises(EmptyCartError):
         self.cart.checkout()

   # Test to confirm cart is clear
    def test_clear(self):
       
        # Add item in cart
        self.cart.add_item("SKU-001", 1)

        # Add discount
        self.cart.apply_discount_code("SAVE10")

        # Clear items
        self.cart.clear()

        # Confirm there are zero items in cart
        self.assertEqual(self.cart.get_item_count(), 0)

        # Confirm cart is empty
        self.assertTrue(self.cart.is_empty)

        # Confirm no discount is applied
        self.assertEqual(self.cart.get_discount_amount(), 0.0)

   # Test invalid quantity error
    def test_invalid_quantity_error(self):

      # Traverse from 0 to -100
      for quantity in range(0, -100, -1):
    
      # Produce subtest to prevent program from terminating after exception is throw
       with self.subTest(quantity):

         # Throw exception when a value of 0 or less than 0 is inputted as quantity
         with self.assertRaises(InvalidQuantityError):
        
          # Add item with quantity of 0 or less
          self.cart.add_item("SKU-001", quantity)

    # Remove or update item that is not in cart
    def test_removed_item_not_in_cart(self):

      # Throw exception when wireless keyboard is removed while not in cart
      with self.assertRaises(CartItemNotFoundError):

         # Remove wireless keyboard
         self.cart.remove_item("SKU-001")

      # Throw exception when wireless keyboard is updated while not in cart
      with self.assertRaises(CartItemNotFoundError):

         # Update wireless keyboard
         self.cart.update_quantity("SKU-001", 8)

    # Add non-existent SKU item 
    def test_add_nonexistent_sku(self):

      # Traverse from 0 to -100
      for i in range(9, 100):
    
       # Produce subtest to prevent program from terminating after exception is throw
       with self.subTest(i=i):

         # Throw exception when item of non-exist name is added in shopping cart
         with self.assertRaises(ItemNotFoundError):
        
          # Add item with non-exist name
          self.cart.add_item("SKU-00" + str(i), 1)











       


if __name__ == "__main__":
    unittest.main()

  # -----------------------------------------------------------

  