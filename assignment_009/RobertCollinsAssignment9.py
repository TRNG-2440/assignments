import unittest
from unittest.mock import patch, MagicMock
from cart import ShoppingCart
from cart_exceptions import (
    CartError, 
    InvalidQuantityError, 
    CartItemNotFoundError,
    EmptyCartError,
    ItemNotFoundError,
    InsufficientStockError
)

# Import these based on actual module structure
# from catalogue import PRODUCT_CATALOGUE, DISCOUNT_CODES
# from inventory import InventoryService
# from pricing import PricingService


class TestItemManagement(unittest.TestCase):
    """Test Case 1: Item Management - add_item, remove_item, update_quantity"""
    
    def setUp(self):
        """Create a fresh shopping cart before each test"""
        self.cart = ShoppingCart()
        
        # Assume these are valid SKUs from catalogue
        self.valid_sku_1 = "SKU001"  # e.g., Laptop - $999.99
        self.valid_sku_2 = "SKU002"  # e.g., Mouse - $29.99
        self.invalid_sku = "SKU999"
    
    def test_add_item_valid(self):
        """Test adding a valid item to cart"""
        self.cart.add_item(self.valid_sku_1, quantity=1)
        # Verify item was added (implementation depends on cart structure)
        self.assertEqual(len(self.cart.items), 1)
    
    def test_add_item_duplicate_sku_accumulates(self):
        """Test adding same SKU multiple times increases quantity"""
        self.cart.add_item(self.valid_sku_1, quantity=2)
        self.cart.add_item(self.valid_sku_1, quantity=3)
        # Should now have 5 total of this SKU
        self.assertEqual(self.cart.items[self.valid_sku_1], 5)
    
    def test_add_item_invalid_sku_raises_error(self):
        """Test adding non-existent SKU raises ItemNotFoundError"""
        with self.assertRaises(ItemNotFoundError):
            self.cart.add_item(self.invalid_sku, quantity=1)
    
    def test_add_item_invalid_quantity_raises_error(self):
        """Test adding zero or negative quantity raises InvalidQuantityError"""
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item(self.valid_sku_1, quantity=0)
        
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item(self.valid_sku_1, quantity=-5)
    
    def test_add_item_insufficient_stock_raises_error(self):
        """Test adding more than available stock raises InsufficientStockError"""
        # Assume inventory only has 10 of this item
        with self.assertRaises(InsufficientStockError):
            self.cart.add_item(self.valid_sku_1, quantity=100)
    
    def test_remove_item_successful(self):
        """Test successful removal of an item from cart"""
        self.cart.add_item(self.valid_sku_1, quantity=2)
        self.cart.remove_item(self.valid_sku_1)
        self.assertNotIn(self.valid_sku_1, self.cart.items)
    
    def test_remove_item_not_in_cart_raises_error(self):
        """Test removing item not in cart raises CartItemNotFoundError"""
        with self.assertRaises(CartItemNotFoundError):
            self.cart.remove_item(self.valid_sku_1)
    
    def test_update_quantity_valid(self):
        """Test updating quantity of existing item"""
        self.cart.add_item(self.valid_sku_1, quantity=2)
        self.cart.update_quantity(self.valid_sku_1, 5)
        self.assertEqual(self.cart.items[self.valid_sku_1], 5)
    
    def test_update_quantity_invalid_quantity_raises_error(self):
        """Test updating to zero or negative quantity raises error"""
        self.cart.add_item(self.valid_sku_1, quantity=2)
        
        with self.assertRaises(InvalidQuantityError):
            self.cart.update_quantity(self.valid_sku_1, 0)
        
        with self.assertRaises(InvalidQuantityError):
            self.cart.update_quantity(self.valid_sku_1, -3)
    
    def test_update_quantity_insufficient_stock_raises_error(self):
        """Test updating to quantity exceeding stock raises error"""
        self.cart.add_item(self.valid_sku_1, quantity=2)
        
        with self.assertRaises(InsufficientStockError):
            self.cart.update_quantity(self.valid_sku_1, 100)
    
    def test_update_quantity_item_not_in_cart_raises_error(self):
        """Test updating item not in cart raises CartItemNotFoundError"""
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity(self.valid_sku_1, 5)


class TestInventoryChecksWithMocking(unittest.TestCase):
    """Test Case 2: Inventory Checks - using mocks to isolate ShoppingCart"""
    
    def setUp(self):
        """Create a fresh shopping cart before each test"""
        self.cart = ShoppingCart()
        self.valid_sku = "SKU001"
    
    @patch('inventory.InventoryService.check_stock')
    def test_add_item_sufficient_stock_available(self, mock_check_stock):
        """Test item added successfully when stock is sufficient"""
        # Mock the inventory service to return high stock
        mock_check_stock.return_value = 50
        
        self.cart.add_item(self.valid_sku, quantity=10)
        
        # Verify the mock was called with correct SKU
        mock_check_stock.assert_called_once_with(self.valid_sku)
        
        # Verify item was added to cart
        self.assertEqual(self.cart.items[self.valid_sku], 10)
    
    @patch('inventory.InventoryService.check_stock')
    def test_add_item_stock_unavailable_raises_error(self, mock_check_stock):
        """Test adding item raises error when stock is insufficient"""
        # Mock inventory to show low stock
        mock_check_stock.return_value = 5
        
        with self.assertRaises(InsufficientStockError):
            self.cart.add_item(self.valid_sku, quantity=10)
        
        # Verify inventory was checked
        mock_check_stock.assert_called_once_with(self.valid_sku)
        
        # Verify item was NOT added to cart
        self.assertNotIn(self.valid_sku, self.cart.items)
    
    @patch('inventory.InventoryService.check_stock')
    def test_add_item_exact_stock_boundary(self, mock_check_stock):
        """Test edge case: requesting exactly available stock"""
        mock_check_stock.return_value = 10
        
        self.cart.add_item(self.valid_sku, quantity=10)
        
        mock_check_stock.assert_called_once_with(self.valid_sku)
        self.assertEqual(self.cart.items[self.valid_sku], 10)
    
    @patch('inventory.InventoryService.check_stock')
    def test_inventory_service_called_each_time(self, mock_check_stock):
        """Verify inventory service is called every time add_item is invoked"""
        mock_check_stock.return_value = 100
        
        self.cart.add_item(self.valid_sku, quantity=1)
        self.cart.add_item(self.valid_sku, quantity=2)
        
        # Should be called twice - once per add_item call
        self.assertEqual(mock_check_stock.call_count, 2)


class TestDiscountCodes(unittest.TestCase):
    """Test Case 3: Discount Codes - validation, application, and removal"""
    
    def setUp(self):
        """Create a fresh shopping cart with some items before each test"""
        self.cart = ShoppingCart()
        
        # Add items to test discount calculations
        # Assume product prices: SKU001=$100, SKU002=$50
        self.cart.add_item("SKU001", quantity=2)  # $200 subtotal
        self.cart.add_item("SKU002", quantity=1)  # $50 subtotal
        # Total subtotal = $250
    
    def test_valid_percentage_discount(self):
        """Test applying valid percentage discount code"""
        # Assume discount code "SAVE10" gives 10% off
        self.cart.apply_discount("SAVE10")
        
        # 10% of $250 = $25 discount
        self.assertEqual(self.cart.get_discount_amount(), 25)
    
    def test_valid_flat_discount(self):
        """Test applying valid flat discount code"""
        # Assume discount code "FLAT20" gives $20 off
        self.cart.apply_discount("FLAT20")
        
        self.assertEqual(self.cart.get_discount_amount(), 20)
    
    def test_expired_discount_code_raises_error(self):
        """Test expired discount code raises appropriate exception"""
        # Assume "EXPIRED" is past its valid date
        with self.assertRaises(CartError):  # Or specific DiscountExpiredError
            self.cart.apply_discount("EXPIRED")
    
    def test_unrecognized_discount_code_raises_error(self):
        """Test invalid discount code raises exception"""
        with self.assertRaises(CartError):  # Or InvalidDiscountCodeError
            self.cart.apply_discount("INVALID_CODE_123")
    
    def test_remove_applied_discount(self):
        """Test removing discount code after application"""
        self.cart.apply_discount("SAVE10")
        self.assertEqual(self.cart.get_discount_amount(), 25)
        
        self.cart.remove_discount()
        self.assertEqual(self.cart.get_discount_amount(), 0)
    
    def test_discount_affects_total_calculation(self):
        """Test that discount correctly reduces total"""
        self.cart.apply_discount("SAVE10")  # 10% off $250 = $25
        subtotal = self.cart.get_subtotal()  # $250
        discount = self.cart.get_discount_amount()  # $25
        tax = self.cart.get_tax()  # Assume 10% tax = $25
        total = self.cart.get_total()  # $250 - $25 + $25 = $250
        
        expected_total = subtotal - discount + tax
        self.assertEqual(total, expected_total)


class TestPricingAndTaxCalculations(unittest.TestCase):
    """Test Case 4: Pricing and Tax - calculations with known cart configuration"""
    
    def setUp(self):
        """Create a cart with fixed items for predictable calculations"""
        self.cart = ShoppingCart()
        
        # Known configuration - hardcoded expected values
        # Assume catalogue prices:
        # SKU001: Laptop - $999.99
        # SKU002: Mouse - $29.99
        # SKU003: Keyboard - $79.99
        # Tax rate: 10% (from catalogue.py)
        
        self.cart.add_item("SKU001", quantity=1)  # $999.99
        self.cart.add_item("SKU002", quantity=2)  # $59.98
        self.cart.add_item("SKU003", quantity=1)  # $79.99
        
        # Expected values (hardcoded based on above)
        self.expected_subtotal = 999.99 + 59.98 + 79.99  # $1139.96
        self.expected_tax_rate = 0.10  # 10%
        
    def test_get_subtotal_returns_correct_value(self):
        """Test subtotal calculation with multiple items"""
        subtotal = self.cart.get_subtotal()
        self.assertAlmostEqual(subtotal, self.expected_subtotal, places=2)
    
    def test_get_tax_returns_correct_value(self):
        """Test tax calculation based on subtotal"""
        expected_tax = self.expected_subtotal * self.expected_tax_rate
        self.assertAlmostEqual(self.cart.get_tax(), expected_tax, places=2)
    
    def test_get_discount_amount_zero_without_code(self):
        """Test discount amount is zero when no discount applied"""
        self.assertEqual(self.cart.get_discount_amount(), 0)
    
    def test_get_total_without_discount(self):
        """Test total = subtotal + tax when no discount"""
        expected_total = self.expected_subtotal + (self.expected_subtotal * self.expected_tax_rate)
        self.assertAlmostEqual(self.cart.get_total(), expected_total, places=2)
    
    def test_get_total_with_discount(self):
        """Test total = subtotal - discount + tax correctly combines"""
        self.cart.apply_discount("SAVE10")  # 10% off
        
        subtotal = self.cart.get_subtotal()
        discount = self.cart.get_discount_amount()
        tax = self.cart.get_tax()
        total = self.cart.get_total()
        
        expected_total = subtotal - discount + tax
        self.assertAlmostEqual(total, expected_total, places=2)
    
    def test_multiple_item_quantity_calculations(self):
        """Test calculations work correctly with different quantities"""
        # Reset cart with different quantities
        test_cart = ShoppingCart()
        test_cart.add_item("SKU002", quantity=5)  # 5 * $29.99 = $149.95
        
        self.assertAlmostEqual(test_cart.get_subtotal(), 149.95, places=2)


class TestCheckoutAndEdgeCases(unittest.TestCase):
    """Test Case 5: Checkout and Edge Cases - boundary conditions"""
    
    def setUp(self):
        """Create a fresh shopping cart before each test"""
        self.cart = ShoppingCart()
        self.valid_sku = "SKU001"
    
    def test_checkout_populated_cart_returns_summary_dict(self):
        """Test checkout returns dictionary with all required keys"""
        self.cart.add_item(self.valid_sku, quantity=2)
        self.cart.apply_discount("SAVE10")
        
        summary = self.cart.checkout()
        
        # Verify summary contains expected keys
        expected_keys = ['items', 'subtotal', 'discount', 'tax', 'total', 'timestamp']
        for key in expected_keys:
            self.assertIn(key, summary)
        
        # Verify values are correct types
        self.assertIsInstance(summary['items'], dict)
        self.assertIsInstance(summary['subtotal'], float)
        self.assertIsInstance(summary['total'], float)
    
    def test_checkout_empty_cart_raises_error(self):
        """Test checking out empty cart raises EmptyCartError"""
        with self.assertRaises(EmptyCartError):
            self.cart.checkout()
    
    def test_clear_resets_all_items(self):
        """Test clear method removes all items from cart"""
        self.cart.add_item(self.valid_sku, quantity=3)
        self.cart.add_item("SKU002", quantity=1)
        self.cart.apply_discount("SAVE10")
        
        self.assertEqual(len(self.cart.items), 2)
        self.assertIsNotNone(self.cart.discount_code)
        
        self.cart.clear()
        
        self.assertEqual(len(self.cart.items), 0)
        self.assertIsNone(self.cart.discount_code)
    
    def test_add_item_zero_quantity_raises_error(self):
        """Test adding item with zero quantity raises InvalidQuantityError"""
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item(self.valid_sku, quantity=0)
    
    def test_add_item_negative_quantity_raises_error(self):
        """Test adding item with negative quantity raises InvalidQuantityError"""
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item(self.valid_sku, quantity=-10)
    
    def test_remove_item_not_in_cart_raises_error(self):
        """Test removing non-existent item raises CartItemNotFoundError"""
        with self.assertRaises(CartItemNotFoundError):
            self.cart.remove_item("NONEXISTENT_SKU")
    
    def test_update_quantity_item_not_in_cart_raises_error(self):
        """Test updating quantity for item not in cart raises error"""
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity("NONEXISTENT_SKU", 5)
    
    def test_checkout_clears_cart_after_successful_checkout(self):
        """Test cart is cleared after successful checkout (if required by design)"""
        self.cart.add_item(self.valid_sku, quantity=1)
        self.cart.checkout()
        
        # After checkout, cart should be empty (depending on design)
        # Comment this if your cart doesn't auto-clear after checkout
        # self.assertEqual(len(self.cart.items), 0)
    
    def test_add_item_after_checkout_works_correctly(self):
        """Test cart can be reused after checkout"""
        self.cart.add_item(self.valid_sku, quantity=1)
        self.cart.checkout()
        
        # Should be able to add items again
        self.cart.add_item("SKU002", quantity=2)
        self.assertEqual(len(self.cart.items), 1)


# Additional optional test class for integration scenarios
class TestIntegrationScenarios(unittest.TestCase):
    """Bonus: Integration-like tests combining multiple features"""
    
    def setUp(self):
        self.cart = ShoppingCart()
    
    def test_full_shopping_workflow(self):
        """Test complete workflow: add items -> apply discount -> checkout"""
        # Add items
        self.cart.add_item("SKU001", quantity=1)
        self.cart.add_item("SKU002", quantity=3)
        
        # Apply discount
        self.cart.apply_discount("SAVE10")
        
        # Verify calculations
        subtotal = self.cart.get_subtotal()
        discount = self.cart.get_discount_amount()
        tax = self.cart.get_tax()
        total = self.cart.get_total()
        
        self.assertEqual(total, subtotal - discount + tax)
        
        # Checkout
        summary = self.cart.checkout()
        self.assertEqual(summary['total'], total)
    
    def test_multiple_discount_attempts(self):
        """Test applying new discount replaces old one"""
        self.cart.add_item("SKU001", quantity=1)
        
        self.cart.apply_discount("SAVE10")  # 10% off
        first_discount = self.cart.get_discount_amount()
        
        self.cart.apply_discount("FLAT20")  # $20 off
        second_discount = self.cart.get_discount_amount()
        
        self.assertNotEqual(first_discount, second_discount)


if __name__ == '__main__':
    # This allows running tests from command line
    unittest.main(verbosity=2)