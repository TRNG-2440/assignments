import unittest
from unittest.mock import patch, MagicMock
from cart import ShoppingCart
from inventory import InventoryService
from cart_exceptions import (
    InvalidQuantityError,
    ItemNotFoundError,
    InsufficientStockError,
    CartItemNotFoundError,
    InvalidDiscountCodeError,
    EmptyCartError
)

class TestItemManagement(unittest.TestCase):
    def setUp(self):
        self.shopping = ShoppingCart()

    # VALID: adding a new item that exists and is in stock
    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item(self, mock_query):
        mock_query.return_value = 50
        self.shopping.add_item("SKU-001", 2)
        self.assertEqual(self.shopping._items["SKU-001"]["quantity"], 2)

    # VALID: adding another item that is in cart that exists and is in stock
    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item_accum(self, mock_query):
        mock_query.return_value = 50
        self.shopping.add_item("SKU-001", 2)
        self.shopping.add_item("SKU-001", 1)
        self.assertEqual(self.shopping._items["SKU-001"]["quantity"], 3)
    
    # add item exceptions, no item
    def test_add_item_not_found(self):
        with self.assertRaises(ItemNotFoundError):
            self.shopping.add_item("random string", 1)

    # add item exceptions, bad quantity 
    def test_add_item_invalid_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            self.shopping.add_item("SKU-001", -1)
    
    # add item exceptions, low stock
    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item_insufficient_stock(self, mock_query):
        mock_query.return_value = 2
        with self.assertRaises(InsufficientStockError):
            self.shopping.add_item("SKU-001", 1000)

    # add item exceptions, no stock
    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item_no_stock(self, mock_query):
        mock_query.return_value = 0
        with self.assertRaises(InsufficientStockError):
            self.shopping.add_item("SKU-001", 1000)

    # VALID: remove item from cart
    def test_remove_item(self):
        self.shopping._items["SKU-001"] = {
            "quantity": 2
        }
        self.shopping.remove_item("SKU-001")
        self.assertNotIn("SKU-001", self.shopping._items)

    # remove item exception, no item
    def test_remove_item_cart_not_found(self):
        with self.assertRaises(CartItemNotFoundError):
            self.shopping.remove_item("random string")

    # VALID: update quantity
    @patch.object(InventoryService, "_query_inventory_db")
    def test_update_quantity(self, mock_query):
        mock_query.return_value = 50
        self.shopping._items["SKU-001"] = {
            "quantity": 2
        }
        self.shopping.update_quantity("SKU-001", 3)
        self.assertEqual(self.shopping._items["SKU-001"]["quantity"], 3)

    # update quantity exceptions, no item
    def test_update_quantity_cart_not_found(self):
        with self.assertRaises(CartItemNotFoundError):
            self.shopping.update_quantity("random string", 1)

    # update quantity exceptions, bad quantity
    def test_update_quantity_invalid_quantity(self):
        self.shopping._items["SKU-001"] = {
            "quantity": 2
        }
        with self.assertRaises(InvalidQuantityError):    
            self.shopping.update_quantity("SKU-001", -1)

    # update quantity exceptions, low stock
    @patch.object(InventoryService, "_query_inventory_db")
    def test_update_quantity_insufficient_stock(self, mock_query):
        mock_query.return_value = 50
        self.shopping._items["SKU-001"] = {
            "quantity": 2
        }
        with self.assertRaises(InsufficientStockError):    
            self.shopping.update_quantity("SKU-001", 1000)

    # update quantity exceptions, no stock
    @patch.object(InventoryService, "_query_inventory_db")
    def test_update_quantity_no_stock(self, mock_query):
        mock_query.return_value = 0
        self.shopping._items["SKU-001"] = {
            "quantity": 2
        }
        with self.assertRaises(InsufficientStockError):    
            self.shopping.update_quantity("SKU-001", 1000)   

class TestInventoryService(unittest.TestCase):
    def setUp(self):
        self.shopping = ShoppingCart()

    # VALID: adding a new item that exists and is in stock
    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item(self, mock_query):
        mock_query.return_value = 50
        self.shopping.add_item("SKU-001", 2)
        self.assertEqual(self.shopping._items["SKU-001"]["quantity"], 2)
        mock_query.assert_called_once_with("SKU-001")

    # add item exceptions, low stock
    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item_insufficient_stock(self, mock_query):
        mock_query.return_value = 2
        with self.assertRaises(InsufficientStockError):
            self.shopping.add_item("SKU-001", 1000)
        mock_query.assert_called_once_with("SKU-001")

    # add item exceptions, no stock
    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item_no_stock(self, mock_query):
        mock_query.return_value = 0
        with self.assertRaises(InsufficientStockError):
            self.shopping.add_item("SKU-001", 1000)
        mock_query.assert_called_once_with("SKU-001")   

class TestDiscountCodes(unittest.TestCase):
    def setUp(self):
        self.shopping = ShoppingCart()

    # VALID: apply percent discount
    def test_get_discount_percent(self):
        self.shopping._items["SKU-001"] = {
            "quantity": 2,
            "unit_price": 49.99
        }
        self.shopping.apply_discount_code("SAVE10")
        self.assertEqual(self.shopping.get_discount_amount(), 10.00)

    # VALID: get flat discount
    def test_get_discount_flat(self):
        self.shopping._items["SKU-001"] = {
            "quantity": 2,
            "unit_price": 49.99
        }
        self.shopping.apply_discount_code("FLAT5")
        self.assertEqual(self.shopping.get_discount_amount(), 5.00)

    # VALID: discount ends up being under 0
    def test_apply_discount_under_zero(self):
        self.shopping._items["SKU-001"] = {
            "quantity": 1,
            "unit_price": 49.99
        }
        self.shopping.apply_discount_code("FLAT15")
        self.assertEqual(self.shopping.get_discount_amount(), 15.00)

    # VALID: get discount, no discount
    def test_get_discount_none(self):
        self.shopping._items["SKU-001"] = {
            "quantity": 2,
            "unit_price": 49.99
        }
        self.assertEqual(self.shopping.get_discount_amount(), 0.00)

    # apply discount exceptions, invalid
    def test_apply_discount_invalid(self):
        with self.assertRaises(InvalidDiscountCodeError):
            self.shopping.apply_discount_code("random string")

    # apply discount exceptions, expired
    def test_apply_discount_expired(self):
        with self.assertRaises(InvalidDiscountCodeError):
            self.shopping.apply_discount_code("EXPIRED50")

    # VALID: remove discount
    def test_remove_discount(self):
        self.shopping.apply_discount_code("SAVE10")
        self.shopping.remove_discount_code()
        self.assertIsNone(self.shopping._discount_code)

class TestPricingTaxCalc(unittest.TestCase):
    def setUp(self):
        self.shopping = ShoppingCart()
        self.shopping._items["SKU-001"] = {
                "sku": "SKU-001",
                "quantity": 2,
                "unit_price": 49.99
            }
        self.shopping._items["SKU-004"] = {
            "sku": "SKU-004",
            "quantity": 2,
            "unit_price": 24.99
        }

    def test_get_subtotal(self):
        self.assertEqual(self.shopping.get_subtotal(), 149.96)

    def test_get_discount_percent(self):
        self.shopping.apply_discount_code("SAVE20")
        self.assertEqual(self.shopping.get_discount_amount(), 29.99)
        
    def test_get_tax(self):
        self.assertEqual(self.shopping.get_tax(), 11.00)

    def test_get_total(self):
        self.shopping.apply_discount_code("SAVE20")
        self.assertEqual(self.shopping.get_total(), 130.97)

class TestCheckoutEdgeCases(unittest.TestCase):
    def setUp(self):
        self.shopping = ShoppingCart()

    # VALID: checkout with 2 items
    def test_checkout(self):
        self.shopping._items["SKU-003"] = {
            "sku": "SKU-003",
            "name": "Ergonomic Mouse",
            "unit_price": 39.99,
            "quantity": 2,
            "category": "Electronics"
        }
        
        self.shopping.apply_discount_code("SAVE20")
        order = self.shopping.checkout()

        self.assertIsInstance(order, dict)
        self.assertIn("customer_id", order)
        self.assertIn("timestamp", order)
        self.assertIn("items", order)
        self.assertIn("subtotal", order)
        self.assertIn("discount_code", order)
        self.assertIn("discount_amount", order)
        self.assertIn("tax", order)
        self.assertIn("total", order)
        self.assertIn("item_count", order)

        self.assertEqual(order["items"], {"SKU-003": {"sku": "SKU-003", "name": "Ergonomic Mouse", "unit_price": 39.99, "quantity": 2, "category": "Electronics"}})
        self.assertEqual(order["subtotal"], 79.98)
        self.assertEqual(order["discount_code"], "SAVE20")
        self.assertEqual(order["discount_amount"], 16.00)
        self.assertEqual(order["tax"], 6.40)
        self.assertEqual(order["total"], 70.38)
        self.assertEqual(order["item_count"], 2)

    # checkout exception, empty cart
    def test_empty_cart(self):
        with self.assertRaises(EmptyCartError):
            self.shopping.checkout()

    # VALID: clear cart
    def test_clear(self):
        self.shopping._items["SKU-001"] = {
            "quantity": 2
        }
        self.shopping._items["SKU-002"] = {
            "quantity": 5
        }
        self.shopping.apply_discount_code("SAVE10")
        self.shopping.clear()
        self.assertEqual(self.shopping._items, {})
        self.assertIsNone(self.shopping._discount_code)

    # add item exceptions, no item
    def test_add_item_not_found(self):
        with self.assertRaises(ItemNotFoundError):
            self.shopping.add_item("random string", 1)

    # add item exceptions, bad quantity 
    def test_add_item_invalid_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            self.shopping.add_item("SKU-001", -1)
    
    # add item exceptions, low stock
    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item_insufficient_stock(self, mock_query):
        mock_query.return_value = 2
        with self.assertRaises(InsufficientStockError):
            self.shopping.add_item("SKU-001", 1000)

    # add item exceptions, no stock
    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item_no_stock(self, mock_query):
        mock_query.return_value = 0
        with self.assertRaises(InsufficientStockError):
            self.shopping.add_item("SKU-001", 1000)