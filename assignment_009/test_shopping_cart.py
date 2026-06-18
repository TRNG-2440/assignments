import unittest
from unittest.mock import patch
from cart import ShoppingCart
from cart_exceptions import (
    EmptyCartError,
    InvalidQuantityError,
    CartItemNotFoundError,
    ItemNotFoundError,
    InsufficientStockError,
    InvalidDiscountCodeError
)
from inventory import InventoryService
from pricing import PricingService

class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.shopping_cart = ShoppingCart()
    
    def tearDown(self):
        self.shopping_cart.clear()

    def test_item_management(self):
        """
        Tests adding, removing and updating quantity of items in the shopping cart class.
        """
        # Local variables
        shopping_cart = self.shopping_cart
        
        # Test add_item function
        shopping_cart.add_item("SKU-004", 1)
        self.assertEqual(shopping_cart.get_items()[0]["sku"], "SKU-004")

        # Test update quantity function
        shopping_cart.update_quantity("SKU-004", 10)
        self.assertEqual(shopping_cart.get_item_count(), 10)

        # Test remove item function
        shopping_cart.remove_item("SKU-004")
        self.assertTrue(shopping_cart.is_empty)

class TestInventoryChecks(unittest.TestCase):
    def setUp(self):
        self.shopping_cart = ShoppingCart()
        self.inventory_service = InventoryService()

    def tearDown(self):
        self.shopping_cart.clear()

    @patch.object(InventoryService, "get_stock")
    def test_sufficient_stock(self, mock_stock):
        """
        Tests add_item by mocking the stock count with a sufficient count
        """
        shopping_cart = self.shopping_cart
        mock_stock.return_value = 10
        
        shopping_cart.add_item("SKU-001", 5)
        self.assertEqual(shopping_cart.get_item_count(), 5)
        mock_stock.assert_called_once_with("SKU-001")

    @patch.object(InventoryService, "get_stock")
    def test_stock_unavailable(self, mock_stock):
        """
        Tests add_item by mocking the stock count with a insufficient count
        """
        shopping_cart = self.shopping_cart
        mock_stock.return_value = 0
        
        with self.assertRaises(InsufficientStockError):
            shopping_cart.add_item("SKU-001", 1)

    @patch.object(InventoryService, "get_stock")
    def test_low_stock_level(self, mock_stock):
        """
        Tests add_item by mocking the stock count with a insufficient count that is not zero
        """
        shopping_cart = self.shopping_cart
        mock_stock.return_value = 2
        
        with self.assertRaises(InsufficientStockError):
            shopping_cart.add_item("SKU-001", 5)

class TestDiscountCodes(unittest.TestCase):
    def setUp(self):
        self.shopping_cart = ShoppingCart()

    def tearDown(self):
        self.shopping_cart.clear()

    @patch.object(PricingService, "validate_discount_code")
    def test_discount_code_application(self, mock_validate):
        """
        Tests applying and removing valid percent and flat rate discount codes.
        """
        shopping_cart = self.shopping_cart
        
        mock_validate.return_value = {"type": "percent", "value": 10}
        shopping_cart.apply_discount_code("SAVE10")
        self.assertEqual(shopping_cart._discount_code, "SAVE10")

        mock_validate.return_value = {"type": "flat", "value": 5.0}
        shopping_cart.apply_discount_code("FLAT5")
        self.assertEqual(shopping_cart._discount_code, "FLAT5")

        shopping_cart.remove_discount_code()
        self.assertIsNone(shopping_cart._discount_code)

    @patch.object(PricingService, "validate_discount_code")
    def test_invalid_discount_codes(self, mock_validate):
        """
        Tests invalid or expired discount codes correctly raise an the correct error.
        """
        shopping_cart = self.shopping_cart
        mock_validate.side_effect = InvalidDiscountCodeError("INVALID")
        
        for code in ["FAKE10", "EXPIRED20"]:
            with self.subTest(code=code):
                with self.assertRaises(InvalidDiscountCodeError):
                    shopping_cart.apply_discount_code(code)

class TestPricingAndTax(unittest.TestCase):
    def setUp(self):
        self.shopping_cart = ShoppingCart()

    def tearDown(self):
        self.shopping_cart.clear()

    @patch.object(InventoryService, "get_stock")
    def test_pricing_calculations(self, mock_stock):
        """
        Tests subtotal, tax, discount, and final total are calculated correctly.
        """
        shopping_cart = self.shopping_cart
        mock_stock.return_value = 20
        
        shopping_cart.add_item("SKU-001", 2)
        shopping_cart.add_item("SKU-005", 1)
        
        subtotal = shopping_cart.get_subtotal()
        tax = shopping_cart.get_tax()
        self.assertEqual(subtotal, 112.97)
        self.assertEqual(tax, 8.65)
        
        shopping_cart.apply_discount_code("FLAT5")
        discount = shopping_cart.get_discount_amount()
        expected_total = round(subtotal - discount + tax, 2)
        self.assertEqual(shopping_cart.get_total(), expected_total)

class TestCheckoutAndEdgeCases(unittest.TestCase):
    def setUp(self):
        self.shopping_cart = ShoppingCart()

    def tearDown(self):
        self.shopping_cart.clear()

    @patch.object(InventoryService, "get_stock")
    def test_checkout_summary(self, mock_stock):
        """
        Tests finalizing a populated cart returns an order summary with the correct information.
        """
        shopping_cart = self.shopping_cart
        mock_stock.return_value = 5
        
        shopping_cart.add_item("SKU-004", 1)
        summary = shopping_cart.checkout()
        self.assertIn("items", summary)
        self.assertIn("total", summary)
        self.assertIn("tax", summary)

    def test_checkout_empty_cart(self):
        """
        Tests checking out with an empty cart, it should raise the EmptyCartError.
        """
        with self.assertRaises(EmptyCartError):
            self.shopping_cart.checkout()

    @patch.object(InventoryService, "get_stock")
    def test_clear_cart(self, mock_stock):
        """
        Tests clearing cart.
        """
        shopping_cart = self.shopping_cart
        mock_stock.return_value = 10
        
        shopping_cart.add_item("SKU-004", 1)
        shopping_cart.apply_discount_code("SAVE10")
        shopping_cart.clear()
        
        self.assertTrue(shopping_cart.is_empty())
        self.assertIsNone(shopping_cart._discount_code)

    def test_invalid_quantity_error(self):
        """
        Tests adding items with a zero or negative quantity.
        """
        shopping_cart = self.shopping_cart
        for qty in [0, -1, -50]:
            with self.subTest(qty=qty):
                with self.assertRaises(InvalidQuantityError):
                    shopping_cart.add_item("SKU-004", qty)

    def test_cart_item_not_found(self):
        """
        Tests that removing or updating an item that is not in the cart.
        """
        shopping_cart = self.shopping_cart
        with self.assertRaises(CartItemNotFoundError):
            shopping_cart.remove_item("SKU-001")
        with self.assertRaises(CartItemNotFoundError):
            shopping_cart.update_quantity("SKU-001", 5)

    def test_item_not_found_catalogue(self):
        """
        Tests adding a SKU that does not exist in the catalogue.
        """
        shopping_cart = self.shopping_cart
        with self.assertRaises(ItemNotFoundError):
            shopping_cart.add_item("INVALID-SKU", 1)

if __name__ == "__main__":
    unittest.main()

