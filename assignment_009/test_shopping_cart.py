import unittest
from unittest.mock import Mock, patch, MagicMock
from cart import ShoppingCart
from pricing import PricingService
from inventory import InventoryService
import cart_exceptions as ce


class ItemManagementTestCase(unittest.TestCase):
    def setUp(self):
        self.sku = ["SKU-000", "SKU-001", "SKU-003", "SKU-004"]
        self.test_cart = ShoppingCart()

    def tearDown(self):
        return super().tearDown()
    
    # ======================================================
    # add_item TESTING
    # ======================================================
    def test_add_item(self):
        self.test_cart.add_item(self.sku[1], 1)
        result = self.test_cart._items[self.sku[1]]["quantity"]
        self.assertEqual(result, 1)

        self.test_cart.add_item(self.sku[1], 1)
        result = self.test_cart._items[self.sku[1]]["quantity"]
        self.assertEqual(result, 2)

    def test_add_item_InvalidQuantityError(self):
        self.assertRaises(ce.InvalidQuantityError, self.test_cart.add_item, self.sku[1], 0)

    def test_add_item_ItemNotFoundError(self):
        self.assertRaises(ce.ItemNotFoundError, self.test_cart.add_item, self.sku[0], 1)

    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item_InsufficientStockError(self, mock_inventory):
        mock_inventory.return_value = 0
        self.assertRaises(ce.InsufficientStockError, self.test_cart.add_item, self.sku[2], 1)
        mock_inventory.assert_called_once_with(self.sku[2])

    # ======================================================
    # remove_item TESTING
    # ======================================================

    def test_remove_item(self):
        sku = self.sku[1]
        self.test_cart._items[sku] = {
            "sku": sku,
            "name": "Wireless Keyboard",
            "price": 49.99,
            "quantity": 1,
            "category": "Electronics",
        }

        self.test_cart.remove_item(sku)
        self.assertEqual(len(self.test_cart._items), 0)

    def test_remove_item_CartItemNotFoundError(self):
        sku = self.sku[1]
        self.assertRaises(ce.CartItemNotFoundError, self.test_cart.remove_item, sku)

    @patch.object(InventoryService, "_query_inventory_db")
    def test_update_quantity(self, mock_inv):
        sku = self.sku[1]
        qty = 2
        mock_inv.return_value = 10
        self.test_cart._items[sku] = {
            "sku": sku,
            "name": "Wireless Keyboard",
            "price": 49.99,
            "quantity": 1,
            "category": "Electronics",
        }
        self.test_cart.update_quantity(sku, qty)
        result = self.test_cart._items[sku]["quantity"]
        self.assertEqual(result, qty)
        mock_inv.assert_called_once_with(sku)

    def test_update_quantity_CartItemNotFoundError(self):
        sku = self.sku[3]
        qty = 2
        self.test_cart._items[self.sku[1]] = {
            "sku": self.sku[1],
            "name": "Wireless Keyboard",
            "price": 49.99,
            "quantity": 1,
            "category": "Electronics",
        }
        self.assertRaises(ce.CartItemNotFoundError, self.test_cart.update_quantity, sku, qty)

    def test_update_quantity_InvalidQuantityError(self):
        sku = self.sku[1]
        qty = 0
        self.test_cart._items[sku] = {
            "sku": sku,
            "name": "Wireless Keyboard",
            "price": 49.99,
            "quantity": 1,
            "category": "Electronics",
        }
        self.assertRaises(ce.InvalidQuantityError, self.test_cart.update_quantity, sku, qty)

    @patch.object(InventoryService, "_query_inventory_db")
    def test_update_quantity_InsufficientStockError(self, mock_inv):
        sku = self.sku[1]
        qty = 5
        self.test_cart._items[sku] = {
            "sku": sku,
            "name": "Wireless Keyboard",
            "price": 49.99,
            "quantity": 1,
            "category": "Electronics",
        }
        mock_inv.return_value = 2
        self.assertRaises(ce.InsufficientStockError, self.test_cart.update_quantity, sku, qty)
        mock_inv.assert_called_once_with(sku)



class InventoryMockingTestCase(unittest.TestCase):
    def setUp(self):
        self.test_cart = ShoppingCart()

    def tearDown(self):
        return super().tearDown()
    
class DiscountCodeTestCase(unittest.TestCase):
    def setUp(self):
        self.test_cart = ShoppingCart()

    def tearDown(self):
        return super().tearDown()
    
class PriceAndTaxTestCase(unittest.TestCase):
    def setUp(self):
        self.test_cart = ShoppingCart()

    def tearDown(self):
        return super().tearDown()
    
class CheckoutTestCase(unittest.TestCase):
    def setUp(self):
        self.test_cart = ShoppingCart()

    def tearDown(self):
        return super().tearDown()

if __name__ == "__main__":
    unittest.main()