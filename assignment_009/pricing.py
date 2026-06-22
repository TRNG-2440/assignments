"""
pricing.py

Pricing service for the e-commerce shopping cart application.

This module is provided as part of the application under test for the
Shopping Cart Unit Testing activity. Do not modify this file.

Contains:
  - PricingService : Handles discount code validation and tax calculation
"""

from datetime import date

from catalogue import DISCOUNT_CODES, PRODUCT_CATALOGUE, CATEGORY_TAX_RATES
from cart_exceptions import InvalidDiscountCodeError


class PricingService:
    """
    Handles discount code validation and tax calculation.
    """

    def validate_discount_code(self, code: str) -> dict:
        """
        Validates a discount code and returns its definition dict.

        Raises:
            InvalidDiscountCodeError: if the code is not recognised or has expired.
        """
        code = code.upper().strip()
        if code not in DISCOUNT_CODES:
            raise InvalidDiscountCodeError(code)
        discount = DISCOUNT_CODES[code]
        if discount["expires"] < date.today():
            raise InvalidDiscountCodeError(code, reason="expired")
        return discount

    def apply_discount(self, subtotal: float, code: str) -> float:
        """
        Applies a validated discount code to a subtotal.

        Returns:
            float: the discounted subtotal (never below 0.00).

        Raises:
            InvalidDiscountCodeError: if the code is invalid or expired.
        """
        discount = self.validate_discount_code(code)
        if discount["type"] == "percent":
            discounted = subtotal * (1 - discount["value"] / 100)
        else:
            discounted = subtotal - discount["value"]
        return round(max(discounted, 0.0), 2)

    def calculate_tax(self, items: list) -> float:
        """
        Calculates total tax across all cart items using per-category rates.

        Args:
            items (list): list of cart item dicts, each containing
                          'sku', 'quantity', and 'unit_price'.

        Returns:
            float: total tax amount rounded to 2 decimal places.
        """
        total_tax = 0.0
        for item in items:
            product = PRODUCT_CATALOGUE.get(item["sku"])
            if product:
                rate = CATEGORY_TAX_RATES.get(product["category"], 0.0)
                total_tax += item["unit_price"] * item["quantity"] * rate
        return round(total_tax, 2)
