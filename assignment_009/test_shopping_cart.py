import unittest
from unittest.mock import patch, MagicMock

from cart import ShoppingCart
from cart_exceptions import (
    CartError,
    ItemNotFoundError,
    InvalidQuantityError,
    InsufficientStockError,
    InvalidDiscountCodeError,
    EmptyCartError,
    CartItemNotFoundError,
)
from inventory import InventoryService
from pricing import PricingService


# ---------------------------------------------------------------------------
# 1. Item Management
# ---------------------------------------------------------------------------

class TestItemManagement(unittest.TestCase):
    """Tests for add_item, remove_item, and update_quantity."""

    def setUp(self):
        self.mock_inventory = MagicMock(spec=InventoryService)
        self.mock_inventory.get_stock.return_value = 50
        self.mock_inventory.is_available.return_value = True
        self.cart = ShoppingCart(inventory_service=self.mock_inventory)

    # --- add_item ---

    def test_add_item_valid(self):
        """Adding a valid SKU with sufficient stock adds it to the cart."""
        self.cart.add_item("SKU-001", 2)
        self.assertEqual(self.cart.get_item_count(), 2)

    def test_add_item_default_quantity_is_one(self):
        """add_item with no quantity argument defaults to 1."""
        self.cart.add_item("SKU-001")
        self.assertEqual(self.cart.get_item_count(), 1)

    def test_add_item_duplicate_sku_accumulates_quantity(self):
        """Adding the same SKU twice sums the quantities."""
        self.cart.add_item("SKU-001", 3)
        self.cart.add_item("SKU-001", 2)
        items = {i["sku"]: i for i in self.cart.get_items()}
        self.assertEqual(items["SKU-001"]["quantity"], 5)

    def test_add_item_multiple_skus(self):
        """Adding different SKUs results in separate line items."""
        self.cart.add_item("SKU-001", 1)
        self.cart.add_item("SKU-002", 1)
        self.assertEqual(len(self.cart.get_items()), 2)

    def test_add_item_invalid_sku_raises_item_not_found(self):
        """Adding an unrecognised SKU raises ItemNotFoundError."""
        with self.assertRaises(ItemNotFoundError):
            self.cart.add_item("SKU-FAKE", 1)

    def test_add_item_zero_quantity_raises_invalid_quantity(self):
        """Adding with quantity=0 raises InvalidQuantityError."""
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item("SKU-001", 0)

    def test_add_item_negative_quantity_raises_invalid_quantity(self):
        """Adding with a negative quantity raises InvalidQuantityError."""
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item("SKU-001", -3)

    def test_add_item_insufficient_stock_raises_error(self):
        """Adding more than available stock raises InsufficientStockError."""
        self.mock_inventory.get_stock.return_value = 2
        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-001", 5)

    # --- remove_item ---

    def test_remove_item_valid(self):
        """Removing an item that is in the cart leaves it empty."""
        self.cart.add_item("SKU-001", 1)
        self.cart.remove_item("SKU-001")
        self.assertTrue(self.cart.is_empty())

    def test_remove_item_not_in_cart_raises_error(self):
        """Removing an SKU not in the cart raises CartItemNotFoundError."""
        with self.assertRaises(CartItemNotFoundError):
            self.cart.remove_item("SKU-001")

    # --- update_quantity ---

    def test_update_quantity_valid(self):
        """Updating quantity to a valid value changes the cart correctly."""
        self.cart.add_item("SKU-001", 1)
        self.cart.update_quantity("SKU-001", 10)
        items = {i["sku"]: i for i in self.cart.get_items()}
        self.assertEqual(items["SKU-001"]["quantity"], 10)

    def test_update_quantity_zero_raises_invalid_quantity(self):
        """Updating to zero raises InvalidQuantityError."""
        self.cart.add_item("SKU-001", 1)
        with self.assertRaises(InvalidQuantityError):
            self.cart.update_quantity("SKU-001", 0)

    def test_update_quantity_negative_raises_invalid_quantity(self):
        """Updating to a negative value raises InvalidQuantityError."""
        self.cart.add_item("SKU-001", 1)
        with self.assertRaises(InvalidQuantityError):
            self.cart.update_quantity("SKU-001", -1)

    def test_update_quantity_exceeds_stock_raises_insufficient_stock(self):
        """Updating to a quantity above stock raises InsufficientStockError."""
        self.mock_inventory.get_stock.return_value = 5
        self.cart.add_item("SKU-001", 1)
        with self.assertRaises(InsufficientStockError):
            self.cart.update_quantity("SKU-001", 10)

    def test_update_quantity_sku_not_in_cart_raises_error(self):
        """Updating an SKU not in the cart raises CartItemNotFoundError."""
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity("SKU-001", 3)


# ---------------------------------------------------------------------------
# 2. Inventory Checks with Mocking
# ---------------------------------------------------------------------------

class TestInventoryMocking(unittest.TestCase):
    """Tests that verify ShoppingCart delegates correctly to InventoryService."""

    def setUp(self):
        self.cart = ShoppingCart()

    @patch.object(InventoryService, "_query_inventory_db")
    def test_add_item_calls_inventory_with_correct_sku(self, mock_query):
        """add_item calls the inventory service with the correct SKU."""
        mock_query.return_value = 50
        self.cart.add_item("SKU-001", 1)
        mock_query.assert_called_with("SKU-001")

    @patch.object(InventoryService, "_query_inventory_db")
    def test_sufficient_stock_allows_add(self, mock_query):
        """When stock is sufficient, add_item succeeds."""
        mock_query.return_value = 100
        self.cart.add_item("SKU-001", 5)
        self.assertEqual(self.cart.get_item_count(), 5)

    @patch.object(InventoryService, "_query_inventory_db")
    def test_zero_stock_raises_insufficient_stock(self, mock_query):
        """When the inventory returns 0 stock, InsufficientStockError is raised."""
        mock_query.return_value = 0
        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-001", 1)

    @patch.object(InventoryService, "_query_inventory_db")
    def test_partial_stock_raises_insufficient_stock(self, mock_query):
        """When stock is lower than requested quantity, error is raised."""
        mock_query.return_value = 3
        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-001", 5)

    @patch.object(InventoryService, "_query_inventory_db")
    def test_inventory_called_once_on_add(self, mock_query):
        """The inventory DB is queried exactly once per add_item call."""
        mock_query.return_value = 50
        self.cart.add_item("SKU-001", 2)
        mock_query.assert_called_once_with("SKU-001")

    @patch.object(InventoryService, "_query_inventory_db")
    def test_duplicate_sku_rechecks_total_quantity(self, mock_query):
        """
        When adding a duplicate SKU, inventory is re-checked against the
        combined (existing + new) quantity.
        """
        mock_query.return_value = 5
        self.cart.add_item("SKU-001", 3)
        with self.assertRaises(InsufficientStockError) as ctx:
            self.cart.add_item("SKU-001", 3)
        self.assertEqual(ctx.exception.requested, 6)
        self.assertEqual(ctx.exception.available, 5)


# ---------------------------------------------------------------------------
# 3. Discount Codes
# ---------------------------------------------------------------------------

class TestDiscountCodes(unittest.TestCase):
    """Tests for discount code validation, application, and removal."""

    def setUp(self):
        mock_inventory = MagicMock(spec=InventoryService)
        mock_inventory.get_stock.return_value = 50
        self.cart = ShoppingCart(inventory_service=mock_inventory)
        # SKU-001 @ $49.99 × 2 = $99.98 subtotal
        self.cart.add_item("SKU-001", 2)

    def test_apply_valid_percent_discount(self):
        """SAVE10 applies a 10% discount to the subtotal."""
        self.cart.apply_discount_code("SAVE10")
        expected = round(99.98 * 0.10, 2)
        self.assertAlmostEqual(self.cart.get_discount_amount(), expected, places=2)

    def test_apply_valid_flat_discount(self):
        """FLAT5 applies a $5.00 flat discount."""
        self.cart.apply_discount_code("FLAT5")
        self.assertAlmostEqual(self.cart.get_discount_amount(), 5.00, places=2)

    def test_apply_valid_flat15_discount(self):
        """FLAT15 applies a $15.00 flat discount."""
        self.cart.apply_discount_code("FLAT15")
        self.assertAlmostEqual(self.cart.get_discount_amount(), 15.00, places=2)

    def test_apply_valid_save20_discount(self):
        """SAVE20 applies a 20% discount to the subtotal."""
        self.cart.apply_discount_code("SAVE20")
        expected = round(99.98 * 0.20, 2)
        self.assertAlmostEqual(self.cart.get_discount_amount(), expected, places=2)

    def test_apply_expired_code_raises_error(self):
        """Applying EXPIRED50 raises InvalidDiscountCodeError."""
        with self.assertRaises(InvalidDiscountCodeError):
            self.cart.apply_discount_code("EXPIRED50")

    def test_apply_unrecognised_code_raises_error(self):
        """Applying a made-up code raises InvalidDiscountCodeError."""
        with self.assertRaises(InvalidDiscountCodeError):
            self.cart.apply_discount_code("NOTACODE")

    def test_code_is_case_insensitive(self):
        """Discount codes are accepted in lowercase."""
        self.cart.apply_discount_code("save10")
        self.assertGreater(self.cart.get_discount_amount(), 0)

    def test_remove_discount_code(self):
        """Removing a discount code resets the discount amount to 0."""
        self.cart.apply_discount_code("SAVE10")
        self.cart.remove_discount_code()
        self.assertEqual(self.cart.get_discount_amount(), 0.0)

    def test_no_discount_code_returns_zero_discount(self):
        """get_discount_amount returns 0.0 when no code is applied."""
        self.assertEqual(self.cart.get_discount_amount(), 0.0)

    def test_applying_new_code_replaces_old(self):
        """Applying a second discount code replaces the first."""
        self.cart.apply_discount_code("SAVE10")
        self.cart.apply_discount_code("FLAT5")
        self.assertAlmostEqual(self.cart.get_discount_amount(), 5.00, places=2)


# ---------------------------------------------------------------------------
# 4. Pricing and Tax Calculations
# ---------------------------------------------------------------------------

class TestPricingAndTax(unittest.TestCase):
    """
    Tests for get_subtotal, get_tax, get_discount_amount, and get_total
    using a fixed, known cart configuration.

    Cart contents:
      SKU-001  Wireless Keyboard   $49.99 × 2  Electronics  tax 8%
      SKU-004  Desk Lamp           $24.99 × 1  Home Office  tax 6%
      SKU-005  Notebook (Pack 3)   $12.99 × 3  Stationery   tax 5%

    Subtotal  = (49.99×2) + (24.99×1) + (12.99×3)
              = 99.98 + 24.99 + 38.97
              = 163.94

    Tax       = (99.98 × 0.08) + (24.99 × 0.06) + (38.97 × 0.05)
              = 7.9984 + 1.4994 + 1.9485
              = 11.45  (rounded to 2 dp)
    """

    SUBTOTAL = 163.94
    TAX      = 11.45

    def setUp(self):
        mock_inventory = MagicMock(spec=InventoryService)
        mock_inventory.get_stock.return_value = 100
        self.cart = ShoppingCart(inventory_service=mock_inventory)
        self.cart.add_item("SKU-001", 2)   # Electronics
        self.cart.add_item("SKU-004", 1)   # Home Office
        self.cart.add_item("SKU-005", 3)   # Stationery

    def test_subtotal(self):
        """get_subtotal returns the correct sum of line-item totals."""
        self.assertAlmostEqual(self.cart.get_subtotal(), self.SUBTOTAL, places=2)

    def test_tax(self):
        """get_tax returns the correct blended tax across categories."""
        self.assertAlmostEqual(self.cart.get_tax(), self.TAX, places=2)

    def test_total_without_discount(self):
        """get_total equals subtotal + tax when no discount is applied."""
        expected = round(self.SUBTOTAL + self.TAX, 2)
        self.assertAlmostEqual(self.cart.get_total(), expected, places=2)

    def test_total_with_percent_discount(self):
        """get_total correctly applies a percentage discount before adding tax."""
        self.cart.apply_discount_code("SAVE10")
        discount = round(self.SUBTOTAL * 0.10, 2)
        expected = round(self.SUBTOTAL - discount + self.TAX, 2)
        self.assertAlmostEqual(self.cart.get_total(), expected, places=2)

    def test_total_with_flat_discount(self):
        """get_total correctly applies a flat discount before adding tax."""
        self.cart.apply_discount_code("FLAT15")
        expected = round(self.SUBTOTAL - 15.00 + self.TAX, 2)
        self.assertAlmostEqual(self.cart.get_total(), expected, places=2)

    def test_total_is_subtotal_minus_discount_plus_tax(self):
        """get_total = get_subtotal - get_discount_amount + get_tax."""
        self.cart.apply_discount_code("SAVE20")
        expected = round(
            self.cart.get_subtotal()
            - self.cart.get_discount_amount()
            + self.cart.get_tax(),
            2,
        )
        self.assertAlmostEqual(self.cart.get_total(), expected, places=2)

    def test_get_item_count(self):
        """get_item_count returns the sum of all unit quantities."""
        self.assertEqual(self.cart.get_item_count(), 6)


# ---------------------------------------------------------------------------
# 5. Checkout and Edge Cases
# ---------------------------------------------------------------------------

class TestCheckoutAndEdgeCases(unittest.TestCase):
    """Tests for checkout behaviour and miscellaneous edge cases."""

    REQUIRED_SUMMARY_KEYS = {
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

    def setUp(self):
        mock_inventory = MagicMock(spec=InventoryService)
        mock_inventory.get_stock.return_value = 50
        self.cart = ShoppingCart(
            inventory_service=mock_inventory, customer_id="test-user"
        )

    def test_checkout_populated_cart_returns_summary(self):
        """checkout on a populated cart returns a dict with all required keys."""
        self.cart.add_item("SKU-001", 1)
        summary = self.cart.checkout()
        self.assertIsInstance(summary, dict)
        self.assertTrue(self.REQUIRED_SUMMARY_KEYS.issubset(summary.keys()))

    def test_checkout_summary_values_are_correct(self):
        """checkout summary values match the cart's computed totals."""
        self.cart.add_item("SKU-001", 2)
        self.cart.apply_discount_code("SAVE10")
        summary = self.cart.checkout()
        self.assertEqual(summary["customer_id"], "test-user")
        self.assertAlmostEqual(summary["subtotal"], self.cart.get_subtotal(), places=2)
        self.assertAlmostEqual(summary["tax"], self.cart.get_tax(), places=2)
        self.assertAlmostEqual(summary["total"], self.cart.get_total(), places=2)
        self.assertEqual(summary["discount_code"], "SAVE10")

    def test_checkout_empty_cart_raises_empty_cart_error(self):
        """checkout on an empty cart raises EmptyCartError."""
        with self.assertRaises(EmptyCartError):
            self.cart.checkout()

    def test_clear_removes_all_items(self):
        """clear() empties the cart."""
        self.cart.add_item("SKU-001", 2)
        self.cart.add_item("SKU-002", 1)
        self.cart.clear()
        self.assertTrue(self.cart.is_empty())

    def test_clear_resets_discount_code(self):
        """clear() removes the applied discount code."""
        self.cart.add_item("SKU-001", 1)
        self.cart.apply_discount_code("SAVE10")
        self.cart.clear()
        self.assertEqual(self.cart.get_discount_amount(), 0.0)

    def test_add_item_zero_quantity_raises_invalid_quantity(self):
        """add_item with quantity=0 raises InvalidQuantityError."""
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item("SKU-001", 0)

    def test_add_item_negative_quantity_raises_invalid_quantity(self):
        """add_item with a negative quantity raises InvalidQuantityError."""
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item("SKU-001", -5)

    def test_remove_item_not_in_cart_raises_error(self):
        """remove_item for an SKU not in the cart raises CartItemNotFoundError."""
        with self.assertRaises(CartItemNotFoundError):
            self.cart.remove_item("SKU-002")

    def test_update_quantity_not_in_cart_raises_error(self):
        """update_quantity for an SKU not in the cart raises CartItemNotFoundError."""
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity("SKU-002", 3)

    def test_add_item_unknown_sku_raises_item_not_found(self):
        """add_item with a SKU absent from the catalogue raises ItemNotFoundError."""
        with self.assertRaises(ItemNotFoundError):
            self.cart.add_item("SKU-999", 1)

    def test_is_empty_on_new_cart(self):
        """A freshly created cart reports itself as empty."""
        self.assertTrue(self.cart.is_empty())

    def test_is_empty_false_after_add(self):
        """is_empty returns False once an item has been added."""
        self.cart.add_item("SKU-001", 1)
        self.assertFalse(self.cart.is_empty())

    def test_all_cart_errors_inherit_from_cart_error(self):
        """All custom exceptions are subclasses of CartError."""
        for exc_cls in (
            ItemNotFoundError,
            InsufficientStockError,
            InvalidQuantityError,
            InvalidDiscountCodeError,
            EmptyCartError,
            CartItemNotFoundError,
        ):
            self.assertTrue(
                issubclass(exc_cls, CartError),
                f"{exc_cls.__name__} should inherit from CartError",
            )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()