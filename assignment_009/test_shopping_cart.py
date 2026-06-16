import unittest
from unittest.mock import patch, MagicMock
from cart import ShoppingCart
from inventory import InventoryService
from cart_exceptions import (
    InvalidQuantityError,
    ItemNotFoundError,
    InsufficientStockError,
    CartItemNotFoundError,
    InvalidDiscountCodeError
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
        self.assertEqual(self.shopping._items["SKU-001"]["quantity"], 5)

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
            "unit_price": 50.00
        }
        self.shopping.apply_discount_code("SAVE10")
        self.assertEqual(self.shopping.get_discount_amount(), 10.00)

    # VALID: get flat discount
    def test_get_discount_flat(self):
        self.shopping._items["SKU-001"] = {
            "quantity": 2,
            "unit_price": 50.00
        }
        self.shopping.apply_discount_code("FLAT5")
        self.assertEqual(self.shopping.get_discount_amount(), 5.00)

    # VALID: discount ends up being under 0
    def test_apply_discount_under_zero(self):
        self.shopping._items["SKU-001"] = {
            "quantity": 1,
            "unit_price": 10.00
        }
        self.shopping.apply_discount_code("FLAT15")
        self.assertEqual(self.shopping.get_discount_amount(), 10.00)

    # VALID: get discount, no discount
    def test_get_discount_none(self):
        self.shopping._items["SKU-001"] = {
            "quantity": 2,
            "unit_price": 50.00
        }
        self.assertEqual(self.shopping.get_discount_amount(), 0.0)

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

class TestCheckoutEdgeCases(unittest.TestCase):
    def setUp(self):
        self.shopping = ShoppingCart()
    