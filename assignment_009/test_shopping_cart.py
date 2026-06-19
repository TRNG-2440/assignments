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

    # ======================================================
    # update_quantity TESTING
    # ======================================================

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





class InventoryMockingTestCase(unittest.TestCase):
    def setUp(self):
        self.sku = ["SKU-000", "SKU-001", "SKU-003", "SKU-004"]
        self.test_cart = ShoppingCart()

    def tearDown(self):
        return super().tearDown()
    
    # ======================================================
    # add_item inventory TESTING
    # ======================================================

    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item(self, mock_inventory):
        mock_inventory.return_value = 10
        self.test_cart.add_item(self.sku[1], 1)
        mock_inventory.assert_called_once_with(self.sku[1])


    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item_InsufficientStockError(self, mock_inventory):
        mock_inventory.return_value = 0
        self.assertRaises(ce.InsufficientStockError, self.test_cart.add_item, self.sku[2], 1)
        mock_inventory.assert_called_once_with(self.sku[2])

    # ======================================================
    # update_quantity inventory TESTING
    # ======================================================
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


class DiscountCodeTestCase(unittest.TestCase):

    
    def setUp(self):
        from datetime import date
        self.test_cart = ShoppingCart()
        self.test_cart._items = {
            "SKU-001": {"name": "Wireless Keyboard",    "sku": "SKU-001", "unit_price": 49.99,  "quantity": 1, "category": "Electronics"},
            "SKU-005": {"name": "Notebook (Pack of 3)", "sku": "SKU-005", "unit_price": 12.99,  "quantity": 1, "category": "Stationery"},
            "SKU-007": {"name": "Monitor Stand",        "sku": "SKU-007", "unit_price": 44.99,  "quantity": 1, "category": "Electronics"},
            "SKU-008": {"name": "Cable Management Kit", "sku": "SKU-008", "unit_price": 18.99,  "quantity": 1, "category": "Home Office"},
        }
        self.codes = ["SAVE10", "SAVE20", "FLAT5", "FLAT15", "EXPIRED50"]
        self.discounts = {
            "SAVE10":    {"type": "percent", "value": 10,    "expires": date(2099, 12, 31)},
            "SAVE20":    {"type": "percent", "value": 20,    "expires": date(2099, 12, 31)},
            "FLAT5":     {"type": "flat",    "value": 5.00,  "expires": date(2099, 12, 31)},
            "FLAT15":    {"type": "flat",    "value": 15.00, "expires": date(2099, 12, 31)},
            "EXPIRED50": {"type": "percent", "value": 50,    "expires": date(2000, 1, 1)},
        }

    def tearDown(self):
        return super().tearDown()
    
    @patch.object(PricingService, "validate_discount_code")
    def test_apply_discount_code_flat(self, mock_pricing):
        #not sure if I really need to mock this because it's read only?
        mock_pricing.return_value = self.discounts[self.codes[2]]
        self.test_cart.apply_discount_code(self.codes[2])
        result = self.test_cart._discount_code
        self.assertEqual(result, self.codes[2])
    
    @patch.object(PricingService, "validate_discount_code")
    def test_apply_discount_code_percent(self, mock_pricing):
        mock_pricing.return_value = self.discounts[self.codes[0]]
        self.test_cart.apply_discount_code(self.codes[0])
        result = self.test_cart._discount_code
        self.assertEqual(result, self.codes[0])
    
    @patch.object(PricingService, "validate_discount_code")
    def test_apply_discount_code_expired_InvalidDiscountCodeError(self, mock_pricing):
        mock_pricing.side_effect = ce.InvalidDiscountCodeError(self.codes[4])
        self.assertRaises(ce.InvalidDiscountCodeError, self.test_cart.apply_discount_code, self.codes[4])
        mock_pricing.assert_called_once_with(self.codes[4])

    @patch.object(PricingService, "validate_discount_code")
    def test_apply_discount_code_InvalidDiscountCodeError(self, mock_pricing):
        mock_pricing.side_effect = ce.InvalidDiscountCodeError("invalid code")
        self.assertRaises(ce.InvalidDiscountCodeError, self.test_cart.apply_discount_code, "invalid code")
        mock_pricing.assert_called_once_with("invalid code")
    
    def test_remove_discount_code(self):
        self.test_cart._discount_code = self.codes[1]
        self.test_cart.remove_discount_code()
        result = self.test_cart._discount_code
        self.assertEqual(result, None)

    def test_apply_discount_flat(self):
        self.test_cart.apply_discount_code(self.codes[2])
        sub = self.test_cart.get_subtotal()
        expected = sub - round(max(sub - self.discounts[self.codes[2]]["value"], 0.0), 2)
        result = self.test_cart.get_discount_amount()
        self.assertEqual(result, expected)

    def test_apply_discount_flat(self):
        self.test_cart.apply_discount_code(self.codes[0])
        sub = self.test_cart.get_subtotal()
        expected = round(max(sub * (float(self.discounts[self.codes[0]]["value"]) / 100.0), 0.0), 2)
        result = self.test_cart.get_discount_amount()
        self.assertEqual(result, expected)

class PriceAndTaxTestCase(unittest.TestCase):
    def setUp(self):
        self.test_cart = ShoppingCart()
        self.test_cart._items = {
            "SKU-001": {"name": "Wireless Keyboard",    "sku": "SKU-001", "unit_price": 49.99,  "quantity": 1, "category": "Electronics"},
            "SKU-005": {"name": "Notebook (Pack of 3)", "sku": "SKU-005", "unit_price": 12.99,  "quantity": 1, "category": "Stationery"},
            "SKU-007": {"name": "Monitor Stand",        "sku": "SKU-007", "unit_price": 44.99,  "quantity": 1, "category": "Electronics"},
            "SKU-008": {"name": "Cable Management Kit", "sku": "SKU-008", "unit_price": 18.99,  "quantity": 1, "category": "Home Office"},
        }
        self.rates = {
            "Electronics": 0.08,
            "Home Office":  0.06,
            "Stationery":   0.05,
        }

    def tearDown(self):
        return super().tearDown()
    
    def test_get_subtotal(self):
        expected = 49.99 + 12.99 + 44.99 + 18.99
        result = self.test_cart.get_subtotal()
        self.assertEqual(result, expected)
    
    def test_get_tax(self):
        expected = 49.99 *  self.rates["Electronics"]
        expected += 12.99 * self.rates["Stationery"]
        expected += 44.99 * self.rates["Electronics"]
        expected += 18.99 * self.rates["Home Office"]
        expected = round(expected, 2)
        result = self.test_cart.get_tax()
        self.assertEqual(result, expected)

    def test_get_total(self):
        expected = self.test_cart.get_subtotal() + self.test_cart.get_tax() - self.test_cart.get_discount_amount()
        result = self.test_cart.get_total()
        self.assertEqual(result, expected)

    
class CheckoutTestCase(unittest.TestCase):
    
    def setUp(self):
        
        self.test_cart = ShoppingCart()

    def tearDown(self):
        return super().tearDown()

    def test_checkout_valid(self):
        from datetime import datetime
        self.test_cart._items = {
            "SKU-001": {"name": "Wireless Keyboard",    "sku": "SKU-001", "unit_price": 49.99,  "quantity": 1, "category": "Electronics"},
            "SKU-005": {"name": "Notebook (Pack of 3)", "sku": "SKU-005", "unit_price": 12.99,  "quantity": 1, "category": "Stationery"},
            "SKU-007": {"name": "Monitor Stand",        "sku": "SKU-007", "unit_price": 44.99,  "quantity": 1, "category": "Electronics"},
            "SKU-008": {"name": "Cable Management Kit", "sku": "SKU-008", "unit_price": 18.99,  "quantity": 1, "category": "Home Office"},
        }
        summary = {
            "customer_id":       self.test_cart._customer_id,
            "timestamp":         datetime.now().isoformat(),
            "items":             self.test_cart.get_items(),
            "subtotal":          self.test_cart.get_subtotal(),
            "discount_code":     self.test_cart._discount_code,
            "discount_amount":   self.test_cart.get_discount_amount(),
            "tax":               self.test_cart.get_tax(),
            "total":             self.test_cart.get_total(),
            "item_count":        self.test_cart.get_item_count(),
        }
        result = self.test_cart.checkout()
        for attr in summary:
            self.assertEqual(summary[attr], result[attr])

    def test_checkout_empty(self):
        self.assertRaises(ce.EmptyCartError, self.test_cart.checkout)
        
    def test_clear(self):
        self.test_cart._items = {
            "SKU-001": {"name": "Wireless Keyboard",    "sku": "SKU-001", "unit_price": 49.99,  "quantity": 1, "category": "Electronics"},
            "SKU-005": {"name": "Notebook (Pack of 3)", "sku": "SKU-005", "unit_price": 12.99,  "quantity": 1, "category": "Stationery"},
            "SKU-007": {"name": "Monitor Stand",        "sku": "SKU-007", "unit_price": 44.99,  "quantity": 1, "category": "Electronics"},
            "SKU-008": {"name": "Cable Management Kit", "sku": "SKU-008", "unit_price": 18.99,  "quantity": 1, "category": "Home Office"},
        }
        self.test_cart.clear()
        items = len(self.test_cart._items)
        disc = self.test_cart._discount_code
        self.assertEqual(items, 0)
        self.assertEqual(disc, None)

if __name__ == "__main__":
    unittest.main()