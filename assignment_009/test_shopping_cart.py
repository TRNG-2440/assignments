import unittest
from unittest.mock import patch, MagicMock
from cart import ShoppingCart
from cart_exceptions import *
from pricing import PricingService

### 1. Item Management

### Write tests that verify the behaviour of `add_item`, `remove_item`, and `update_quantity`. 
# Your tests should confirm that items are correctly added to the cart, 
# that quantities accumulate when the same SKU is added more than once, 
# and that remove and update operations behave correctly for both valid and invalid inputs.


class ItemManagement(unittest.TestCase):

    def setUp(self):
        # Makes a new cart before every test!
        self.cart = ShoppingCart()
    
    def test_add(self):

        # Checks if the Notebooks appear in the cart after being added
        self.cart.add_item("SKU-005",)

        self.assertEqual(self.cart.get_items(), [{
                "sku": "SKU-005",
                "name": "Notebook (Pack of 3)",
                "unit_price": 12.99,
                "quantity": 1,
                "category": "Stationery",
            }])
        
        items_list = self.cart.get_items()
        
        self.assertTrue(any(item['sku'] == "SKU-005" for item in items_list))

        # Checks that adding 2 notebooks actually addes two notebooks
        self.cart.add_item("SKU-005", 2)

        # After our addition, we should have 3 entries of SKU-005
        self.assertEqual(self.cart.get_items(), [{
                "sku": "SKU-005",
                "name": "Notebook (Pack of 3)",
                "unit_price": 12.99,
                "quantity": 3,
                "category": "Stationery",
            }])
        
    def test_remove(self):
        self.cart.add_item("SKU-005")

        # Again, check if the item got added
        items_list = self.cart.get_items()
        
        self.assertTrue(any(item['sku'] == "SKU-005" for item in items_list))

        self.cart.remove_item("SKU-005")

        # If remove works the cart will have no items
        self.assertEqual(self.cart.get_items(), [])

        # If we try to remove again an error should be raised
        with self.assertRaises(CartItemNotFoundError):
             self.cart.remove_item("SKU-005")

    def test_update(self):
        self.cart.add_item("SKU-005")

        self.cart.update_quantity("SKU-005", 10)    
        # If update worked, we should see 10 items!
        self.assertEqual(self.cart.get_item_count(), 10)

        # Error testing!  This one ensures incorrect SKUs are handled correctly
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity("SKU-999", 3)

        # Ensures negative numbers are handled correctly
        with self.assertRaises(InvalidQuantityError):
            self.cart.update_quantity("SKU-005", -8)

class InventoryChecks(unittest.TestCase):
        
    # This patch ensures inventory service will be replaced with our mock
    @patch('cart.InventoryService')
    def test_stock(self, mock_inventory_service):

        # In our cart, self._inventory is declared with InventoryService()
        mock_inventory_instance = mock_inventory_service.return_value

        # get_stock is used in add_item checks, so lets make get_stock return 10
        mock_inventory_instance.get_stock.return_value = 10


        self.cart = ShoppingCart()

        self.cart.add_item('SKU-001', 10)   

        # Tests if we have 10 items
        self.assertEqual(self.cart.get_item_count(), 10)

        # Tests if going 1 over the stock limit raises an error
        with self.assertRaises(InsufficientStockError):
            self.cart.add_item('SKU-001', 1)  

        # Double checks if get_stock of my mock inventory was called when I input 'SKU-001'
        mock_inventory_instance.get_stock.assert_called_with('SKU-001')

        # Lets see what happens if an item is simply out of stock or not in the catalogue (which SKU-999 is not)!
        with self.assertRaises(ItemNotFoundError):
            self.cart.add_item('SKU-999', 1)

### 3. Discount Codes
#Write tests covering the full range of discount code behaviour: valid percentage-based codes, 
# valid flat-rate codes, unrecognised codes, expired codes, and the removal of an applied code. 
# Verify that discount amounts are calculated correctly against known subtotals.
# DISCOUNT_CODES = {
#     "SAVE10":    {"type": "percent", "value": 10,    "expires": date(2099, 12, 31)},
#     "SAVE20":    {"type": "percent", "value": 20,    "expires": date(2099, 12, 31)},
#     "FLAT5":     {"type": "flat",    "value": 5.00,  "expires": date(2099, 12, 31)},
#     "FLAT15":    {"type": "flat",    "value": 15.00, "expires": date(2099, 12, 31)},
#     "EXPIRED50": {"type": "percent", "value": 50,    "expires": date(2000, 1, 1)},
# }
# Discount codes for reference

class DiscountChecks(unittest.TestCase):
    def setUp(self):
        self.pricer = PricingService()
        self.cart = ShoppingCart()

    def test_codes(self):

        #SAVE10 should apply a percentage discount of 10%
        self.assertEqual(self.pricer.apply_discount(10.10, "SAVE10"), 9.09)

        # SAVE20 should give a different result
        self.assertNotEqual(self.pricer.apply_discount(10.10, "SAVE20"), 9.09)

        self.assertEqual(self.pricer.apply_discount(10.10, "SAVE20"), 8.08)

        # Now we test flat codes!
        self.assertEqual(self.pricer.apply_discount(4, "FLAT5"), 0)

        self.assertEqual(self.pricer.apply_discount(22.10, "FLAT15"), 7.10)

        # And test if codes are currently seen as invalid
        with self.assertRaises(InvalidDiscountCodeError) as ee:
            self.pricer.apply_discount(12, "EXPIRED20")

    def test_code_application(self):

        # Lets see if invalid codes are handled correctly!
        with self.assertRaises(InvalidDiscountCodeError) as ie:
            self.pricer.apply_discount(124, "TOTALLYLEGITCODESAVE100")

        # Checks if a discount code was applied
        self.cart.apply_discount_code("SAVE20")

        self.assertEqual(self.cart._discount_code, "SAVE20")

        # Checks if a discount code was removed
        self.cart.remove_discount_code()

        self.assertIsNone(self.cart._discount_code)

### 4. Pricing and Tax Calculations
#Write tests that verify `get_subtotal`, `get_discount_amount`, `get_tax`, and `get_total` 
# return the correct values for a known cart configuration. Use a cart with a fixed set of 
# items so that expected values can be calculated and hardcoded in your assertions. 
# Include a test that confirms the total is correctly computed as `subtotal - discount + tax`.
class PricingChecks(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

        # These items should be worth $639.86

        self.cart.add_item("SKU-001", 5)
        self.cart.add_item("SKU-002",6)
        self.cart.add_item("SKU-006", 3)

    def test_pricing(self):

        self.assertEqual(self.cart.get_subtotal(), 639.86)
        # Should have 0 discount before we apply the code!

        self.assertEqual(self.cart.get_discount_amount(), 0)
        self.cart.apply_discount_code("SAVE20")

        
        # 20% of 639.86 is 127.97 when rounded
        self.assertEqual(self.cart.get_discount_amount(), 127.97)

        # (459.89 * .08 <- tax rate for electronics) + (179.97 * .06 <- rate for office) 
        # = 47.59 which should be our tax amount!  
        self.assertEqual(self.cart.get_tax(), 47.59)

        # All in all, our total should be 559.48 (639.86 - 127.97) + 47.59
        self.assertEqual(self.cart.get_total(), 559.48)

    def tearDown(self):
        self.cart.clear()



### 5. Checkout and Edge Cases
# Write tests for the `checkout` method and the following edge cases:
# - Checking out a populated cart returns a summary dict containing all required keys
# - Checking out an empty cart raises `EmptyCartError`
# - Calling `clear` resets all items and the discount code
# - Adding an item with a zero or negative quantity raises `InvalidQuantityError`
# - Removing or updating an item that is not in the cart raises `CartItemNotFoundError`
# - Adding a SKU that does not exist in the product catalogue raises `ItemNotFoundError`
class CheckoutChecks(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    # Tests if a summary dictionary is returned!
    def test_summary(self):
        self.cart.add_item("SKU-001", 5)
        self.cart.add_item("SKU-002",6)
        self.cart.add_item("SKU-006", 3)

        self.assertIsInstance(self.cart.checkout(), dict)
        # These are the keys the result dictionary should have
        cart_keys = ["customer_id", "timestamp", "items", "subtotal", "discount_code", "discount_amount", "tax", "total", "item_count"]
        self.assertEqual(list(self.cart.checkout().keys()), cart_keys)       


    # Empty cart should give emptycarterror (remember setup made a fresh and empty cart!)
    def test_empty(self):
        with self.assertRaises(EmptyCartError):
            self.cart.checkout()

        # Add items and check if the cart is full
        self.cart.add_item("SKU-001", 5)
        self.cart.add_item("SKU-002",6)
        self.cart.add_item("SKU-006", 3)
        self.cart.apply_discount_code("SAVE20")
        self.assertFalse(self.cart.is_empty())
        self.assertIsNotNone(self.cart._discount_code)

        # Tests the cart's clear method
        self.cart.clear()
        self.assertTrue(self.cart.is_empty())
        self.assertIsNone(self.cart._discount_code)

    def test_checkout_errors(self):
        # Ensures respective cart errors are raised
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item("SKU-001", -2)
            self.cart.add("SKU-002", 0)

        with self.assertRaises(CartItemNotFoundError):
            self.cart.remove_item("SKU-005")
            self.cart.update_quantity("SKU-005", 5)

        with self.assertRaises(ItemNotFoundError):
            self.cart.add_item("SKU-666")

if __name__ == '__main__':
    unittest.main()
