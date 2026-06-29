import unittest
from unittest.mock import patch

from cart import ShoppingCart
from inventory import InventoryService

from cart_exceptions import (
    CartError,
    ItemNotFoundError,
    InvalidQuantityError,
    InsufficientStockError,
    CartItemNotFoundError,
    EmptyCartError,
    InvalidDiscountCodeError,
)


# ==========================================================
# 1. ITEM MANAGEMENT TESTS
# ==========================================================

class TestItemManagement(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_item_success(self):
        self.cart.add_item("SKU-001", 2)

        items = self.cart.get_items()

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["sku"], "SKU-001")
        self.assertEqual(items[0]["quantity"], 2)

    def test_duplicate_sku_accumulates_quantity(self):
        self.cart.add_item("SKU-001", 2)
        self.cart.add_item("SKU-001", 3)

        items = self.cart.get_items()

        self.assertEqual(items[0]["quantity"], 5)

    def test_remove_item_success(self):
        self.cart.add_item("SKU-001", 1)

        self.cart.remove_item("SKU-001")

        self.assertTrue(self.cart.is_empty())

    def test_remove_item_not_in_cart(self):
        with self.assertRaises(CartItemNotFoundError):
            self.cart.remove_item("SKU-001")

    def test_update_quantity_success(self):
        self.cart.add_item("SKU-001", 1)

        self.cart.update_quantity("SKU-001", 5)

        items = self.cart.get_items()

        self.assertEqual(items[0]["quantity"], 5)

    def test_update_quantity_invalid(self):
        self.cart.add_item("SKU-001", 1)

        with self.assertRaises(InvalidQuantityError):
            self.cart.update_quantity("SKU-001", 0)

    def test_update_quantity_item_not_found(self):
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity("SKU-001", 5)

    def test_invalid_sku(self):
        with self.assertRaises(ItemNotFoundError):
            self.cart.add_item("SKU-999", 1)

    def test_invalid_quantity_values(self):
        for qty in [0, -1, -10]:
            with self.subTest(quantity=qty):
                with self.assertRaises(InvalidQuantityError):
                    self.cart.add_item("SKU-001", qty)


# ==========================================================
# 2. INVENTORY MOCKING TESTS
# ==========================================================

class TestInventoryChecksWithMocking(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    @patch.object(InventoryService, "get_stock")
    def test_sufficient_stock_adds_item(self, mock_stock):
        mock_stock.return_value = 100

        self.cart.add_item("SKU-001", 10)

        items = self.cart.get_items()

        self.assertEqual(items[0]["quantity"], 10)
        mock_stock.assert_called_once_with("SKU-001")

    @patch.object(InventoryService, "get_stock")
    def test_no_stock_available(self, mock_stock):
        mock_stock.return_value = 0

        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-001", 1)

    @patch.object(InventoryService, "get_stock")
    def test_requested_quantity_greater_than_stock(self, mock_stock):
        mock_stock.return_value = 5

        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-001", 10)

        mock_stock.assert_called_once_with("SKU-001")

    @patch.object(InventoryService, "get_stock")
    def test_update_quantity_insufficient_stock(self, mock_stock):
        mock_stock.return_value = 50

        self.cart.add_item("SKU-001", 1)

        mock_stock.return_value = 3

        with self.assertRaises(InsufficientStockError):
            self.cart.update_quantity("SKU-001", 10)


# ==========================================================
# 3. DISCOUNT CODE TESTS
# ==========================================================

class TestDiscountCodes(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

        self.cart.add_item("SKU-001", 2)
        self.cart.add_item("SKU-005", 3)

    def test_valid_percent_discount(self):
        self.cart.apply_discount_code("SAVE10")

        self.assertEqual(self.cart.get_discount_amount(), 13.90)

    def test_valid_flat_discount(self):
        self.cart.apply_discount_code("FLAT5")

        self.assertEqual(self.cart.get_discount_amount(), 5.00)

    def test_invalid_discount_code(self):
        with self.assertRaises(InvalidDiscountCodeError):
            self.cart.apply_discount_code("NOTREAL")

    def test_expired_discount_code(self):
        with self.assertRaises(InvalidDiscountCodeError):
            self.cart.apply_discount_code("EXPIRED50")

    def test_remove_discount_code(self):
        self.cart.apply_discount_code("SAVE10")

        self.assertGreater(self.cart.get_discount_amount(), 0)

        self.cart.remove_discount_code()

        self.assertEqual(self.cart.get_discount_amount(), 0.0)


# ==========================================================
# 4. PRICING AND TAX TESTS
# ==========================================================

class TestPricingAndTaxCalculations(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

        self.cart.add_item("SKU-001", 2)
        self.cart.add_item("SKU-005", 3)

    def test_subtotal(self):
        self.assertEqual(self.cart.get_subtotal(), 138.95)

    def test_tax(self):
        self.assertEqual(self.cart.get_tax(), 9.95)

    def test_discount_amount(self):
        self.cart.apply_discount_code("SAVE10")

        self.assertEqual(self.cart.get_discount_amount(), 13.90)

    def test_total_calculation(self):
        self.cart.apply_discount_code("SAVE10")

        expected_total = 138.95 - 13.90 + 9.95

        self.assertEqual(self.cart.get_total(), round(expected_total, 2))


# ==========================================================
# 5. CHECKOUT AND EDGE CASE TESTS
# ==========================================================

class TestCheckoutAndEdgeCases(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_checkout_returns_summary(self):
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

        self.assertTrue(required_keys.issubset(summary.keys()))

    def test_checkout_empty_cart(self):
        with self.assertRaises(EmptyCartError):
            self.cart.checkout()

    def test_clear_resets_cart(self):
        self.cart.add_item("SKU-001", 2)
        self.cart.apply_discount_code("SAVE10")

        self.cart.clear()

        self.assertTrue(self.cart.is_empty())
        self.assertEqual(self.cart.get_discount_amount(), 0.0)

    def test_remove_missing_item(self):
        with self.assertRaises(CartItemNotFoundError):
            self.cart.remove_item("SKU-001")

    def test_update_missing_item(self):
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity("SKU-001", 5)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item("SKU-001", -5)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item("SKU-001", 0)

    def test_add_item_insufficient_stock_real_inventory(self):
        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-007", 10)


if __name__ == "__main__":
    unittest.main()
