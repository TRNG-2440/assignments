import unittest
from unittest.mock import patch, MagicMock

from cart import ShoppingCart
from cart_exceptions import (
    CartError,
    InvalidQuantityError,
    ItemNotFoundError,
    InsufficientStockError,
    CartItemNotFoundError,
    EmptyCartError,
    InvalidDiscountCodeError,
)
from inventory import InventoryService
from pricing import PricingService
from catalogue import PRODUCT_CATALOGUE, DISCOUNT_CODES



#### ITEM MANAGEMENT
class TestItemManagement(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()
        self.sku = "SKU-001"  # Wireless Keyboard

    def test_add_item_valid(self):
        self.cart.add_item(self.sku, 2)
        self.assertIn(self.sku, self.cart._items)
        self.assertEqual(self.cart._items[self.sku]["quantity"], 2)

    def test_add_item_accumulates_quantity(self):
        self.cart.add_item(self.sku, 1)
        self.cart.add_item(self.sku, 3)
        self.assertEqual(self.cart._items[self.sku]["quantity"], 4)

    def test_add_item_invalid_sku(self):
        with self.assertRaises(ItemNotFoundError):
            self.cart.add_item("BAD-SKU", 1)

    def test_add_item_invalid_quantity(self):
        for invalid in (0, -1, -10):
            with self.subTest(invalid=invalid):
                with self.assertRaises(InvalidQuantityError):
                    self.cart.add_item(self.sku, invalid)

    def test_remove_item_valid(self):
        self.cart.add_item(self.sku, 1)
        self.cart.remove_item(self.sku)
        self.assertNotIn(self.sku, self.cart._items)

    def test_remove_item_not_found(self):
        with self.assertRaises(CartItemNotFoundError):
            self.cart.remove_item("SKU-999")

    def test_update_quantity_valid(self):
        self.cart.add_item(self.sku, 1)
        self.cart.update_quantity(self.sku, 5)
        self.assertEqual(self.cart._items[self.sku]["quantity"], 5)

    def test_update_quantity_invalid(self):
        self.cart.add_item(self.sku, 1)
        with self.assertRaises(InvalidQuantityError):
            self.cart.update_quantity(self.sku, 0)

    def test_update_quantity_item_not_found(self):
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity("SKU-999", 3)

#### INVENTORY WITH MOCKS
class TestInventoryChecks(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()
        self.sku = "SKU-001"

    @patch.object(InventoryService, "get_stock")
    def test_add_item_stock_available(self, mock_stock):
        mock_stock.return_value = 10

        self.cart.add_item(self.sku, 2)

        mock_stock.assert_called_once_with(self.sku)
        self.assertEqual(self.cart._items[self.sku]["quantity"], 2)

    @patch.object(InventoryService, "get_stock")
    def test_add_item_stock_unavailable(self, mock_stock):
        mock_stock.return_value = 0

        with self.assertRaises(InsufficientStockError):
            self.cart.add_item(self.sku, 1)

    @patch.object(InventoryService, "get_stock")
    def test_add_item_stock_lower_than_requested(self, mock_stock):
        mock_stock.return_value = 3

        with self.assertRaises(InsufficientStockError):
            self.cart.add_item(self.sku, 5)

    @patch.object(InventoryService, "get_stock")
    def test_inventory_method_called(self, mock_stock):
        mock_stock.return_value = 5

        self.cart.add_item(self.sku, 1)

        mock_stock.assert_called_with(self.sku)


#### DISCOUNT CODES
class TestDiscountCodes(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()
        self.cart.add_item("SKU-001", 2)

    def test_valid_percentage_discount(self):
        self.cart.apply_discount_code("SAVE10")
        expected = round(self.cart.get_subtotal() * 0.10, 2)
        self.assertEqual(self.cart.get_discount_amount(), expected)

    def test_valid_flat_discount(self):
        self.cart.apply_discount_code("FLAT5")
        self.assertEqual(self.cart.get_discount_amount(), 5.00)

    def test_unrecognised_discount_code(self):
        with self.assertRaises(InvalidDiscountCodeError):
            self.cart.apply_discount_code("BADCODE")

    def test_expired_discount_code(self):
        with self.assertRaises(InvalidDiscountCodeError):
            self.cart.apply_discount_code("EXPIRED50")

    def test_remove_discount_code(self):
        self.cart.apply_discount_code("SAVE10")
        self.cart.remove_discount_code()
        self.assertIsNone(self.cart._discount_code)

#### PRICING AND TAX
class TestPricingAndTax(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()
        self.cart.add_item("SKU-001", 2)  # 49.99 each
        self.cart.add_item("SKU-004", 1)  # 24.99

    def test_subtotal(self):
        expected = (
            PRODUCT_CATALOGUE["SKU-001"]["price"] * 2 +
            PRODUCT_CATALOGUE["SKU-004"]["price"]
        )
        self.assertEqual(self.cart.get_subtotal(), round(expected, 2))

    def test_discount_amount(self):
        self.cart.apply_discount_code("SAVE10")
        expected = round(self.cart.get_subtotal() * 0.10, 2)
        self.assertEqual(self.cart.get_discount_amount(), expected)

    def test_tax(self):
        items = self.cart.get_items()
        expected_tax = PricingService().calculate_tax(items)
        self.assertEqual(self.cart.get_tax(), expected_tax)

    def test_total(self):
        subtotal = self.cart.get_subtotal()
        discount = self.cart.get_discount_amount()
        tax = self.cart.get_tax()
        expected_total = round(subtotal - discount + tax, 2)
        self.assertEqual(self.cart.get_total(), expected_total)


#### CHECKOUT AND EDGE CASES
class TestCheckoutAndEdgeCases(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_checkout_populated_cart(self):
        self.cart.add_item("SKU-001", 1)
        summary = self.cart.checkout()

        self.assertIn("items", summary)
        self.assertIn("subtotal", summary)
        self.assertIn("discount_code", summary)
        self.assertIn("discount_amount", summary)
        self.assertIn("tax", summary)
        self.assertIn("total", summary)
        self.assertIn("item_count", summary)
        self.assertIn("timestamp", summary)
        self.assertIn("customer_id", summary)

    def test_checkout_empty_cart(self):
        with self.assertRaises(EmptyCartError):
            self.cart.checkout()

    def test_clear_resets_cart(self):
        self.cart.add_item("SKU-001", 1)
        self.cart.apply_discount_code("SAVE10")
        self.cart.clear()

        self.assertEqual(self.cart._items, {})
        self.assertIsNone(self.cart._discount_code)

    def test_add_zero_or_negative_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item("SKU-001", 0)
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item("SKU-001", -1)

    def test_remove_item_not_in_cart(self):
        with self.assertRaises(CartItemNotFoundError):
            self.cart.remove_item("SKU-999")

    def test_update_item_not_in_cart(self):
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity("SKU-999", 3)

    def test_add_nonexistent_sku(self):
        with self.assertRaises(ItemNotFoundError):
            self.cart.add_item("BAD-SKU", 1)

