"""
Test areas:
    1. TestItemManagement
        - add valid item, duplicate SKU accumulates quantities
        - reject zero/negative quantity and unknown SKU
        - remove and update items, including not-in-cart cases

    2. TestInventoryMocking
        - patch the inventory DB call to control stock levels
        - sufficient stock adds successfully
        - unavailable / insufficient stock raises InsufficientStockError
        - verify the inventory check is actually called

    3. TestDiscountCodes
        - valid percent and flat codes apply correctly
        - unrecognised and expired codes raise InvalidDiscountCodeError
        - removing a code clears the discount

    4. TestPricingCalculations
        - subtotal, discount amount, tax, and total against known values
        - confirm total = subtotal - discount + tax

    5. TestCheckoutAndEdgeCases
        - checkout returns a summary dict with the expected keys
        - empty cart checkout raises EmptyCartError
        - clear resets both items and discount code
        - edge cases: bad quantity, item not in cart, SKU not in catalogue
"""

import unittest
from unittest.mock import patch
from cart import ShoppingCart

from cart_exceptions import CartError

from cart_exceptions import InvalidQuantityError, ItemNotFoundError, CartItemNotFoundError  # used for testing cart items from cart.py

from cart_exceptions import InsufficientStockError  # used for inventory mock tests

from cart_exceptions import InvalidDiscountCodeError

from cart_exceptions import EmptyCartError

from inventory import InventoryService



class TestItemManagement(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_valid_item(self):
        """
        add item --> see if the actual is matching the expected
        """
        self.cart.add_item("SKU-001", 2)
        items = self.cart.get_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["quantity"], 2)

    def test_add_invalid_item(self):
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item("SKU-001", 0)
    
    def test_item_does_not_exist(self):
        with self.assertRaises(ItemNotFoundError):
            self.cart.add_item("SKU-999", 1)
    
    def test_add_existing_item_quantity(self):
        self.cart.add_item("SKU-001", 2)
        self.cart.add_item("SKU-001", 6)

        items = self.cart.get_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["quantity"], 8)

    def test_remove_cart_item(self):
        self.cart.add_item("SKU-001", 2)
        self.cart.remove_item("SKU-001")
        
        items = self.cart.get_items()
        self.assertEqual(len(items), 0)
    
    def test_remove_item_not_in_cart(self):
        self.cart.add_item("SKU-001", 2)
        with self.assertRaises(CartItemNotFoundError):
            self.cart.remove_item("SKU-002")

    def test_update_quantity_success(self):
        self.cart.add_item("SKU-001", 2)
        self.cart.update_quantity("SKU-001", 10)

        items = self.cart.get_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["quantity"], 10)

    def test_update_quantity_not_in_cart(self):
        self.cart.add_item("SKU-001", 2)
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity("SKU-999", 6)
    
    def test_update_invalid(self):
        self.cart.add_item("SKU-001", 2)
        with self.assertRaises(InvalidQuantityError):
            self.cart.update_quantity("SKU-001", -1)


class TestInventoryMocking(unittest.TestCase):
    """
    The `ShoppingCart` relies on `InventoryService` to check stock levels before 
    allowing items to be added. In a production environment this service would make 
    a live call to an external inventory database — something unit tests must never 
    depend on. Your job is to read `cart.py` and `inventory.py`, understand the call 
    chain between `ShoppingCart` and `InventoryService`, determine the appropriate method 
    to patch to take control of it.

    - Simulate sufficient stock being available and verify the item is added successfully
    - Simulate stock being unavailable and verify the correct exception is raised
    - Simulate the inventory service returning a lower stock level than the requested 
      quantity
    - Verify that the mocked method you patched is actually called when `add_item` is 
      invoked (use `assert_called_with` or `assert_called_once`)


    """
    def setUp(self):
        self.cart = ShoppingCart()


    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_tem_with_sufficient_stock(self, mock_query):
        mock_query.return_value = 100

        self.cart.add_item("SKU-001", 5)

        items = self.cart.get_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["quantity"], 5)

    
    @patch.object(InventoryService, "_query_inventory_db")
    def test_item_stock_unavailable(self, mock_query):
        mock_query.return_value = 0

        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-001", 5)


    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item_insufficient_stock(self, mock_query):
        mock_query.return_value = 2

        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-001", 5)

    
    @patch.object(InventoryService, "_query_inventory_db")
    def test_inventory_method_called(self, mock_query):
        mock_query.return_value = 100
        self.cart.add_item("SKU-001", 5)

        mock_query.assert_called_once_with("SKU-001")


class TestDiscountCodes(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    """
    Write tests covering the full range of discount code behaviour: 
        - valid percentage-based codes
        - valid flat-rate codes
        - unrecognised codes
        - expired codes
        - removal of an applied code
        - Verify that discount amounts are calculated correctly against known subtotals
    """

    def test_valid_percent_code(self):
        self.cart.add_item("SKU-001", 2)
        self.cart.apply_discount_code("SAVE10")

        self.assertEqual(self.cart.get_discount_amount(), 10.0)

    def test_valid_flat_rate_codes(self):
        self.cart.add_item("SKU-001", 2)
        self.cart.apply_discount_code("FLAT15")

        # self.assertEqual(self.cart.get_subtotal(), 99.98)
        self.assertEqual(self.cart.get_discount_amount(), 15.0)

    def test_unrecognized_codes(self):
        self.cart.add_item("SKU-001", 2)

        with self.assertRaises(InvalidDiscountCodeError):
            self.cart.apply_discount_code("SOMECODE")


    def test_expired_discount_code(self):
        self.cart.add_item("SKU-001", 5)

        with self.assertRaises(InvalidDiscountCodeError):
            self.cart.apply_discount_code("EXPIRED50")

    def test_remove_applied_code(self):
        self.cart.add_item("SKU-001", 2)
        self.cart.apply_discount_code("FLAT15")
        self.assertEqual(self.cart.get_discount_amount(), 15.0)

        self.cart.remove_discount_code()
        self.assertEqual(self.cart.get_discount_amount(), 0.0)
    

class TestPricingCalculations(unittest.TestCase):
    """
    Write tests that verify 
        `get_subtotal`
        `get_discount_amount`
        `get_tax`
        `get_total`
    
    Include a test that confirms the total is correctly computed as `subtotal - discount + tax`.

    """

    def setUp(self):
        self.cart = ShoppingCart()
        self.cart.add_item("SKU-001", 2)   # 2 × 49.99 Electronics
        self.cart.add_item("SKU-004", 1)   # 1 × 24.99 Home Office


    def test_valid_subtotal(self):
        self.assertEqual(self.cart.get_subtotal(), 124.97)
    
    def test_discount_amount(self):
        self.cart.apply_discount_code("SAVE20")
        self.assertEqual(self.cart.get_discount_amount(), 24.99)

    def test_tax_amount(self):
        self.assertEqual(self.cart.get_tax(), 9.50)
    
    def test_total_amount(self):
        self.cart.apply_discount_code("SAVE20")
        self.assertEqual(self.cart.get_total(), 109.48)

    def test_total_is_correctly_calculated(self):
        """
        total = subtotal - discount + tax
        """
        self.cart.apply_discount_code("SAVE20")

        expected = (self.cart.get_subtotal() - self.cart.get_discount_amount() + self.cart.get_tax())

        self.assertEqual(self.cart.get_total(), round(expected, 2))


class TestCheckoutAndEdgeCases(unittest.TestCase):
    """
    - Checking out a populated cart returns a summary dict containing all required keys
    - Checking out an empty cart raises `EmptyCartError`
    - Calling `clear` resets all items and the discount code
    - Adding an item with a zero or negative quantity raises `InvalidQuantityError`
    - Removing or updating an item that is not in the cart raises `CartItemNotFoundError`

    - Adding a SKU that does not exist in the product catalogue raises `ItemNotFoundError`
    """

    def setUp(self):
        self.cart = ShoppingCart()

    def test_checkout_summary(self):
        self.cart.add_item("SKU-001", 2)   # 2 × 49.99 Electronics
        self.cart.add_item("SKU-004", 1)   # 1 × 24.99 Home Office

        summary = self.cart.checkout()

        self.assertIn("subtotal", summary)
        self.assertIn("total", summary)
        self.assertIn("items", summary)

        self.assertEqual(summary["item_count"], 3)

    def test_checking_out_empty_cart(self):
        with self.assertRaises(EmptyCartError):
            self.cart.checkout()
    

    def test_clearing_cart(self):
        self.cart.add_item("SKU-001", 2)   # 2 × 49.99 Electronics
        self.cart.add_item("SKU-004", 1)   # 1 × 24.99 Home Office
        self.cart.apply_discount_code("SAVE20")

        items = self.cart.get_items()
        self.assertEqual(len(items), 2)
        self.assertEqual(self.cart.get_discount_amount(), 24.99)

        self.cart.clear()

        items = self.cart.get_items()
        self.assertEqual(len(items), 0)
        self.assertEqual(self.cart.get_discount_amount(), 0.0)


    def test_adding_zero_quantity_items(self):
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item("SKU-001", 0)

    
    def test_adding_negative_quantity_items(self):
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item("SKU-001", -5)

    def test_remove_item_not_in_cart(self):
        self.cart.add_item("SKU-001", 2)
        with self.assertRaises(CartItemNotFoundError):
            self.cart.remove_item("SKU-005")
    
    def test_update_item_not_in_cart(self):
        self.cart.add_item("SKU-001", 2)
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity("SKU-005", 7)
    
    def test_add_invalid_item(self):
        with self.assertRaises(ItemNotFoundError):
            self.cart.add_item("SKU-324", 10)

    







if __name__ == "__main__":
    unittest.main()
