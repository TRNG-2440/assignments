import unittest
from unittest.mock import patch, MagicMock
from cart import ShoppingCart
from cart_exceptions import CartError

class testShopping(unittest.TestCase):
    # Testing Fixtures
    def setUp(self):
        pass
    def tearDown(self):
        pass
    
    # Testing ShoppingCart
    def test_shopping_cart_add_item(self):
        pass
    def test_shopping_cart_remove_item(self):
        pass
    def test_shopping_cart_update_quantity(self):
        pass
    
    # Testing with mocking enabled
    def test_mocked_method_working(self):
        pass
    def test_enough_stock_available(self):
        pass
    def test_no_stock_available(self):
        pass
    def test_lower_stock_than_requested(self):
        pass
    
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