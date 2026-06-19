import unittest
from unittest.mock import Mock
from unittest.mock import patch, MagicMock
from cart import ShoppingCart
import cart_exceptions
from inventory import InventoryService

class TestItemManagement(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_item(self):
        self.cart.add_item("SKU-001")

        # testing for adding without a specified quantity
        sku = self.cart._items["SKU-001"]["sku"]
        self.assertEqual(sku, "SKU-001")
        quantity = self.cart._items["SKU-001"]["quantity"]
        self.assertEqual(quantity, 1)

        # testing for adding same sku into cart
        self.cart.add_item("SKU-001", 5)
        sku = self.cart._items["SKU-001"]["sku"]
        self.assertEqual(sku, "SKU-001")
        quantity = self.cart._items["SKU-001"]["quantity"]
        self.assertEqual(quantity, 6)

        # testing for adding another item
        self.cart.add_item("SKU-002", 3)
        sku = self.cart._items["SKU-002"]["sku"]
        self.assertEqual(sku, "SKU-002")
        quantity = self.cart._items["SKU-002"]["quantity"]
        self.assertEqual(quantity, 3)

    def test_remove_item(self):
        self.cart.add_item("SKU-001", 5)
        self.cart.add_item("SKU-002", 3)

        print (self.cart._items)
        
        # test to remove second item - FIX
        self.cart.remove_item("SKU-002")
        self.assertFalse("SKU-002" in self.cart._items)

    def test_update_quantity(self):
        self.cart.add_item("SKU-001", 5)
        self.cart.add_item("SKU-002", 3)

        self.cart.update_quantity("SKU-001", 9)

        quantity = self.cart._items["SKU-001"]["quantity"]
        self.assertEqual(quantity, 9)

class TestInventoryChecksWithMocking(unittest.TestCase):
    def setUp(self):
        self.mock_service = Mock(spec=InventoryService)
        self.cart = ShoppingCart(inventory_service=self.mock_service)

    def test_sufficient_stock(self):
        # set stock to 30 and add 5 to cart
        self.mock_service.get_stock.return_value = 30
        self.cart.add_item("SKU-001", 5)
        result_sku = self.cart.get_items()[0]["sku"]
        result_quantity = self.cart.get_items()[0]["quantity"]
        self.assertEqual(result_sku, "SKU-001")
        self.assertEqual(result_quantity, 5)
        self.mock_service.get_stock.assert_called_once() # test to see if mock service called

    def test_unavailable_stock(self):
        # set stock to 0 and add 5 to cart
        self.mock_service.get_stock.return_value = 0
        self.assertRaises(cart_exceptions.InsufficientStockError, self.cart.add_item, "SKU-001", 5)
        self.mock_service.get_stock.assert_called_once() # test to see if mock service called

    def test_insufficient_stock(self):
        # set stock to 10 and add 15 to cart
        self.mock_service.get_stock.return_value = 10
        self.assertRaises(cart_exceptions.InsufficientStockError, self.cart.add_item, "SKU-001", 15)
        self.mock_service.get_stock.assert_called_once() # test to see if mock service called

class TestDiscountCodes(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_valid_codes(self): 
        # exact string
        self.cart.apply_discount_code("SAVE10")
        self.assertEqual(self.cart._discount_code, "SAVE10")
        # some lower case
        self.cart.apply_discount_code("sAvE10")
        self.assertEqual(self.cart._discount_code, "SAVE10")
        # testing with whitespaces
        self.cart.apply_discount_code("  SAVE10  ")
        self.assertEqual(self.cart._discount_code, "SAVE10")

    def test_invalid_codes(self):
        # wrong string
        self.assertRaises(cart_exceptions.InvalidDiscountCodeError, self.cart.apply_discount_code, "save")

        # expired code
        self.assertRaises(cart_exceptions.InvalidDiscountCodeError, self.cart.apply_discount_code, "EXPIRED50")

    def test_remove_code(self):
        self.cart.apply_discount_code("SAVE10")
        self.assertEqual(self.cart._discount_code, "SAVE10")
        self.cart.remove_discount_code()
        self.assertEqual(self.cart._discount_code, None)

    def test_discount(self):
        # sure subtotal of 50
        self.cart.get_subtotal = MagicMock(return_value = 50)
        # save 10 discount code
        self.cart.apply_discount_code("SAVE10")
        self.assertEqual(self.cart._discount_code, "SAVE10")
        result = self.cart.get_discount_amount()
        self.assertEqual(result, 5)
        # save 20 
        self.cart.apply_discount_code("SAVE20")
        self.assertEqual(self.cart._discount_code, "SAVE20")
        result = self.cart.get_discount_amount()
        self.assertEqual(result, 10)
        # flat 5
        self.cart.apply_discount_code("FLAT5")
        self.assertEqual(self.cart._discount_code, "FLAT5")
        result = self.cart.get_discount_amount()
        self.assertEqual(result, 5)
        # flat 15
        self.cart.apply_discount_code("FLAT15")
        self.assertEqual(self.cart._discount_code, "FLAT15")
        result = self.cart.get_discount_amount()
        self.assertEqual(result, 15)

class TestPricingAndTaxCalculations(unittest.TestCase):
    pass
    def setUp(self):
        self.items = {
            'SKU-001': {'sku': 'SKU-001', 'name': 'Wireless Keyboard', 'unit_price': 49.99, 'quantity': 5, 'category': 'Electronics'}, 
            'SKU-002': {'sku': 'SKU-002', 'name': 'USB-C Hub', 'unit_price': 34.99, 'quantity': 3, 'category': 'Electronics'}
        }
        self.cart = ShoppingCart()

    def test_get_subtotal(self):
        # change _items to mock items
        with patch.object(self.cart, "_items", self.items):
            result = self.cart.get_subtotal()
            self.assertEqual(result, (5 * 49.99) + (3 * 34.99))
            

    def test_get_discount_amount(self):
        # apply a discount
        self.cart.apply_discount_code("SAVE20")
        self.assertEqual(self.cart._discount_code, "SAVE20")
        # change _items to mock items
        with patch.object(self.cart, "_items", self.items):
            result = self.cart.get_discount_amount()
            self.assertEqual(result, round(.2*((5 * 49.99) + (3 * 34.99)), 2))
            
    def test_get_tax(self):
        # change _items to mock items
        with patch.object(self.cart, "_items", self.items):
            result = self.cart.get_tax()
            rate = 0.08
            self.assertEqual(result, round(rate*((5 * 49.99) + (3 * 34.99)), 2))
            
    
    def test_get_total(self):
        # apply a discount
        self.cart.apply_discount_code("SAVE20")
        self.assertEqual(self.cart._discount_code, "SAVE20")
        # change _items to mock items
        with patch.object(self.cart, "_items", self.items):
            result = self.cart.get_total()
            subtotal = round((5 * 49.99) + (3 * 34.99), 2)
            tax = round(.08*(subtotal), 2)
            discount = round(.2*(subtotal), 2)
            self.assertEqual(result, round(subtotal-discount+tax, 2))

class TestCheckoutAndEdgeCases(unittest.TestCase):
    def setUp(self):
        self.mock_items = {
            'SKU-001': {'sku': 'SKU-001', 'name': 'Wireless Keyboard', 'unit_price': 49.99, 'quantity': 5, 'category': 'Electronics'}, 
            'SKU-002': {'sku': 'SKU-002', 'name': 'USB-C Hub', 'unit_price': 34.99, 'quantity': 3, 'category': 'Electronics'}
        }

        self.cart = ShoppingCart()

    def test_checkout_summary(self):
        with patch.object(self.cart, "_items", self.mock_items):
            result = self.cart.checkout()
            # testing keys
            self.assertIn("customer_id", result.keys())
            self.assertIn("timestamp", result.keys())
            self.assertIn("items", result.keys())
            self.assertIn("subtotal", result.keys())
            self.assertIn("discount_code", result.keys())
            self.assertIn("discount_amount", result.keys())
            self.assertIn("tax", result.keys())
            self.assertIn("total", result.keys())
            self.assertIn("item_count", result.keys())

    def test_checkout_empty_cart(self):
        # cart is already empty
        self.assertRaises(cart_exceptions.EmptyCartError, self.cart.checkout)
    
    def test_clear(self):
        with patch.object(self.cart, "_items", self.mock_items):
            self.cart.clear()
            result = self.cart._items
            self.assertEqual(result, {})

    def test_add_item_with_zero_or_negative(self):
        self.assertRaises(cart_exceptions.InvalidQuantityError, self.cart.add_item, "SKU-001", 0)
        self.assertRaises(cart_exceptions.InvalidQuantityError, self.cart.add_item, "SKU-001", -5)

    def test_removing_updating_item_not_in_cart(self):
        # no items in cart currently
        self.assertRaises(cart_exceptions.CartItemNotFoundError, self.cart.remove_item, "SKU-001")
        self.assertRaises(cart_exceptions.CartItemNotFoundError, self.cart.update_quantity, "SKU-001", 10)

    def test_add_item_not_in_catalogue(self):
        self.assertRaises(cart_exceptions.ItemNotFoundError, self.cart.add_item, "fake-item", 5)

            

    
