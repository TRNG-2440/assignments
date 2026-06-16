import os
import sys
from typing import List
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from catalogue import PRODUCT_CATALOGUE, DISCOUNT_CODES, CATEGORY_TAX_RATES
from cart_exceptions import (
    CartItemNotFoundError,
    EmptyCartError,
    InsufficientStockError,
    InvalidDiscountCodeError,
    InvalidQuantityError,
    ItemNotFoundError,
)
from cart import ShoppingCart
from pricing import PricingService
from inventory import InventoryService


class TestItemManagement(unittest.TestCase):
    def setUp(self) -> None:
        self.cart = ShoppingCart()

    def tearDown(self) -> None:
        del self.cart

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

    def tearDown(self) -> None:
        del self.cart

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


class TestDiscountCodes(unittest.TestCase):
    def setUp(self) -> None:
        self.pricing_service = PricingService()
        self.cart = ShoppingCart(pricing_service=self.pricing_service)

    def tearDown(self) -> None:
        del self.pricing_service
        del self.cart

    def test_valid_percent_discount_code(self) -> None:
        discount_code = "save10"
        expected_dict = DISCOUNT_CODES.get(discount_code.upper().strip())

        output_dict = self.pricing_service.validate_discount_code(discount_code)
        self.assertDictEqual(output_dict, expected_dict)
        self.assertEquals(output_dict.get("type"), "percent")

    def test_valid_flat_discount_code(self) -> None:
        discount_code = "flat5"
        expected_dict = DISCOUNT_CODES.get(discount_code.upper().strip())

        output_dict = self.pricing_service.validate_discount_code(discount_code)
        self.assertDictEqual(output_dict, expected_dict)
        self.assertEquals(output_dict.get("type"), "flat")

    def test_unrecognized_discount_code(self) -> None:
        discount_code = "flat50"
        with self.assertRaisesRegex(
            InvalidDiscountCodeError,
            f"Discount code '{discount_code.upper().strip()}' is invalid or expired.",
        ):
            self.pricing_service.validate_discount_code(discount_code)

    def test_expired_discount_code(self) -> None:
        discount_code = "expired50"
        with self.assertRaisesRegex(
            InvalidDiscountCodeError,
            f"Discount code '{discount_code.upper().strip()}' is expired.",
        ):
            self.pricing_service.validate_discount_code(discount_code)

    def test_remove_discount_code(self) -> None:
        discount_code = "flat5"

        self.cart.apply_discount_code(discount_code)
        self.cart.remove_discount_code()
        self.assertEquals(self.cart.get_discount_amount(), 0.0)

    def test_apply_discount_code_in_cart(self) -> None:
        discount_code = "flat5"
        self.cart.apply_discount_code(discount_code)
        self.assertEquals(self.cart._discount_code, discount_code.upper().strip())

    def test_apply_discount_percent_code(self) -> None:
        discount_code = "save10"
        discount_info = DISCOUNT_CODES.get(discount_code.upper().strip())
        subtotal = 20

        discount_subtotal = self.pricing_service.apply_discount(subtotal, discount_code)
        self.assertEquals(
            discount_subtotal, (1 - discount_info.get("value") / 100) * subtotal
        )

    def test_apply_discount_flat_code(self) -> None:
        discount_code = "flat5"
        discount_info = DISCOUNT_CODES.get(discount_code.upper().strip())
        subtotal = 20

        discount_subtotal = self.pricing_service.apply_discount(subtotal, discount_code)
        self.assertEquals(discount_subtotal, subtotal - discount_info.get("value"))

    def test_apply_discount_negative_discounted_amount(self) -> None:
        discount_code = "flat5"
        subtotal = 2

        discount_subtotal = self.pricing_service.apply_discount(subtotal, discount_code)
        self.assertEquals(discount_subtotal, 0.0)


class TestPricingAndTax(unittest.TestCase):
    def setUp(self) -> None:
        self.cart = ShoppingCart()
        self.sku = "SKU-001"
        self.quantity = 2
        product = PRODUCT_CATALOGUE[self.sku]
        self.unit_price = product["price"]
        self.tax_rate = CATEGORY_TAX_RATES[product["category"]]
        self.discount_code = "FLAT5"
        self.discount = DISCOUNT_CODES[self.discount_code].get("value")
        expected_dict: dict = {
            "sku": self.sku,
            "name": product["name"],
            "unit_price": product["price"],
            "quantity": self.quantity,
            "category": product["category"],
        }

        self.cart.add_item(sku=self.sku, quantity=self.quantity)
        items: List = self.cart.get_items()
        filtered_items: List = [item for item in items if item.get("sku") == self.sku]

        self.assertEquals(len(filtered_items), 1)
        self.assertDictEqual(filtered_items[0], expected_dict)

        self.cart.apply_discount_code(self.discount_code)
        self.assertEquals(self.cart._discount_code, self.discount_code)

    def tearDown(self) -> None:
        del self.cart

    def test_get_subtotal(self) -> None:
        subtotal = self.cart.get_subtotal()
        self.assertEquals(subtotal, self.quantity * self.unit_price)

    def test_get_tax(self) -> None:
        tax_amount = self.cart.get_tax()
        self.assertAlmostEquals(
            tax_amount, round(self.unit_price * self.quantity * self.tax_rate, 2)
        )

    def test_get_discount_amount(self) -> None:
        discounted_subtotal = self.cart.get_discount_amount()
        self.assertAlmostEquals(discounted_subtotal, self.discount)

    def test_get_total(self) -> None:
        total = self.cart.get_total()
        expected_subtotal = self.unit_price * self.quantity
        expected_tax = round(self.unit_price * self.quantity * self.tax_rate, 2)
        self.assertAlmostEquals(
            total,
            round(expected_subtotal - self.discount + expected_tax, 2),
        )


class TestCheckoutAndEdgeCases(unittest.TestCase):
    def setUp(self) -> None:
        self.cart = ShoppingCart()

    def tearDown(self) -> None:
        del self.cart

    def test_valid_checkout(self) -> None:
        sku: str = "SKU-001"
        quantity: int = 2
        discount_code: str = "FLAT5"
        product = PRODUCT_CATALOGUE[sku]
        item: dict = {
            "sku": sku,
            "name": product["name"],
            "unit_price": product["price"],
            "quantity": quantity,
            "category": product["category"],
        }
        expected_dict: dict = {
            "customer_id": "guest",
            "items": [item],
            "subtotal": 99.98,
            "discount_code": discount_code,
            "discount_amount": 5.00,
            "tax": 8.00,
            "total": 102.98,
            "item_count": 2,
        }

        self.cart.add_item(sku=sku, quantity=quantity)
        self.cart.apply_discount_code(discount_code)
        output_dict = self.cart.checkout()
        self.assertDictContainsSubset(expected_dict, output_dict)

    def test_checkout_empty_cart(self) -> None:
        with self.assertRaises(EmptyCartError):
            self.cart.checkout()

    def test_clear(self) -> None:
        sku: str = "SKU-001"
        quantity: int = 2
        product = PRODUCT_CATALOGUE[sku]
        discount_code = "FLAT5"
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

        self.cart.apply_discount_code(discount_code)
        self.assertEquals(self.cart._discount_code, discount_code)

        self.cart.clear()
        self.assertCountEqual(self.cart.get_items(), [])
        self.assertEquals(self.cart._discount_code, None)

    def test_add_negative_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item(sku="SKU-001", quantity=-23)

    def test_add_zero_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            self.cart.add_item(sku="SKU-001", quantity=0)

    def test_update_sku_not_in_cart(self) -> None:
        sku = "SKU-001"
        with self.assertRaises(CartItemNotFoundError):
            self.cart.update_quantity(sku=sku, quantity=1)

    def test_add_invalid_sku(self):
        with self.assertRaises(ItemNotFoundError):
            self.cart.add_item(sku="SKU-009")
