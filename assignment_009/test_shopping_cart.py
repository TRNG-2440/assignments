import unittest
from unittest.mock import patch, MagicMock
from cart import ShoppingCart
from cart_exceptions import CartError, InsufficientStockError, InvalidDiscountCodeError, InvalidQuantityError, CartItemNotFoundError, ItemNotFoundError, EmptyCartError
from inventory import InventoryService
from pricing import PricingService
from datetime import datetime

class TestShoppingCart(unittest.TestCase):
    # Testing Fixtures
    def setUp(self):
        self.test_inventory_service = InventoryService()
        self.test_pricing_service = PricingService()
        self.test_cart = ShoppingCart(self.test_inventory_service, self.test_pricing_service)
        
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
    
class TestShoppingCartWithMocking(unittest.TestCase):
    # Testing Fixtures
    def setUp(self):
        self.test_inventory_service = InventoryService()
        self.test_pricing_service = PricingService()
        self.test_cart = ShoppingCart(self.test_inventory_service, self.test_pricing_service)

    @patch.object(InventoryService, "get_stock")
    def test_enough_stock_available(self, mock_get_stock):
        mock_get_stock.return_value = 10000
        self.test_cart.add_item("SKU-001", 5000)
        self.assertIn("SKU-001", self.test_cart._items) # Double checking its in there
        self.assertEqual(self.test_cart._items["SKU-001"]["quantity"], 5000) # Confirm there is one        
        mock_get_stock.assert_called_once_with("SKU-001") # Asserting mock method was called
    
    @patch.object(InventoryService, "get_stock")
    def test_no_stock_available(self, mock_get_stock):
        mock_get_stock.return_value = 0
        with self.assertRaises(InsufficientStockError) as isem:
            self.test_cart.add_item("SKU-001")
        
        # The following checks the error message to ensure it is all correct
        self.assertEqual(str(isem.exception), "Insufficient stock for SKU 'SKU-001': requested 1, only 0 available.")
        
        mock_get_stock.assert_called_once_with("SKU-001") # Asserting mock method was called
        
    @patch.object(InventoryService, "get_stock")
    def test_lower_stock_than_requested(self, mock_get_stock):
        mock_get_stock.return_value = 1
        with self.assertRaises(InsufficientStockError) as isem:
            self.test_cart.add_item("SKU-001", 2) # Checking SKU cannot be added due to insufficient stock
        
        # The following checks the error message to ensure it is all correct
        self.assertEqual(str(isem.exception), "Insufficient stock for SKU 'SKU-001': requested 2, only 1 available.")
        
        with self.assertRaises(KeyError):
            self.test_cart._items["SKU-001"] # Double checking sku not present    
        mock_get_stock.assert_called_once_with("SKU-001") # Asserting mock method was called
    
class TestDiscountCodes(unittest.TestCase):
    # Testing Fixtures
    def setUp(self):
        self.test_inventory_service = InventoryService()
        self.test_pricing_service = PricingService()
        self.test_cart = ShoppingCart(self.test_inventory_service, self.test_pricing_service)
    
    # ensure that all codes apply discounts correctly against known subtotals
    def test_percentage_based_code(self):
        subtotal = self.test_pricing_service.apply_discount(10, "SAVE10")
        # 10% of 10 is 1. Should return 9
        self.assertEqual(9.00, subtotal)
        
        subtotal = self.test_pricing_service.apply_discount(10, "SAVE20")
        # 20% of 10 is 2. Should return 8
        self.assertEqual(8.00, subtotal)
        
    def test_flat_rate_code(self):
        subtotal = self.test_pricing_service.apply_discount(20, "FLAT5")
        # 20 minus 5 is 15
        self.assertEqual(15.00, subtotal)
        
        subtotal = self.test_pricing_service.apply_discount(20, "FLAT15")
        # 20 minus 15 is 5
        self.assertEqual(5.00, subtotal)
        
    # Looking for InvalidDiscountCodeError
    def test_invalid_code(self):
        with self.assertRaises(InvalidDiscountCodeError) as idcem:
            self.test_pricing_service.apply_discount(100, "INVALID100")
        self.assertEqual(str(idcem.exception), "Discount code 'INVALID100' is invalid or expired.")
    
    def test_expired_code(self):
        with self.assertRaises(InvalidDiscountCodeError) as idcem:
            self.test_pricing_service.apply_discount(100, "EXPIRED50")
        self.assertEqual(str(idcem.exception), "Discount code 'EXPIRED50' is expired.")
    
    @patch.object(InventoryService, "get_stock")
    def test_removing_applied_code(self, mock_get_stock):
        mock_get_stock.return_value = 10000
        self.test_cart.add_item("SKU-001") # Worth 49.99, so discount should be less
        mock_get_stock.assert_called_once_with("SKU-001") # Asserting mock method was called
        
        # Should return 0, since there is no discount code present
        self.assertEqual(self.test_cart.get_discount_amount(), 0.00)
        
        # Add 15 dollar discount, then check if it exists
        self.test_cart.apply_discount_code("FLAT15")
        self.assertEqual(self.test_cart.get_discount_amount(), 15.00)
        
        # Finally, remove 15 dollar discount, check it is removed
        self.test_cart.remove_discount_code()
        self.assertEqual(self.test_cart.get_discount_amount(), 0.00)

class TestPricingAndTaxCalculations(unittest.TestCase):
    # Testing Fixtures, including preset cart
    @patch.object(InventoryService, "get_stock")
    def setUp(self, mock_get_stock):
        self.test_inventory_service = InventoryService()
        self.test_pricing_service = PricingService()
        self.test_cart = ShoppingCart(self.test_inventory_service, self.test_pricing_service)
        
        # Mock
        mock_get_stock.return_value = 1000
        self.test_cart.add_item("SKU-001")
        self.test_cart.add_item("SKU-004")
        self.test_cart.add_item("SKU-005")
    
    # Note:
        # "SKU-001" costs 49.99, has 0.08 Tax Rate (Total 53.99)
        # "SKU-004" costs 24.99, has 0.06 Tax Rate (Total 26.49)
        # "SKU-005" costs 12.99, has 0.05 Tax Rate (Total 13.64)
        # Sub total Should be 49.99 + 24.99 + 12.99 = 87.97
        # Total should be 94.12
    
    def test_get_subtotal(self):
        # Get Subtotal and validate
        test_subtotal = self.test_cart.get_subtotal()
        self.assertEqual(87.97, test_subtotal)

    def test_get_discount_amount(self):
        # Get Flat Discount and validate
        self.test_cart.apply_discount_code("FLAT15")
        test_discount_amount = self.test_cart.get_discount_amount()
        self.assertEqual(15.00, test_discount_amount)
        
        # Get Percent Discount and validate
        self.test_cart.apply_discount_code("SAVE10")
        test_discount_amount = self.test_cart.get_discount_amount()
        self.assertEqual(8.80, test_discount_amount) # 10% of 87.97 is 8.797 ~= 8.80
            
    def test_get_tax(self):
        
        # Get Tax and validate
        test_tax_amount = self.test_cart.get_tax()  # Tax Should be 6.15
        self.assertEqual(6.15, test_tax_amount)
    
    def test_get_total(self):    
        # Get total and validate
        test_total_amount = self.test_cart.get_total() # Should be 94.12
        self.assertEqual(94.12, test_total_amount)
        
        # Get total and validate again with discount code
        self.test_cart.apply_discount_code("FLAT15")
        test_total_amount = self.test_cart.get_total() # Should be 79.12
        self.assertEqual(79.12, test_total_amount)

'''
summary = {
            "customer_id":       self._customer_id,
            "timestamp":         datetime.now().isoformat(),
            "items":             self.get_items(),
            "subtotal":          self.get_subtotal(),
            "discount_code":     self._discount_code,
            "discount_amount":   self.get_discount_amount(),
            "tax":               self.get_tax(),
            "total":             self.get_total(),
            "item_count":        self.get_item_count(),
        }
'''

class TestCheckoutAndEdgeCases(unittest.TestCase):
    # Testing Fixtures
    def setUp(self):
        self.test_inventory_service = InventoryService()
        self.test_pricing_service = PricingService()
        self.test_cart = ShoppingCart(self.test_inventory_service, self.test_pricing_service)
    
    @patch.object(InventoryService, "get_stock")
    def test_checkout_populated_cart(self, mock_get_stock):
        # Populate cart, fill all values, then test
        mock_get_stock.return_value = 10000
        self.test_cart.add_item("SKU-001")
        self.test_cart.add_item("SKU-004")
        self.test_cart.add_item("SKU-005")
        self.assertEqual(mock_get_stock.call_count, 3)
        
        self.test_cart.apply_discount_code("FLAT15")
        
        # Get time (for later validation), then checkout
        test_time = datetime.now().isoformat()
        test_checkoutDict = self.test_cart.checkout()
        
        # Test all values in the summary
        self.assertEqual(test_checkoutDict["customer_id"], "guest")
        self.assertEqual(test_checkoutDict["timestamp"], test_time)
        self.assertTrue(any(item.get('sku') == "SKU-001" for item in test_checkoutDict["items"]))
        self.assertTrue(any(item.get('sku') == "SKU-004" for item in test_checkoutDict["items"]))
        self.assertTrue(any(item.get('sku') == "SKU-005" for item in test_checkoutDict["items"]))
        self.assertEqual(test_checkoutDict["subtotal"], 87.97)
        self.assertEqual(test_checkoutDict["discount_code"], "FLAT15")
        self.assertEqual(test_checkoutDict["discount_amount"], 15)
        self.assertEqual(test_checkoutDict["tax"], 6.15)
        self.assertEqual(test_checkoutDict["total"], 79.12)
        self.assertEqual(test_checkoutDict["item_count"], 3)
        
    
    def test_checkout_empty_cart(self):
        with self.assertRaises(EmptyCartError):
            self.test_cart.checkout()
    
    @patch.object(InventoryService, "get_stock")
    def test_call_clear_resets_all(self, mock_get_stock):
        mock_get_stock.return_value = 10000
        self.test_cart.add_item("SKU-001")
        self.test_cart.add_item("SKU-004")
        self.test_cart.add_item("SKU-005")
        self.assertEqual(mock_get_stock.call_count, 3)
        # Checkout, ensure something is output (meaning there are items in cart)
        testing_checkoutDict = self.test_cart.checkout()
        self.assertIsNotNone(testing_checkoutDict)
        
    
    @patch.object(InventoryService, "get_stock")
    def test_invalid_quantity_error(self, mock_get_stock):
        mock_get_stock.return_value = 10000
        with self.assertRaises(InvalidQuantityError):
            self.test_cart.add_item("SKU-001", 0)
        with self.assertRaises(InvalidQuantityError):
            self.test_cart.add_item("SKU-001", -100)
        
    def test_cart_item_not_found(self):
        with self.assertRaises(CartItemNotFoundError):
            self.test_cart.update_quantity("SKU-100", 10000000)
        with self.assertRaises(CartItemNotFoundError):
            self.test_cart.remove_item("SKU-200")
    
    @patch.object(InventoryService, "get_stock")
    def test_item_not_found(self, mock_get_stock):
        mock_get_stock.return_value = 10000
        self.test_cart.add_item("SKU-001")
        self.test_cart.add_item("SKU-004")
        self.test_cart.add_item("SKU-005")
        self.assertEqual(mock_get_stock.call_count, 3)
        with self.assertRaises(ItemNotFoundError):
            self.test_cart.add_item("SKU-200")
    