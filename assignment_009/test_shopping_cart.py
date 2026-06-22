import unittest
from unittest.mock import MagicMock, call, patch

from cart import ShoppingCart
from cart_exceptions import (
    CartItemNotFoundError,
    EmptyCartError,
    InsufficientStockError,
    InvalidDiscountCodeError,
    InvalidQuantityError,
    ItemNotFoundError,
)
from inventory import InventoryService


class TestItemManagement(unittest.TestCase):
    def setUp(self):
        self.inventory = MagicMock(spec=InventoryService)
        self.inventory.get_stock.return_value = 100
        self.cart = ShoppingCart(inventory_service=self.inventory)

    def test_add_item(self):
        self.cart.add_item("SKU-001", 2)

        item = self.cart.get_items()[0]
        self.assertEqual(item["sku"], "SKU-001")
        self.assertEqual(item["quantity"], 2)

    def test_add_same_sku_accumulates_quantity(self):
        self.cart.add_item("SKU-001", 2)
        self.cart.add_item("SKU-001", 3)

        self.assertEqual(self.cart.get_items()[0]["quantity"], 5)

    def test_remove_item(self):
        self.cart.add_item("SKU-001")

        self.cart.remove_item("SKU-001")

        self.assertTrue(self.cart.is_empty())

    def test_remove_missing_item_raises_error(self):
        with self.assertRaises(CartItemNotFoundError):
            self.cart.remove_item("SKU-001")

    def test_update_quantity(self):
        self.cart.add_item("SKU-001")

        self.cart.update_quantity("SKU-001", 4)

        self.assertEqual(self.cart.get_items()[0]["quantity"], 4)

    def test_update_missing_item_raises_error(self):
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity("SKU-001", 2)

    def test_update_with_invalid_quantities_raises_error(self):
        self.cart.add_item("SKU-001")

        for quantity in (0, -1, -100):
            with self.subTest(quantity=quantity):
                with self.assertRaises(InvalidQuantityError):
                    self.cart.update_quantity("SKU-001", quantity)

    def test_update_with_insufficient_stock_raises_error(self):
        self.cart.add_item("SKU-001")
        self.inventory.get_stock.return_value = 2

        with self.assertRaises(InsufficientStockError):
            self.cart.update_quantity("SKU-001", 3)


class TestInventoryChecks(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    @patch.object(InventoryService, "_query_inventory_db")
    def test_sufficient_stock_adds_item(self, mock_query):
        mock_query.return_value = 10

        self.cart.add_item("SKU-001", 3)

        self.assertEqual(self.cart.get_item_count(), 3)
        mock_query.assert_called_once_with("SKU-001")

    @patch.object(InventoryService, "_query_inventory_db")
    def test_unavailable_stock_raises_error(self, mock_query):
        mock_query.return_value = 0

        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-001", 1)

    @patch.object(InventoryService, "_query_inventory_db")
    def test_stock_lower_than_requested_raises_error(self, mock_query):
        mock_query.return_value = 2

        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-001", 3)

        mock_query.assert_called_once_with("SKU-001")

    @patch.object(InventoryService, "_query_inventory_db")
    def test_temporary_inventory_failure_then_recovery(self, mock_query):
        mock_query.side_effect = [ConnectionError("Inventory unavailable"), 5]

        with self.assertRaises(ConnectionError):
            self.cart.add_item("SKU-001", 2)
        self.cart.add_item("SKU-001", 2)

        self.assertEqual(self.cart.get_item_count(), 2)
        self.assertEqual(mock_query.call_count, 2)


class TestDiscountCodes(unittest.TestCase):
    def setUp(self):
        self.inventory = MagicMock(spec=InventoryService)
        self.inventory.get_stock.return_value = 100
        self.cart = ShoppingCart(inventory_service=self.inventory)
        self.cart.add_item("SKU-001")

    def test_valid_discount_codes(self):
        cases = (("SAVE10", 5.00), ("FLAT5", 5.00))

        for code, expected_discount in cases:
            with self.subTest(code=code):
                self.cart.apply_discount_code(code)
                self.assertEqual(self.cart.get_discount_amount(), expected_discount)

    def test_unrecognised_code_raises_error(self):
        with self.assertRaises(InvalidDiscountCodeError):
            self.cart.apply_discount_code("NOT-A-CODE")

    def test_expired_code_raises_error(self):
        with self.assertRaises(InvalidDiscountCodeError):
            self.cart.apply_discount_code("EXPIRED50")

    def test_remove_discount_code(self):
        self.cart.apply_discount_code("SAVE10")

        self.cart.remove_discount_code()

        self.assertEqual(self.cart.get_discount_amount(), 0.0)


class TestPricingAndTaxCalculations(unittest.TestCase):
    def setUp(self):
        self.inventory = MagicMock(spec=InventoryService)
        self.inventory.get_stock.return_value = 100
        self.cart = ShoppingCart(inventory_service=self.inventory)
        self.cart.add_item("SKU-001", 2)
        self.cart.add_item("SKU-004", 1)
        self.cart.apply_discount_code("SAVE10")

    def test_subtotal(self):
        self.assertEqual(self.cart.get_subtotal(), 124.97)

    def test_discount_amount(self):
        self.assertEqual(self.cart.get_discount_amount(), 12.50)

    def test_tax(self):
        self.assertEqual(self.cart.get_tax(), 9.50)

    def test_total(self):
        self.assertEqual(self.cart.get_total(), 121.97)

    def test_total_combines_subtotal_discount_and_tax(self):
        expected = 124.97 - 12.50 + 9.50

        self.assertEqual(self.cart.get_total(), round(expected, 2))


class TestCheckoutAndEdgeCases(unittest.TestCase):
    def setUp(self):
        self.inventory = MagicMock(spec=InventoryService)
        self.inventory.get_stock.return_value = 100
        self.cart = ShoppingCart(
            inventory_service=self.inventory, customer_id="customer-123"
        )

    def test_checkout_populated_cart_returns_summary(self):
        self.cart.add_item("SKU-001", 2)

        summary = self.cart.checkout()

        required_keys = {
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
        self.assertTrue(required_keys.issubset(summary))
        self.assertEqual(summary["customer_id"], "customer-123")
        self.assertEqual(summary["item_count"], 2)

    def test_checkout_empty_cart_raises_error(self):
        with self.assertRaises(EmptyCartError):
            self.cart.checkout()

    def test_clear_removes_items_and_discount(self):
        self.cart.add_item("SKU-001")
        self.cart.apply_discount_code("SAVE10")

        self.cart.clear()

        self.assertTrue(self.cart.is_empty())
        self.assertEqual(self.cart.get_discount_amount(), 0.0)

    def test_add_invalid_quantities_raises_error(self):
        for quantity in (0, -1, -100):
            with self.subTest(quantity=quantity):
                with self.assertRaises(InvalidQuantityError):
                    self.cart.add_item("SKU-001", quantity)

    def test_remove_or_update_missing_item_raises_error(self):
        operations = (
            ("remove", lambda: self.cart.remove_item("SKU-001")),
            ("update", lambda: self.cart.update_quantity("SKU-001", 2)),
        )

        for operation, action in operations:
            with self.subTest(operation=operation):
                with self.assertRaises(CartItemNotFoundError):
                    action()

    def test_add_unknown_sku_raises_error(self):
        with self.assertRaises(ItemNotFoundError):
            self.cart.add_item("SKU-999")


class TestPricingServiceMocking(unittest.TestCase):
    def setUp(self):
        self.inventory = MagicMock(spec=InventoryService)
        self.inventory.get_stock.return_value = 100
        self.pricing = MagicMock()
        self.pricing.apply_discount.return_value = 40.00
        self.pricing.calculate_tax.return_value = 4.00
        self.cart = ShoppingCart(
            inventory_service=self.inventory, pricing_service=self.pricing
        )
        self.cart.add_item("SKU-001")
        self.cart.apply_discount_code("SAVE10")

    def test_checkout_uses_mocked_pricing_service(self):
        self.cart.checkout()

        expected_items = self.cart.get_items()
        self.assertEqual(
            self.pricing.apply_discount.call_args_list,
            [call(49.99, "SAVE10"), call(49.99, "SAVE10")],
        )
        self.assertEqual(
            self.pricing.calculate_tax.call_args_list,
            [call(expected_items), call(expected_items)],
        )


if __name__ == "__main__":
    unittest.main()
