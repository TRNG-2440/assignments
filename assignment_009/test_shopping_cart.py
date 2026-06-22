import unittest
from unittest.mock import patch, MagicMock

from cart import ShoppingCart
from inventory import InventoryService
from pricing import PricingService
from cart_exceptions import (
    CartError,
    InvalidQuantityError,
    ItemNotFoundError,
    InsufficientStockError,
    CartItemNotFoundError,
    InvalidDiscountCodeError,
    EmptyCartError,
)


class TestItemManagement(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    @patch.object(InventoryService, "_query_inventory_db", return_value=50)
    def test_add_item_creates_line_item_for_valid_sku(self, mock_inventory):
        self.cart.add_item("SKU-001", 2)

        self.assertIn("SKU-001", self.cart._items)
        self.assertEqual(self.cart._items["SKU-001"]["quantity"], 2)
        self.assertEqual(self.cart._items["SKU-001"]["name"], "Wireless Keyboard")
        mock_inventory.assert_called_once_with("SKU-001")

    @patch.object(InventoryService, "_query_inventory_db", return_value=50)
    def test_add_item_merges_quantity_when_sku_already_exists(self, mock_inventory):
        self.cart.add_item("SKU-001", 1)
        self.cart.add_item("SKU-001", 4)

        self.assertEqual(self.cart._items["SKU-001"]["quantity"], 5)
        self.assertEqual(mock_inventory.call_count, 2)

    def test_add_item_rejects_unknown_sku(self):
        for sku in ["BAD-SKU", "SKU-999"]:
            with self.subTest(sku=sku):
                with self.assertRaises(ItemNotFoundError):
                    self.cart.add_item(sku, 1)

    def test_add_item_rejects_non_positive_quantity(self):
        for quantity in [0, -1, -20]:
            with self.subTest(quantity=quantity):
                with self.assertRaises(InvalidQuantityError):
                    self.cart.add_item("SKU-001", quantity)

    def test_remove_item_deletes_existing_sku(self):
        self.cart._items["SKU-001"] = {
            "sku": "SKU-001",
            "name": "Wireless Keyboard",
            "unit_price": 49.99,
            "quantity": 2,
            "category": "Electronics",
        }

        self.cart.remove_item("SKU-001")

        self.assertNotIn("SKU-001", self.cart._items)

    def test_remove_item_raises_when_sku_not_in_cart(self):
        for sku in ["SKU-001", "MISSING-SKU"]:
            with self.subTest(sku=sku):
                with self.assertRaises(CartItemNotFoundError):
                    self.cart.remove_item(sku)

    @patch.object(InventoryService, "_query_inventory_db", return_value=30)
    def test_update_quantity_changes_existing_line_item(self, mock_inventory):
        self.cart._items["SKU-002"] = {
            "sku": "SKU-002",
            "name": "USB-C Hub",
            "unit_price": 34.99,
            "quantity": 1,
            "category": "Electronics",
        }

        self.cart.update_quantity("SKU-002", 6)

        self.assertEqual(self.cart._items["SKU-002"]["quantity"], 6)
        mock_inventory.assert_called_once_with("SKU-002")

    def test_update_quantity_raises_for_missing_cart_item(self):
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity("SKU-002", 2)

    def test_update_quantity_raises_for_non_positive_quantity(self):
        self.cart._items["SKU-002"] = {
            "sku": "SKU-002",
            "name": "USB-C Hub",
            "unit_price": 34.99,
            "quantity": 1,
            "category": "Electronics",
        }

        for quantity in [0, -3]:
            with self.subTest(quantity=quantity):
                with self.assertRaises(InvalidQuantityError):
                    self.cart.update_quantity("SKU-002", quantity)


class TestInventoryChecksWithMocking(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item_succeeds_when_inventory_service_reports_stock(self, mock_inventory):
        mock_inventory.return_value = 12

        self.cart.add_item("SKU-004", 3)

        self.assertEqual(self.cart._items["SKU-004"]["quantity"], 3)
        mock_inventory.assert_called_once_with("SKU-004")

    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item_raises_when_inventory_service_reports_zero_stock(self, mock_inventory):
        mock_inventory.return_value = 0

        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-004", 1)

        mock_inventory.assert_called_once_with("SKU-004")

    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item_raises_when_inventory_is_lower_than_requested(self, mock_inventory):
        mock_inventory.return_value = 2

        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-001", 5)

        mock_inventory.assert_called_once_with("SKU-001")

    @patch.object(InventoryService, "_query_inventory_db")
    def test_update_quantity_raises_when_new_quantity_exceeds_stock(self, mock_inventory):
        self.cart._items["SKU-001"] = {
            "sku": "SKU-001",
            "name": "Wireless Keyboard",
            "unit_price": 49.99,
            "quantity": 1,
            "category": "Electronics",
        }
        mock_inventory.return_value = 3

        with self.assertRaises(InsufficientStockError):
            self.cart.update_quantity("SKU-001", 4)

        mock_inventory.assert_called_once_with("SKU-001")

    @patch.object(InventoryService, "_query_inventory_db")
    def test_inventory_side_effect_can_fail_then_recover(self, mock_inventory):
        mock_inventory.side_effect = [ConnectionError("inventory offline"), 20]

        with self.assertRaises(ConnectionError):
            self.cart.add_item("SKU-005", 1)

        self.cart.add_item("SKU-005", 1)

        self.assertEqual(self.cart._items["SKU-005"]["quantity"], 1)
        self.assertEqual(mock_inventory.call_count, 2)


class TestDiscountCodeBehavior(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()
        self.cart._items["SKU-001"] = {
            "sku": "SKU-001",
            "name": "Wireless Keyboard",
            "unit_price": 49.99,
            "quantity": 2,
            "category": "Electronics",
        }

    def test_percent_discount_code_produces_expected_discount_amount(self):
        self.cart.apply_discount_code("SAVE10")
        self.assertEqual(self.cart.get_discount_amount(), 10.00)

    def test_flat_discount_code_produces_expected_discount_amount(self):
        self.cart.apply_discount_code("FLAT5")
        self.assertEqual(self.cart.get_discount_amount(), 5.00)

    def test_discount_amount_defaults_to_zero_without_code(self):
        self.assertEqual(self.cart.get_discount_amount(), 0.00)

    def test_flat_discount_is_capped_by_subtotal(self):
        self.cart._items = {
            "SKU-005": {
                "sku": "SKU-005",
                "name": "Notebook Pack of 3",
                "unit_price": 12.99,
                "quantity": 1,
                "category": "Stationery",
            }
        }

        self.cart.apply_discount_code("FLAT15")

        self.assertEqual(self.cart.get_discount_amount(), 12.99)

    def test_apply_discount_code_raises_for_invalid_code(self):
        for code in ["NOTREAL", "SAVE500"]:
            with self.subTest(code=code):
                with self.assertRaises(InvalidDiscountCodeError):
                    self.cart.apply_discount_code(code)

    def test_apply_discount_code_raises_for_expired_code(self):
        with self.assertRaises(InvalidDiscountCodeError):
            self.cart.apply_discount_code("EXPIRED50")

    def test_remove_discount_code_clears_current_code(self):
        self.cart.apply_discount_code("SAVE10")
        self.cart.remove_discount_code()

        self.assertIsNone(self.cart._discount_code)


class TestPricingAndTotals(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()
        self.cart._items["SKU-001"] = {
            "sku": "SKU-001",
            "name": "Wireless Keyboard",
            "unit_price": 49.99,
            "quantity": 2,
            "category": "Electronics",
        }
        self.cart._items["SKU-004"] = {
            "sku": "SKU-004",
            "name": "Desk Lamp",
            "unit_price": 24.99,
            "quantity": 2,
            "category": "Home Office",
        }

    def test_get_subtotal_returns_expected_hardcoded_value(self):
        self.assertEqual(self.cart.get_subtotal(), 149.96)

    def test_get_tax_returns_expected_hardcoded_value(self):
        self.assertEqual(self.cart.get_tax(), 11.00)

    def test_get_discount_amount_returns_expected_value_for_known_cart(self):
        self.cart.apply_discount_code("SAVE20")
        self.assertEqual(self.cart.get_discount_amount(), 29.99)

    def test_get_total_matches_subtotal_minus_discount_plus_tax(self):
        self.cart.apply_discount_code("SAVE20")

        subtotal = self.cart.get_subtotal()
        discount = self.cart.get_discount_amount()
        tax = self.cart.get_tax()
        total = self.cart.get_total()

        self.assertEqual(total, 130.97)
        self.assertEqual(total, round(subtotal - discount + tax, 2))


class TestCheckoutAndEdgeCases(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart(customer_id="cust-100")

    def test_checkout_returns_complete_summary_for_populated_cart(self):
        self.cart._items["SKU-003"] = {
            "sku": "SKU-003",
            "name": "Ergonomic Mouse",
            "unit_price": 39.99,
            "quantity": 2,
            "category": "Electronics",
        }
        self.cart.apply_discount_code("SAVE20")

        order = self.cart.checkout()

        expected_keys = {
            "customer_id",
            "timestamp",
            "items",
            "subtotal",
            "discount_code",
            "discount_amount",
            "tax",
            "total",
            "item_count",
        }

        self.assertIsInstance(order, dict)
        self.assertTrue(expected_keys.issubset(order.keys()))
        self.assertEqual(order["customer_id"], "cust-100")
        self.assertEqual(order["items"], [self.cart._items["SKU-003"]])
        self.assertEqual(order["subtotal"], 79.98)
        self.assertEqual(order["discount_code"], "SAVE20")
        self.assertEqual(order["discount_amount"], 16.00)
        self.assertEqual(order["tax"], 6.40)
        self.assertEqual(order["total"], 70.38)
        self.assertEqual(order["item_count"], 2)

    def test_checkout_raises_for_empty_cart(self):
        with self.assertRaises(EmptyCartError):
            self.cart.checkout()

    def test_clear_removes_all_items_and_discount_code(self):
        self.cart._items["SKU-001"] = {
            "sku": "SKU-001",
            "name": "Wireless Keyboard",
            "unit_price": 49.99,
            "quantity": 1,
            "category": "Electronics",
        }
        self.cart.apply_discount_code("SAVE10")

        self.cart.clear()

        self.assertEqual(self.cart._items, {})
        self.assertIsNone(self.cart._discount_code)

    def test_cart_error_is_base_class_for_cart_exceptions(self):
        self.assertTrue(issubclass(ItemNotFoundError, CartError))
        self.assertTrue(issubclass(InvalidQuantityError, CartError))
        self.assertTrue(issubclass(InsufficientStockError, CartError))
        self.assertTrue(issubclass(CartItemNotFoundError, CartError))
        self.assertTrue(issubclass(InvalidDiscountCodeError, CartError))
        self.assertTrue(issubclass(EmptyCartError, CartError))


class TestPricingServiceMockIntegration(unittest.TestCase):
    def setUp(self):
        self.mock_pricing = MagicMock(spec=PricingService)
        self.cart = ShoppingCart(pricing_service=self.mock_pricing)
        self.cart._items["SKU-001"] = {
            "sku": "SKU-001",
            "name": "Wireless Keyboard",
            "unit_price": 50.00,
            "quantity": 2,
            "category": "Electronics",
        }

    def test_checkout_uses_injected_pricing_service_methods(self):
        self.mock_pricing.validate_discount_code.return_value = {
            "type": "percent",
            "value": 20,
        }
        self.mock_pricing.apply_discount.return_value = 80.00
        self.mock_pricing.calculate_tax.return_value = 10.00

        self.cart.apply_discount_code("SAVE20")
        order = self.cart.checkout()

        self.mock_pricing.validate_discount_code.assert_called_with("SAVE20")

        self.mock_pricing.apply_discount.assert_called_with(100.00, "SAVE20")

        self.assertGreaterEqual(self.mock_pricing.calculate_tax.call_count, 1)
        self.mock_pricing.calculate_tax.assert_called_with(list(self.cart._items.values()))

        self.assertEqual(order["discount_amount"], 20.00)
        self.assertEqual(order["tax"], 10.00)
        self.assertEqual(order["total"], 90.00)


if __name__ == "__main__":
    unittest.main()