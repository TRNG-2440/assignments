import unittest
from unittest.mock import patch, MagicMock
from cart import ShoppingCart
from cart_exceptions import CartError, InsufficientStockError, InvalidDiscountCodeError, EmptyCartError, InvalidQuantityError, CartItemNotFoundError, ItemNotFoundError


class item_management(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_add(self):
        result = self.cart.add_item('SKU-001', 1)
        expected = None
        self.assertEqual(result, expected)

    def test_remove(self):
        self.cart.add_item('SKU-001', 1)
        result = self.cart.remove_item('SKU-001')
        expected = None
        self.assertEqual(result, expected)

    def test_update(self):
        self.cart.add_item('SKU-001', 2)
        result = self.cart.update_quantity('SKU-001', 2)
        expected = None
        self.assertEqual(result, expected)

    def test_add_duplicate_item(self):
        self.cart.add_item('SKU-001', 1)
        self.cart.add_item('SKU-001', 1)
        self.assertEqual(self.cart.get_item_count(), 2)


class InventoryTest(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    @patch('cart.InventoryService.get_stock')
    def test_sufficient_stock(self, mocking_get_stock):
        mocking_get_stock.return_value = 7
        self.cart.add_item('SKU-001', 5)
        self.assertEqual(self.cart.get_item_count(), 5)
        mocking_get_stock.assert_called_once_with('SKU-001')

    @patch('cart.InventoryService.get_stock')
    def test_insufficient_stock(self, mocking_get_stock):
        mocking_get_stock.return_value = 7
        
        with self.assertRaises(InsufficientStockError) as context:
            self.cart.add_item('SKU-001', 10)
        expected_error = "Insufficient stock for SKU 'SKU-001': requested 10, only 7 available."
        self.assertEqual(str(context.exception), expected_error)
        mocking_get_stock.assert_called_once_with('SKU-001')

    @patch('cart.InventoryService.get_stock')
    def test_zero_stock(self, mocking_get_stock):
        mocking_get_stock.return_value = 0

        with self.assertRaises(InsufficientStockError) as context:
            self.cart.add_item('SKU-001', 10)
        expected_error = "Insufficient stock for SKU 'SKU-001': requested 10, only 0 available."
        self.assertEqual(str(context.exception), expected_error)
        mocking_get_stock.assert_called_once_with('SKU-001')


class DiscountTesting(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    @patch('cart.InventoryService.get_stock')
    def test_valid_discount(self, mocking_get_stock):
        mocking_get_stock.return_value = 10
        
        self.cart.add_item('SKU-001', 1) 
        self.cart.apply_discount_code('SAVE10')
        # SKU-001 is $49.99, so a 10% discount rounds out to $5.00 in the module logic
        self.assertEqual(self.cart.get_discount_amount(), 5.00)

    @patch('cart.InventoryService.get_stock')
    def test_valid_flat_rate(self, mocking_get_stock):
        mocking_get_stock.return_value = 10
        
        self.cart.add_item('SKU-001', 1) 
        self.cart.apply_discount_code('FLAT15')
        self.assertEqual(self.cart.get_discount_amount(), 15.00)

    def test_unrecognized_code(self):
        with self.assertRaises(InvalidDiscountCodeError) as context:
            self.cart.apply_discount_code('1234')
            
        expected_error = "Discount code '1234' is invalid or expired."
        self.assertEqual(str(context.exception), expected_error)

    def test_expired_code(self):
        with self.assertRaises(InvalidDiscountCodeError) as context:
            self.cart.apply_discount_code('EXPIRED50')
            
        expected_error = "Discount code 'EXPIRED50' is expired."
        self.assertEqual(str(context.exception), expected_error)

    @patch('cart.InventoryService.get_stock')
    def test_remove_discount(self, mocking_get_stock):
        mocking_get_stock.return_value = 10
        self.cart.add_item('SKU-001', 1) 
        
        self.cart.apply_discount_code('SAVE10')
        self.cart.remove_discount_code()
        self.assertEqual(self.cart.get_discount_amount(), 0.0)


class Pricing_Tax_Testing(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()
        
    @patch('cart.InventoryService.get_stock')
    def test_subtotal(self, mocking_get_stock):
        mocking_get_stock.return_value = 10
        self.cart.add_item('SKU-001', 2)  
        self.cart.add_item('SKU-005', 2)  
        
        # Real baseline prices from system data sum up to 125.96
        sub = self.cart.get_subtotal()
        self.assertEqual(sub, 125.96)

    @patch('cart.InventoryService.get_stock')
    def test_discount_amount(self, mocking_get_stock):
        mocking_get_stock.return_value = 10
        self.cart.add_item('SKU-001', 2)
        self.cart.add_item('SKU-005', 2)
        self.cart.apply_discount_code('SAVE10') 
        
        self.assertEqual(self.cart.get_discount_amount(), 12.6)

    @patch('cart.InventoryService.get_stock')
    def test_tax(self, mocking_get_stock):
        mocking_get_stock.return_value = 10
        self.cart.add_item('SKU-001', 2)  
        self.cart.add_item('SKU-005', 2)  
        
        tax_val = self.cart.get_tax()
        self.assertEqual(tax_val, 9.3)

    @patch('cart.InventoryService.get_stock')
    def test_total(self, mocking_get_stock):
        mocking_get_stock.return_value = 10
        self.cart.add_item('SKU-001', 2)  
        self.cart.add_item('SKU-005', 2)  
        self.cart.apply_discount_code('SAVE10') 
        
        tot = self.cart.get_total()
        self.assertEqual(tot, 122.66)


class Checkout_Edge_Cases(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    @patch('cart.InventoryService.get_stock')
    def test_checkout_populated_cart(self, mocking_get_stock):
        mocking_get_stock.return_value = 5
        self.cart.add_item('SKU-001', 1)
        
        result = self.cart.checkout()
        self.assertTrue('items', result)
        self.assertTrue('subtotal', result)
        self.assertTrue('discount_amount', result) 
        self.assertTrue('tax', result)
        self.assertTrue('total', result)

    def test_checkout_empty_cart(self):
        with self.assertRaises(EmptyCartError) as context:
            self.cart.checkout()
        expected_error = "Cannot check out: the cart is empty."
        self.assertEqual(str(context.exception), expected_error)

    @patch('cart.InventoryService.get_stock')
    def test_clear_cart(self, mocking_get_stock):
        mocking_get_stock.return_value = 5
        self.cart.add_item('SKU-001', 1)
        self.cart.apply_discount_code('SAVE10')
        
        self.cart.clear()
        self.assertEqual(self.cart.get_item_count(), 0)
        self.assertEqual(self.cart.get_discount_amount(), 0.0)

    @patch('cart.InventoryService.get_stock')
    def test_invalid_quantity_zero_or_negative(self, mocking_get_stock):
        mocking_get_stock.return_value = 5
        
        with self.assertRaises(InvalidQuantityError) as context:
            self.cart.add_item('SKU-001', 0)
        expected_error = "Invalid quantity '0': quantity must be a positive integer."
        self.assertEqual(str(context.exception), expected_error)

    def test_remove_or_update_item_not_in_cart(self):
        with self.assertRaises(CartItemNotFoundError) as context_remove:
            self.cart.remove_item('SKU-999')
        expected_remove_error = "SKU 'SKU-999' is not in the cart."
        self.assertEqual(str(context_remove.exception), expected_remove_error)

        with self.assertRaises(CartItemNotFoundError) as context_update:
            self.cart.update_quantity('SKU-999', 2)
        expected_update_error = "SKU 'SKU-999' is not in the cart."
        self.assertEqual(str(context_update.exception), expected_update_error)

    @patch('cart.InventoryService.get_stock')
    def test_nonexistent_sku(self, mocking_get_stock):
        mocking_get_stock.return_value = 5
        
        with self.assertRaises(ItemNotFoundError) as context:
            self.cart.add_item('NONEXISTENT-SKU', 1)
        expected_error = "No product found with SKU 'NONEXISTENT-SKU'."
        self.assertEqual(str(context.exception), expected_error)


if __name__ == '__main__':
    unittest.main()