import os
import sys
from typing import List
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from catalogue import PRODUCT_CATALOGUE
from cart_exceptions import (
    CartItemNotFoundError,
    InsufficientStockError,
    InvalidQuantityError,
    ItemNotFoundError,
)
from cart import ShoppingCart
from pricing import PricingService
from inventory import InventoryService


class TestItemManagement(unittest.TestCase):
    def setUp(self) -> None:
        self.inventory = InventoryService()
        self.pricing = PricingService()
        self.cart = ShoppingCart(self.inventory, self.pricing)

    def tearDown(self) -> None:
        del self.cart
        del self.inventory
        del self.pricing

    def test_add_negative_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item(sku="SKU-001", quantity=-23)

    def test_add_zero_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item(sku="SKU-001", quantity=0)

    def test_add_invalid_sku(self):
        with self.assertRaises(ItemNotFoundError):
            self.cart.add_item(sku="SKU-009")

    def test_add_insufficent_stock(self):
        sku = "SKU-001"
        quantity = 51
        with self.assertRaises(InsufficientStockError):
            self.cart.add_item(sku=sku, quantity=quantity)

    def test_add_insufficent_stock_duplicate_sku(self):
        sku = "SKU-001"
        quantity1 = 2
        quantity2 = 49

        self.cart.add_item(sku=sku, quantity=quantity1)
        with self.assertRaises(InsufficientStockError):
            self.cart.add_item(sku=sku, quantity=quantity2)

    def test_add_valid_addition(self) -> None:
        sku: str = "SKU-001"
        quantity: int = 2
        product = PRODUCT_CATALOGUE[sku]
        expected_dict: dict = {
            "sku": sku,
            "name": product["name"],
            "unit_price": product["price"],
            "quantity": quantity,
            "category": product["category"],
        }

        self.cart.add_item(sku=sku, quantity=quantity)
        items: List = self.cart.get_items()
        filtered_items: List = [item for item in items if item.get("sku") == sku]

        self.assertEquals(len(filtered_items), 1)
        self.assertDictEqual(filtered_items[0], expected_dict)

    def test_add_duplicate_SKU(self) -> None:
        sku: str = "SKU-001"
        quantity1: int = 2
        quantity2: int = 1
        product = PRODUCT_CATALOGUE[sku]
        expected_dict: dict = {
            "sku": sku,
            "name": product["name"],
            "unit_price": product["price"],
            "quantity": quantity2 + quantity1,
            "category": product["category"],
        }

        self.cart.add_item(sku=sku, quantity=quantity1)
        self.cart.add_item(sku=sku, quantity=quantity2)
        items: List = self.cart.get_items()
        filtered_items: List = [item for item in items if item.get("sku") == sku]

        self.assertEquals(len(filtered_items), 1)
        self.assertDictEqual(filtered_items[0], expected_dict)

    def test_remove_sku_not_in_cart(self) -> None:
        with self.assertRaises(CartItemNotFoundError):
            self.cart.remove_item("SKU-001")

    def test_remove_sku_in_cart(self) -> None:
        sku = "SKU-001"

        self.cart.add_item(sku=sku)
        self.cart.remove_item(sku=sku)
        items: List = self.cart.get_items()
        filtered_items: List = [item for item in items if item.get("sku") == sku]
        self.assertEquals(len(filtered_items), 0)

    def test_update_sku_not_in_cart(self) -> None:
        sku = "SKU-001"
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity(sku=sku, quantity=1)

    def test_update_negative_quantity(self) -> None:
        sku = "SKU-001"

        self.cart.add_item(sku=sku)
        with self.assertRaises(InvalidQuantityError):
            self.cart.update_quantity(sku=sku, quantity=-10)

    def test_update_zero_quantity(self) -> None:
        sku = "SKU-001"

        self.cart.add_item(sku=sku)
        with self.assertRaises(InvalidQuantityError):
            self.cart.update_quantity(sku=sku, quantity=0)

    def test_update_insufficient_stock(self) -> None:
        sku = "SKU-001"
        quantity = 51

        self.cart.add_item(sku=sku)
        with self.assertRaises(InsufficientStockError):
            self.cart.update_quantity(sku=sku, quantity=quantity)

    def test_update_valid(self) -> None:
        sku = "SKU-001"
        quantity = 50
        product = PRODUCT_CATALOGUE[sku]
        expected_dict: dict = {
            "sku": sku,
            "name": product["name"],
            "unit_price": product["price"],
            "quantity": quantity,
            "category": product["category"],
        }

        self.cart.add_item(sku=sku)
        self.cart.update_quantity(sku=sku, quantity=quantity)
        items: List = self.cart.get_items()
        filtered_items: List = [item for item in items if item.get("sku") == sku]

        self.assertEquals(len(filtered_items), 1)
        self.assertDictEqual(filtered_items[0], expected_dict)


class TestInventoryManagement(unittest.TestCase):
    def setUp(self) -> None:
        self.cart = ShoppingCart()

    @patch.object(InventoryService, "get_stock")
    def test_get_stock_unavailable(self, mock_get_stock) -> None:
        sku: str = "SKU-001"
        mock_get_stock.return_value = 0

        with self.assertRaises(InsufficientStockError):
            self.cart.add_item(sku=sku, quantity=1)

        mock_get_stock.assert_called_once_with(sku)

    @patch.object(InventoryService, "get_stock")
    def test_get_stock_insufficient(self, mock_get_stock) -> None:
        sku: str = "SKU-001"
        quantity: int = 51
        mock_get_stock.return_value = 20

        with self.assertRaises(InsufficientStockError):
            self.cart.add_item(sku=sku, quantity=quantity)

        mock_get_stock.assert_called_once_with(sku)

    @patch.object(InventoryService, "get_stock")
    def test_get_stock_available(self, mock_get_stock) -> None:
        sku: str = "SKU-001"
        quantity: int = 1
        product = PRODUCT_CATALOGUE[sku]
        expected_dict: dict = {
            "sku": sku,
            "name": product["name"],
            "unit_price": product["price"],
            "quantity": quantity,
            "category": product["category"],
        }
        mock_get_stock.return_value = 23

        self.cart.add_item(sku=sku, quantity=quantity)
        items: List = self.cart.get_items()
        filtered_items: List = [item for item in items if item.get("sku") == sku]

        self.assertEquals(len(filtered_items), 1)
        self.assertDictEqual(filtered_items[0], expected_dict)
        mock_get_stock.assert_called_once_with(sku)
