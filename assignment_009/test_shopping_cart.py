import unittest
from unittest.mock import patch, MagicMock
from cart import ShoppingCart
from cart_exceptions import CartError
from inventory import InventoryService

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

        # Test pdate quantity function
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

        def test_sufficient_stock(self):
            self.shopping_cart.add_item

if __name__ == "__main__":
    unittest.main()

