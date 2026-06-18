# libraries
from datetime import date
import unittest
from unittest.mock import patch, MagicMock
from pricing import PricingService
from inventory import InventoryService
from cart import ShoppingCart
from cart_exceptions import CartError, ItemNotFoundError, InsufficientStockError, InvalidDiscountCodeError, InvalidQuantityError, EmptyCartError, CartItemNotFoundError

# 1. Item Management
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
        self.assertEqual(items[0]["quantity"], 2)
        self.assertEqual(items[0]["name"], "Wireless Keyboard")
        self.assertEqual(items[0]["unit_price"], 49.99)
        self.assertEqual(items[0]["category"], "Electronics")
    
    # add_item using default quanitity
    def test_add_item_valid_default_quantity(self):
        self.cart.add_item("SKU-002")
        items = self.cart.get_items()
        self.assertEqual(len(items), 1)

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
        with self.assertRaises(CartItemNotFoundError):
            self.cart.remove_item("SKU-002")
    
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

# 2. Inventory Checks with Mocking
class TestInventoryMocking(unittest.TestCase):
    # ShoppingCart.add_item calls self._inventory.get_stock(sku) directly to
    # check live stock, so get_stock is the method to patch. Patching it here
    # means no real (simulated DB) inventory lookup ever runs in these tests.
    def setUp(self):
        self.cart = ShoppingCart()
        patcher = patch.object(InventoryService, "get_stock")
        self.mock_get_stock = patcher.start()
        self.addCleanup(patcher.stop)

    # ============================================================
    # sufficient stock -> item is added successfully
    def test_add_item_sufficient_stock(self):
        self.mock_get_stock.return_value = 100
        self.cart.add_item("SKU-001", 2)
        items = self.cart.get_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["quantity"], 2)

    # stock unavailable (0) -> InsufficientStockError raised
    def test_add_item_no_stock(self):
        self.mock_get_stock.return_value = 0
        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-001", 1)

    # available stock is lower than the requested quantity -> error raised
    def test_add_item_stock_lower_than_requested(self):
        self.mock_get_stock.return_value = 3
        with self.assertRaises(InsufficientStockError):
            self.cart.add_item("SKU-001", 5)

    # the patched method is actually invoked (with the right SKU) on add_item
    def test_get_stock_called_on_add(self):
        self.mock_get_stock.return_value = 50
        self.cart.add_item("SKU-001", 1)
        self.mock_get_stock.assert_called_once_with("SKU-001")


# 3. Discount Codes 
class TestDiscountCodes(unittest.TestCase):
    def setUp(self):
        self.pricing = PricingService()
    
    # ============================================================
    # VALIDATING DIFFERENT DISCOUNT CODES
    def test_validate_code_save10(self):
        discount = self.pricing.validate_discount_code("SAVE10")
        self.assertEqual(discount["type"], "percent")
        self.assertEqual(discount["value"], 10)
        self.assertEqual(discount["expires"], date(2099, 12, 31))
    def test_validate_code_save20(self):
        discount = self.pricing.validate_discount_code("SAVE20")
        self.assertEqual(discount["type"], "percent")
        self.assertEqual(discount["value"], 20)
        self.assertEqual(discount["expires"], date(2099, 12, 31))
    def test_validate_code_flat5(self):
        discount = self.pricing.validate_discount_code("FLAT5")
        self.assertEqual(discount["type"], "flat")
        self.assertEqual(discount["value"], 5.00)
        self.assertEqual(discount["expires"], date(2099, 12, 31))
    def test_validate_code_flat15(self):
        discount = self.pricing.validate_discount_code("FLAT15")
        self.assertEqual(discount["type"], "flat")
        self.assertEqual(discount["value"], 15.00)
        self.assertEqual(discount["expires"], date(2099, 12, 31))
    def test_validate_code_expired50(self):
        with self.assertRaises(InvalidDiscountCodeError):
            self.pricing.validate_discount_code("EXPIRED50")
    
    def test_validate_code_bad_code(self):
        with self.assertRaises(InvalidDiscountCodeError):
            self.pricing.validate_discount_code("SAVE30")

# 4. Pricing & Tax Calculations
class TestPricingAndTax(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    # Fixed cart configuration used for the pricing/tax assertions.
    # Spans three tax categories so tax is exercised across rates:
    #   SKU-001 x2  -> Wireless Keyboard, 49.99, Electronics (8%)
    #   SKU-004 x1  -> Desk Lamp,         24.99, Home Office (6%)
    #   SKU-005 x1  -> Notebook,          12.99, Stationery (5%)
    # Resulting known values:
    #   subtotal = 137.96, tax = 10.15
    def _populate_fixed_cart(self):
        self.cart.add_item("SKU-001", 2)
        self.cart.add_item("SKU-004", 1)
        self.cart.add_item("SKU-005", 1)

    # ============================================================
    # SUBTOTAL
    # empty cart 
    def test_get_subtotal_empty(self):
        self.assertEqual(self.cart.get_subtotal(), 0.0)

    # cart with items
    def test_get_subtotal_one_item(self):
        self.cart.add_item("SKU-001", 1)
        self.assertEqual(self.cart.get_subtotal(), 49.99)
    
    # more than one item in cart
    def test_get_subtotal_multiple_items(self):
        self.cart.add_item("SKU-001", 1)
        self.cart.add_item("SKU-002", 2)
        self.assertEqual(self.cart.get_subtotal(), 119.97)

    # subtotal of the fixed cart configuration
    def test_get_subtotal_fixed_cart(self):
        self._populate_fixed_cart()
        self.assertEqual(self.cart.get_subtotal(), 137.96)

    # ============================================================
    # DISCOUNT AMOUNT
    # no discount code -> 0
    def test_discount_amount_no_discount(self):
        self.cart.add_item("SKU-001")
        self.assertEqual(self.cart.get_discount_amount(), 0.0)

    # empty cart with no discount code -> 0
    def test_discount_amount_empty_cart(self):
        self.assertEqual(self.cart.get_discount_amount(), 0.0)

    # percentage-based discount code on the fixed cart
    def test_discount_amount_percent_code(self):
        self._populate_fixed_cart()
        self.cart.apply_discount_code("SAVE10")
        self.assertEqual(self.cart.get_discount_amount(), 13.8)

    # flat-rate discount code on the fixed cart
    def test_discount_amount_flat_code(self):
        self._populate_fixed_cart()
        self.cart.apply_discount_code("FLAT15")
        self.assertEqual(self.cart.get_discount_amount(), 15.0)

    # removing an applied code resets the discount back to 0
    def test_discount_amount_after_removal(self):
        self._populate_fixed_cart()
        self.cart.apply_discount_code("SAVE10")
        self.cart.remove_discount_code()
        self.assertEqual(self.cart.get_discount_amount(), 0.0)

    # applying an unrecognised code raises InvalidDiscountCodeError
    def test_apply_invalid_code_raises(self):
        self._populate_fixed_cart()
        with self.assertRaises(InvalidDiscountCodeError):
            self.cart.apply_discount_code("SAVE30")

    # applying an expired code raises InvalidDiscountCodeError
    def test_apply_expired_code_raises(self):
        self._populate_fixed_cart()
        with self.assertRaises(InvalidDiscountCodeError):
            self.cart.apply_discount_code("EXPIRED50")

    # ============================================================
    # TAX
    # empty cart has no tax
    def test_get_tax_empty_cart(self):
        self.assertEqual(self.cart.get_tax(), 0.0)

    # single-category tax: SKU-001 x1 (Electronics 8%) -> 49.99 * 0.08
    def test_get_tax_single_item(self):
        self.cart.add_item("SKU-001", 1)
        self.assertEqual(self.cart.get_tax(), 4.0)

    # tax across multiple categories on the fixed cart
    def test_get_tax_fixed_cart(self):
        self._populate_fixed_cart()
        self.assertEqual(self.cart.get_tax(), 10.15)

    # ============================================================
    # TOTAL
    # empty cart total is 0
    def test_get_total_empty_cart(self):
        self.assertEqual(self.cart.get_total(), 0.0)

    # total with no discount: subtotal + tax
    def test_get_total_no_discount(self):
        self._populate_fixed_cart()
        self.assertEqual(self.cart.get_total(), 148.11)

    # total with a percentage discount applied
    def test_get_total_percent_discount(self):
        self._populate_fixed_cart()
        self.cart.apply_discount_code("SAVE10")
        self.assertEqual(self.cart.get_total(), 134.31)

    # total with a flat discount applied
    def test_get_total_flat_discount(self):
        self._populate_fixed_cart()
        self.cart.apply_discount_code("FLAT15")
        self.assertEqual(self.cart.get_total(), 133.11)

    # total is exactly subtotal - discount + tax
    def test_get_total_is_subtotal_minus_discount_plus_tax(self):
        self._populate_fixed_cart()
        self.cart.apply_discount_code("SAVE10")
        expected = round(
            self.cart.get_subtotal()
            - self.cart.get_discount_amount()
            + self.cart.get_tax(),
            2,
        )
        self.assertEqual(self.cart.get_total(), expected)

# 5. Checkout & Edge Cases  
class TestCheckoutEdgeCases(unittest.TestCase):
    # set up 
    def setUp(self):
        self.cart = ShoppingCart()

    # ============================================================
    # CHECKOUT

    # populated cart has correct summary (with all keys present)
    def test_populated_cart_summary(self):
        self.cart.add_item("SKU-001")
        summary = self.cart.checkout()
        self.assertIn("customer_id", summary)
        self.assertIn("timestamp", summary)
        self.assertIn("items", summary)
        self.assertIn("subtotal", summary)
        self.assertIn("discount_code", summary)
        self.assertIn("discount_amount", summary)
        self.assertIn("tax", summary)
        self.assertIn("total", summary)
        self.assertIn("item_count", summary)

    # raises error for empty cart
    def test_empty_cart_summary(self):
        with self.assertRaises(EmptyCartError):
            self.cart.checkout()

    # ============================================================
    # CLEAR
    def test_clear(self):
        self.cart.add_item("SKU-001", 5)
        self.cart.apply_discount_code("SAVE10")
        self.cart.clear()
        items = self.cart.get_items() # should be empty
        self.assertEqual(len(items), 0)
        self.assertIsNone(self.cart._discount_code)
    
    
