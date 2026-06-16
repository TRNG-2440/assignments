#Assignment 9- Unit Testing for Shopping Cart System
#Alex Tran

import unittest
from unittest.mock import patch, MagicMock

from cart import ShoppingCart 
from inventory import InventoryService
from pricing import PricingService

from cart_exceptions import (
    CartError, 
    ItemNotFoundError, 
    InsufficientStockError, 
    InvalidQuantityError, 
    InvalidDiscountCodeError, 
    EmptyCartError, 
    CartItemNotFoundError
)

class TestItemManagement(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()
    
    def test_add_item_successfully(self):
        self.cart.add_item("SKU-001", 2)
        items = self.cart.get_items()

        #check that all the values are equal
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["sku"], "SKU-001")
        self.assertEqual(items[0]["quantity"], 2)
        self.assertEqual(items[0]["unit_price"], 49.99)
    
    def test_add_same_item_twice_accumulates(self):

        self.cart.add_item("SKU-001", 2)
        self.cart.add_item("SKU-001", 3)
        
        items = self.cart.get_items()

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["quantity"], 5)

    def test_remove_item_successfully(self):
        self.cart.add_item("SKU-002", 3)

        self.cart.remove_item("SKU-002")
        self.assertTrue(self.cart.is_empty())

    def test_remove_item_not_in_cart_error(self):
        with self.assertRaises(CartItemNotFoundError):
            self.cart.remove_item("SKU-001")
        

    def test_update_cart_number_successfully(self):
        self.cart.add_item("SKU-001", 2)

        self.cart.update_quantity("SKU-001", 5)

        items = self.cart.get_items()
        self.assertEqual(items[0]["quantity"], 5)
    
    def test_update_item_not_in_cart(self):
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity("SKU-001", 2)
    
    def test_add_zero_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item("SKU-001", 0)
    
    def test_add_invalid_sku(self):
        with self.assertRaises(ItemNotFoundError):
            self.cart.add_item("SKU-999", 1)


#Tests for Inventory Checks with Mocking

class TestInventoryChecks(unittest.TestCase):
    
    def setUp(self):
        self.cart = ShoppingCart()
    
    @patch.object(InventoryService, "get_stock")
    def test_add_item_sufficient_stock(self, mock_get_stock):
        mock_get_stock.return_value = 10

        self.cart.add_item("SKU-001", 2)
        items = self.cart.get_items()
        self.assertEqual(items[0]["quantity"], 2)
        mock_get_stock.assert_called_once_with("SKU-001")
    
    @patch.object(InventoryService, "get_stock")
    def test_add_item_insufficient_stock(self, mock_get_stock):
        mock_get_stock.return_value = 1

        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-001", 2)

    @patch.object(InventoryService, "get_stock")
    def test_add_item_exceeds_stock(self, mock_get_stock):
        mock_get_stock.return_value = 6

        self.cart.add_item("SKU-001", 2)
        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-001", 6)

class TestDiscountCode(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

        self.cart.add_item("SKU-001", 2) #price = 49.99 *2 = 99.98

    def test_valid_percent_discount(self):
        self.cart.apply_discount_code("SAVE10")

        self.assertEqual(self.cart.get_discount_amount(), 10.00)
    
    def test_valid_flat_five(self):
        self.cart.apply_discount_code("FLAT5")
        self.assertEqual(self.cart.get_discount_amount(), 5.00)
    
    def test_valid_remove_discount(self):
        self.cart.apply_discount_code("SAVE10")
        self.cart.remove_discount_code()
        self.assertEqual(self.cart.get_discount_amount(), 0.00)
    
    def test_invalid_discount(self):
        with self.assertRaises(InvalidDiscountCodeError):
            self.cart.apply_discount_code("ABCDXYZ")
    
    def test_expired_discount(self):
        with self.assertRaises(InvalidDiscountCodeError):
            self.cart.apply_discount_code("EXPIRED50")

class TestPricingAndTaxCalculations(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()
        self.cart.add_item("SKU-001", 2) #pricing is  $49.99 * 2 = $99.98
        self.cart.add_item("SKU-004", 1) #pricing is $24.99 * 1 = $24.99
    
    def test_get_subtotal(self):
        self.assertEqual(self.cart.get_subtotal(), 124.97)

    def test_get_tax(self):

        #Electronics: 99.98 * .08 = 8.00
        #Home Office: 24.99 * .06 = 1.50
        #Total Tax: 8.00 + 1.50 = 9.50

        self.assertEqual(self.cart.get_tax(), 9.50)

    def test_get_discount_amount(self):
        self.cart.apply_discount_code("SAVE10")

        self.assertEqual(self.cart.get_discount_amount(), 12.50)

    def test_get_total(self):
        self.cart.apply_discount_code("SAVE10")

        #Calculations:
        #124.97 - 12.50 + 9.50 = 121.97

        self.assertEqual(self.cart.get_total(), 121.97 )



#testing checkout behavior and edge cases
#checkout returns a summary dictionary and returns an error if the cart is empty
class TestCheckoutEdgeCases(unittest.TestCase):
    
    def setUp(self):
        self.cart = ShoppingCart(customer_id = "customer-678")
        

    def test_populated_cart(self):
        self.cart.add_item("SKU-002", 2)
        summary = self.cart.checkout()

        self.assertIn("customer_id", summary)
        self.assertIn("timestamp", summary)
        self.assertIn("items", summary)
        self.assertIn("subtotal", summary)
        self.assertIn("discount_amount", summary)
        self.assertIn("discount_code", summary)
        self.assertIn("tax", summary)
        self.assertIn("total", summary)
        self.assertIn("item_count", summary)


        self.assertEqual(summary["customer_id"], "customer-678" )
        self.assertEqual(summary["item_count"], 2)

    def test_empty_cart_error(self):
        with self.assertRaises(EmptyCartError):
            self.cart.checkout()

    def test_clear_items_and_discounts(self):
        self.cart.add_item("SKU-006", 1)
        self.cart.apply_discount_code("SAVE10")

        #clear the cart and check afterwards that it is empty and the discount code has been removed
        self.cart.clear()

        self.assertTrue(self.cart.is_empty())
        self.assertEqual(self.cart.get_discount_amount(), 0) 

    def  test_negative_quantity_to_cart(self):
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item("SKU-002", -5)
    
    def test_update_missing_item(self):
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity("SKU-004", 2)
           
    def test_remove_missing_item(self):
        with self.assertRaises(CartItemNotFoundError):
            self.cart.remove_item("SKU-004")

    def test_add_invalid_sku(self):
        with self.assertRaises(ItemNotFoundError):
            self.cart.add_item("SKU-456", 2)        


if __name__ == "__main__":
    unittest.main()
    