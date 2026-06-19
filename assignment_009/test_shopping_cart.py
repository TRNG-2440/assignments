import unittest
from unittest.mock import patch, MagicMock
from cart import ShoppingCart
from cart_exceptions import CartError, InsufficientStockError
from inventory import InventoryService
from pricing import PricingService

class TestShopping(unittest.TestCase):
    # Testing Fixtures
    def setUp(self):
        self.test_inventory_service = InventoryService()
        self.test_pricing_service = PricingService()
        self.test_cart = ShoppingCart(self.test_inventory_service, self.test_pricing_service)
        
    def tearDown(self):
        pass    # Probably no need to implement
                # We do not need to actually tear anything down
    
    # Testing ShoppingCart (using inventory service)
    def test_shopping_cart_add_item(self): # Check if an item is added successfully
        self.test_cart.add_item("SKU-001")
        self.assertIn("SKU-001", self.test_cart._items) # Double checking its in there
        self.assertEqual(self.test_cart._items["SKU-001"]["quantity"], 1) # Confirm there is one        
    
    def test_shopping_cart_remove_item(self):
        self.test_cart.add_item("SKU-001") # Add Item
        self.test_cart.remove_item("SKU-001") 
        self.assertNotIn("SKU-001", self.test_cart._items) # Check SKU-001 not in the items list
    
    def test_shopping_cart_update_quantity(self):
        self.test_cart.add_item("SKU-001") # Add Item
        self.assertEqual(self.test_cart._items["SKU-001"]["quantity"], 1) # Confirm there is one
        self.test_cart.update_quantity("SKU-001", 10) # Change to 10
        self.assertEqual(self.test_cart._items["SKU-001"]["quantity"], 10) # Confirm there are 10
    
    # Testing with mocking enabled
    @patch.object(InventoryService, "get_stock")
    def test_enough_stock_available(self, mock_get_stock):
        mock_get_stock.return_value = 10000
        self.test_cart.add_item("SKU-001", 5000)
        self.assertIn("SKU-001", self.test_cart._items) # Double checking its in there
        self.assertEqual(self.test_cart._items["SKU-001"]["quantity"], 5000) # Confirm there is one        
        mock_get_stock.assert_called_once_with("SKU-001")
    
    @patch.object(InventoryService, "get_stock")
    def test_no_stock_available(self, mock_get_stock):
        mock_get_stock.return_value = 0
        with self.assertRaises(InsufficientStockError):
            self.test_cart.add_item("SKU-001")
        mock_get_stock.assert_called_once_with("SKU-001")
        
    @patch.object(InventoryService, "get_stock")
    def test_lower_stock_than_requested(self, mock_get_stock):
        mock_get_stock.return_value = 1
        with self.assertRaises(InsufficientStockError):
            self.test_cart.add_item("SKU-001", 2)
        self.assertIn("SKU-001", self.test_cart._items) # Double checking its in there
        self.assertEqual(self.test_cart._items["SKU-001"]["quantity"], 1) # Confirm there is one        
        mock_get_stock.assert_called_once_with("SKU-001")
    
    # Testing Discount Codes (full coverage of discount code behavior)
        # ensure that all codes apply discounts correctly against known subtotals
    def test_percentage_based_code():
        pass
    def test_flat_rate_code():
        pass
    def test_invalid_code():
        pass
    def test_expired_code():
        pass
    def test_removing_applied_code():
        pass

    # Testing Pricing and tax calculations
    def test_get_subtotal():
        pass
    def test_get_discount_code():
        pass
    def test_get_tax():
        pass
    def test_get_total():
        pass

    # Checkout and edge cases
    def test_checkout_populated_cart():
        pass
    def test_checkout_empty_cart():
        pass
    def test_call_clear_resets_all():
        pass
    def test_invalid_quantity_error():
        pass
    def test_cart_item_not_found():
        pass
    def test_item_not_found():
        pass