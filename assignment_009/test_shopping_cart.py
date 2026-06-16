"""

"""

import unittest
from datetime import datetime
from functools import reduce
from typing import Any
from unittest.mock import patch, MagicMock

from inventory import InventoryService
from pricing import  PricingService
from cart import ShoppingCart
from cart_exceptions import CartError, ItemNotFoundError, InvalidQuantityError, InsufficientStockError, CartItemNotFoundError, InvalidDiscountCodeError, EmptyCartError
from catalogue import PRODUCT_CATALOGUE, DISCOUNT_CODES


class TestItemManagement(unittest.TestCase):
    def setUp(self):
        self.inventory = MagicMock()

        self.item_quantity = 10
        self.inventory.get_stock.return_value = self.item_quantity

        self.cart = ShoppingCart(inventory_service=self.inventory, customer_id="1")
        self.test_items_1: list[dict[str, Any]] = [item_of_quantity(key, value, 1) for key, value in PRODUCT_CATALOGUE.items()]
        self.test_items_2: list[dict[str, Any]] = [item_of_quantity(key, value, 2) for key, value in PRODUCT_CATALOGUE.items()]
        self.test_items_20: list[dict[str, Any]] = [item_of_quantity(key, value, 20) for key, value in PRODUCT_CATALOGUE.items()]

    def test_shopping_cart_add_item_adds_item(self):
        item: dict[str, Any] = self.test_items_1[0]

        self.cart.add_item(item["sku"])
        self.assertEqual(len(self.cart.get_items()), 1, "Only 1 item for add item")
        self.assertDictEqual(self.cart.get_items()[0], item, "Items must be match")

    def test_shopping_cart_adds_item_adds_multiple_items(self):
        for i in range(0, len(self.test_items_1)):
            item: dict[str, Any] = self.test_items_1[i]
            self.cart.add_item(item["sku"])
            self.assertEqual(len(self.cart.get_items()), i+1, "Additional items should increase the number of items")

    def test_shopping_cart_adds_item_adds_quantity(self):
        item: dict[str, Any] = self.test_items_2[0]
        self.cart.add_item(item["sku"], 2)
        self.assertDictEqual(self.cart.get_items()[0], item, "Items must match")

    def test_shopping_cart_adds_item_multiple_adds_increase_quantity(self):
        item: dict[str, Any] = self.test_items_1[0]
        item2: dict[str, Any] = self.test_items_2[0]

        self.cart.add_item(item["sku"], 1)
        self.cart.add_item(item["sku"], 1)

        self.assertEqual(len(self.cart.get_items()), 1)
        self.assertDictEqual(self.cart.get_items()[0], item2, "Items must match")

    def test_shopping_cart_adds_item_errors_on_unknown_item(self):
        item_key: str = "unknown item"
        self.assertRaisesRegex(ItemNotFoundError, f"No product found with SKU '{item_key}'.", self.cart.add_item, item_key)

    def test_shopping_cart_adds_item_errors_on_invalid_quantity(self):
        item: dict[str, Any] = self.test_items_1[0]
        quantity: int = -1
        self.assertRaisesRegex(InvalidQuantityError, f"Invalid quantity '{quantity}': quantity must be a positive integer.", self.cart.add_item, item["sku"], quantity)

    def test_shopping_cart_adds_item_errors_on_insufficient_quantity(self):
        quantity: int = 20
        item: dict[str, Any] = self.test_items_20[0]
        self.assertRaisesRegex(InsufficientStockError,
                               f"Insufficient stock for SKU '{item["sku"]}': "
                                f"requested {quantity}, only {self.item_quantity} available.",
                               self.cart.add_item, item["sku"], quantity)

    def test_shopping_cart_remove_item_removes_item(self):
        for item in self.test_items_2:
            self.cart.add_item(item["sku"])
        self.cart.remove_item(self.test_items_2[0]["sku"])
        self.assertEqual(len(self.cart.get_items()), len(self.test_items_2) - 1)
        self.assertNotIn(self.test_items_2[0], self.cart.get_items(), "Item should be removed")

    def test_shopping_cart_remove_item_error_on_not_found(self):
        item: dict[str, Any] = self.test_items_2[0]
        not_found_item: dict[str, Any] = self.test_items_2[1]
        not_found_sku = not_found_item["sku"]
        self.cart.add_item(item["sku"])
        self.assertRaisesRegex(CartItemNotFoundError, f"SKU '{not_found_sku}' is not in the cart.", self.cart.remove_item, not_found_sku)

    def test_shopping_cart_update_quantity_updates_quantity(self):
        item: dict[str, Any] = self.test_items_1[0]
        item2: dict[str, Any] = self.test_items_2[0]
        self.cart.add_item(item["sku"])
        self.cart.update_quantity(item["sku"], 2)

        self.assertEqual(len(self.cart.get_items()), 1)
        self.assertDictEqual(self.cart.get_items()[0], item2, "Items must match")

    def test_shopping_cart_update_quantity_errors_on_not_found(self):
        item: dict[str, Any] = self.test_items_2[0]
        item_sku = item["sku"]
        quantity: int = 5

        self.assertRaisesRegex(CartItemNotFoundError, f"SKU '{item_sku}' is not in the cart.",
                               self.cart.update_quantity, item_sku, quantity)

    def test_shopping_cart_update_quantity_error_on_invalid_quantity(self):
        item: dict[str, Any] = self.test_items_1[0]
        self.cart.add_item(item["sku"])
        quantity: int = -1
        self.assertRaisesRegex(InvalidQuantityError,
                               f"Invalid quantity '{quantity}': quantity must be a positive integer.",
                               self.cart.update_quantity, item["sku"], quantity)


    def test_shopping_cart_update_quantity_errors_on_insufficient_stock(self):
        item: dict[str, Any] = self.test_items_1[0]
        self.cart.add_item(item["sku"])
        quantity: int = 20
        self.assertRaisesRegex(InsufficientStockError,
                               f"Insufficient stock for SKU '{item["sku"]}': "
                               f"requested {quantity}, only {self.item_quantity} available.",
                               self.cart.update_quantity, item["sku"], quantity)

class TestInventoryService(unittest.TestCase):
    def setUp(self) -> None:
        self.inventory_service: InventoryService = InventoryService()
        self.cart = ShoppingCart(inventory_service=self.inventory_service)
        self.test_items_1: list[dict[str, Any]] = [item_of_quantity(key, value, 1) for key, value in PRODUCT_CATALOGUE.items()]
        self.test_items_2: list[dict[str, Any]] = [item_of_quantity(key, value, 2) for key, value in PRODUCT_CATALOGUE.items()]

    @patch.object(InventoryService, "_query_inventory_db")
    def test_sufficient_stock(self, mock_inventory_db):
        mock_inventory_db.return_value = 10
        item: dict[str, Any] = self.test_items_1[0]

        self.cart.add_item(item["sku"])
        self.assertEqual(len(self.cart.get_items()), 1, "Only 1 item for add item")
        self.assertDictEqual(self.cart.get_items()[0], item, "Items must be match")

        mock_inventory_db.assert_called_once()

    @patch.object(InventoryService, "_query_inventory_db")
    def test_stock_unavailable(self, mock_inventory_db):
        sku: str = self.test_items_2[0]["sku"]
        mock_inventory_db.side_effect = ItemNotFoundError(sku)
        item: dict[str, Any] = self.test_items_1[0]

        self.assertRaisesRegex(ItemNotFoundError,
                               f"No product found with SKU '{sku}'.",
                               self.cart.add_item, item["sku"])
        mock_inventory_db.assert_called_once()

    @patch.object(InventoryService, "_query_inventory_db")
    def test_insufficient_stock(self, mock_inventory_db):
        max_quantity: int = 1
        mock_inventory_db.return_value = max_quantity
        quantity: int = 2
        item: dict[str, Any] = self.test_items_2[0]
        self.assertRaisesRegex(InsufficientStockError,
                               f"Insufficient stock for SKU '{item["sku"]}': "
                               f"requested {quantity}, only {max_quantity} available.",
                               self.cart.add_item, item["sku"], quantity)
        mock_inventory_db.assert_called_once()

class TestDiscountCodes(unittest.TestCase):
    def setUp(self) -> None:
        self.pricing_service = PricingService()

    def test_valid_percent_code(self):
        code: str = "SAVE10"
        discount_count: dict[str, Any] = self.pricing_service.validate_discount_code(code)
        self.assertDictEqual(discount_count, DISCOUNT_CODES[code])

    def test_valid_flat_code(self):
        code: str = "FLAT5"
        discount_count: dict[str, Any] = self.pricing_service.validate_discount_code(code)
        self.assertDictEqual(discount_count, DISCOUNT_CODES[code])

    def test_unrecognized_code(self):
        code: str = "UNKNOWN"
        self.assertRaisesRegex(InvalidDiscountCodeError, f"Discount code '{code}' is invalid or expired.",
        self.pricing_service.validate_discount_code, code)

    def test_expired_code(self):
        code: str = "EXPIRED50"
        self.assertRaisesRegex(InvalidDiscountCodeError, f"Discount code '{code}' is expired.",
                               self.pricing_service.validate_discount_code, code)

    def test_apply_percent_code(self):
        cart = ShoppingCart(pricing_service=self.pricing_service, customer_id="1")
        code: str = "SAVE10"
        cart.apply_discount_code(code)
        self.assertEqual(cart._discount_code, code)

    def test_remove_code(self):
        cart = ShoppingCart(pricing_service=self.pricing_service, customer_id="1")
        code: str = "SAVE10"
        cart.apply_discount_code(code)
        cart.remove_discount_code()
        self.assertIsNone(cart._discount_code)

    def test_percent_code_correct(self):
        subtotal: float = 10.00
        code: str = "SAVE10"
        wanted_total: float = subtotal * 0.90

        total: float = self.pricing_service.apply_discount(subtotal, code)

        self.assertEqual(total, wanted_total)

    def test_flat_code_correct(self):
        subtotal: float = 10.00
        code: str = "FLAT5"
        wanted_total: float = subtotal - 5.0

        total: float = self.pricing_service.apply_discount(subtotal, code)

        self.assertEqual(total, wanted_total)

    def test_applied_discount_cannot_be_negative(self):
        subtotal: float = 2.00
        code: str = "FLAT5"
        wanted_total: float = 0

        total: float = self.pricing_service.apply_discount(subtotal, code)

        self.assertEqual(total, wanted_total)

class TestPricingAndTax(unittest.TestCase):
    def setUp(self) -> None:
        self.pricing_service = PricingService()
        self.inventory = MagicMock()
        self.item_quantity = 10
        self.inventory.get_stock.return_value = self.item_quantity
        self.cart = ShoppingCart(inventory_service=self.inventory, customer_id="1")
        self.test_items_1: list[dict[str, Any]] = [item_of_quantity(key, value, 1) for key, value in PRODUCT_CATALOGUE.items()]

        for item in self.test_items_1:
            self.cart.add_item(item["sku"])

        self.code: str = "SAVE10"
        self.cart.apply_discount_code(self.code)

        self.sub_total: float = sum(item["unit_price"] * item["quantity"] for item in self.test_items_1)

    def test_get_subtotal(self):
        self.assertEqual(self.cart.get_subtotal(), self.sub_total)

    def test_get_discount_amount(self):
        discount_wanted: float = round(self.sub_total * 0.10, 2)

        self.assertEqual(self.cart.get_discount_amount(), discount_wanted)

    def test_calculate_tax(self):
        tax: float = 20.48
        self.assertEqual(self.pricing_service.calculate_tax(self.test_items_1), tax)


    def test_get_tax(self):
        tax: float = 20.48
        self.assertEqual(self.cart.get_tax(), tax)

    def test_get_total(self):
        tax: float = 20.48
        discount: float = round(self.sub_total * 0.10, 2)
        self.assertAlmostEqual(self.cart.get_total(), self.sub_total - discount + tax, 2)

class TestCheckout(unittest.TestCase):
    def setUp(self) -> None:
        self.pricing_service = PricingService()
        self.inventory = MagicMock()
        self.item_quantity = 10
        self.inventory.get_stock.return_value = self.item_quantity
        self.customer_id: str = "1"
        self.cart = ShoppingCart(inventory_service=self.inventory, customer_id=self.customer_id)

        self.test_items_1: list[dict[str, Any]] = [item_of_quantity(key, value, 1) for key, value in PRODUCT_CATALOGUE.items()]

    def test_checkout_correct(self):
        for item in self.test_items_1:
            self.cart.add_item(item["sku"])

        expected_keys: list[str] = [
            "customer_id",
            "timestamp",
            "items",
            "subtotal",
            "discount_code",
            "discount_amount",
            "tax",
            "total",
            "item_count",
        ]

        summary: dict[str, Any] = self.cart.checkout()

        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, summary)

    def test_checkout_errors(self):
        self.assertRaisesRegex(EmptyCartError, "Cannot check out: the cart is empty.", self.cart.checkout)

    def test_clear_resets_items_discount_code(self):
        self.cart.add_item(self.test_items_1[0]["sku"])
        self.cart.apply_discount_code("SAVE10")
        self.cart.clear()

        self.assertEqual(len(self.cart.get_items()), 0)
        self.assertEqual(self.cart.get_discount_amount(), 0.0)


def item_of_quantity(key: str, product: dict[str, Any], quantity: int) -> dict[str, Any]:
    item: dict[str, Any] = dict(product)
    item["sku"] = key
    price: int = product["price"]
    del item["price"]
    item["unit_price"] = price
    item["quantity"] = quantity
    return item
