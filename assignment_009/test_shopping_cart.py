# libraries
import unittest
from unittest.mock import patch, MagicMock
from cart import ShoppingCart
from cart_exceptions import CartError, ItemNotFoundError, InsufficientStockError, InvalidDiscountCodeError, InvalidQuantityError, EmptyCartError, CartItemNotFoundError

# tests for item management
class TestItemManagement(unittest.TestCase):
    # setup 
    def setUp(self):
        # create ShoppingCart object for tests
        self.cart = ShoppingCart()
    # ============================================================
    # ADDING ITEMS
    # add_item
    def test_add_item_valid(self):
        self.cart.add_item("SKU-001", 2)
        items = self.cart.get_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["sku"], "SKU-001")
        self.assertEqual(items[0]["name"], "Wireless Keyboard")
        self.assertEqual(items[0]["unit_price"], 49.99)
        self.assertEqual(items[0]["category"], "Electronics")
    
    # add_item using default quanitity
    def test_add_item_valid_default_quantity(self):
        self.cart.add_item("SKU-002")
        items = self.cart.get_items()
        self.assertEqual(self.cart.get_item_count(), 1)

    # add_item with resused SKUs for correct quantity
    def test_add_item_duplicate_skus_accumulate(self):
        self.cart.add_item("SKU-002", 2)
        self.cart.add_item("SKU-002", 3)
        items = self.cart.get_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["quantity"], 5)
    
    # add_item with SKU with invalid quantity
    def test_add_item_bad_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item("SKU-001", 0)

    # add_item with SKU not in catalogue
    def test_add_item_bad_sku(self):
        with self.assertRaises(ItemNotFoundError):
            self.cart.add_item("SKU-999")
    
    # add_item with not enough stock 
    def test_add_item_insufficient_stock(self):
        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-003")

    # ============================================================
    # REMOVING ITEMS
    # remove_item
    def test_remove_one_item(self):
        self.cart.add_item("SKU-001", 1)
        self.cart.remove_item("SKU-001")
        items = self.cart.get_items() # should be empty dict
        self.assertEqual(len(items), 0)

    # remove_item with multiple items added first
    def test_remove_multiple_items_in_cart(self):
        self.cart.add_item("SKU-001")
        self.cart.add_item("SKU-002")
        items = self.cart.get_items() # len 2 right now
        self.assertEqual(len(items), 2)
        self.cart.remove_item("SKU-001")
        new_items = self.cart.get_items() # should be len 1 now
        self.assertEqual(len(new_items), 1)
    
    # remove_item but with sku not in cart
    def test_remove_item_bad_sku(self):
        self.cart.add_item("SKU-001")
        self.assertRaisesRegex(CartItemNotFoundError, "SKU 'SKU-002' is not in the cart.", self.cart.remove_item, "SKU-002")
    
    # ============================================================
    # UPDATING QUANTITY
    # normal amount
    def test_update_quantity(self):
        self.cart.add_item("SKU-001", 2)
        self.cart.update_quantity("SKU-001", 5) 
        items = self.cart.get_items()
        self.assertEqual(items[0]["quantity"], 5)
    
    # item not in cart 
    def test_update_quantity_not_in_cart(self):
        self.cart.add_item("SKU-007", 3)
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity("SKU-001", 10)
    
    # invalid quantity
    def test_update_quantity_invalid_quantity(self):
        self.cart.add_item("SKU-008", 2)
        with self.assertRaises(InvalidQuantityError):
            self.cart.update_quantity("SKU-008", -1)
    
    # insufficient stock
    def test_update_quantity_insuff_stock(self):
        self.cart.add_item("SKU-006", 1)
        with self.assertRaises(InsufficientStockError):
            self.cart.update_quantity("SKU-006", 20)
