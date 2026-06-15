"""
cart.py

Core shopping cart for the e-commerce application.

This module is provided as part of the application under test for the
Shopping Cart Unit Testing activity. Do not modify this file.

Contains:
  - ShoppingCart : Core cart logic (add, remove, checkout, etc.)
"""

from datetime import datetime

from catalogue import PRODUCT_CATALOGUE
from cart_exceptions import (
    InvalidQuantityError,
    ItemNotFoundError,
    InsufficientStockError,
    CartItemNotFoundError,
    EmptyCartError,
)
from inventory import InventoryService
from pricing import PricingService


class ShoppingCart:
    """
    Core shopping cart for an enterprise e-commerce platform.

    Responsibilities:
      - Maintain a list of items (SKU, quantity, unit price)
      - Delegate inventory checks to InventoryService
      - Delegate pricing/tax logic to PricingService
      - Enforce business rules via custom exceptions
      - Produce a structured order summary on checkout
    """

    def __init__(
        self,
        inventory_service: InventoryService = None,
        pricing_service: PricingService = None,
        customer_id: str = None,
    ):
        self._items: dict[str, dict] = {}   # keyed by SKU
        self._discount_code: str | None = None
        self._customer_id = customer_id or "guest"
        self._inventory = inventory_service or InventoryService()
        self._pricing = pricing_service or PricingService()
        self._created_at = datetime.now()

    # ------------------------------------------------------------------
    # Item Management
    # ------------------------------------------------------------------

    def add_item(self, sku: str, quantity: int = 1) -> None:
        """
        Adds a product to the cart.

        Performs a live inventory check via InventoryService before
        adding. If the SKU is already in the cart the quantities are
        combined and rechecked against inventory.

        Raises:
            ItemNotFoundError: if the SKU does not exist in the catalogue.
            InvalidQuantityError: if quantity is not a positive integer.
            InsufficientStockError: if the total requested quantity
                                    exceeds available stock.
        """
        if quantity <= 0:
            raise InvalidQuantityError(quantity)

        if sku not in PRODUCT_CATALOGUE:
            raise ItemNotFoundError(sku)

        product = PRODUCT_CATALOGUE[sku]
        existing_qty = self._items[sku]["quantity"] if sku in self._items else 0
        total_qty = existing_qty + quantity

        available = self._inventory.get_stock(sku)
        if total_qty > available:
            raise InsufficientStockError(sku, total_qty, available)

        if sku in self._items:
            self._items[sku]["quantity"] = total_qty
        else:
            self._items[sku] = {
                "sku": sku,
                "name": product["name"],
                "unit_price": product["price"],
                "quantity": quantity,
                "category": product["category"],
            }

    def remove_item(self, sku: str) -> None:
        """
        Removes a product entirely from the cart.

        Raises:
            CartItemNotFoundError: if the SKU is not currently in the cart.
        """
        if sku not in self._items:
            raise CartItemNotFoundError(sku)
        del self._items[sku]

    def update_quantity(self, sku: str, quantity: int) -> None:
        """
        Updates the quantity of an existing cart item.

        Raises:
            CartItemNotFoundError: if the SKU is not in the cart.
            InvalidQuantityError: if the new quantity is not positive.
            InsufficientStockError: if the new quantity exceeds stock.
        """
        if sku not in self._items:
            raise CartItemNotFoundError(sku)
        if quantity <= 0:
            raise InvalidQuantityError(quantity)

        available = self._inventory.get_stock(sku)
        if quantity > available:
            raise InsufficientStockError(sku, quantity, available)

        self._items[sku]["quantity"] = quantity

    def clear(self) -> None:
        """Removes all items and resets the applied discount code."""
        self._items.clear()
        self._discount_code = None

    # ------------------------------------------------------------------
    # Discount Codes
    # ------------------------------------------------------------------

    def apply_discount_code(self, code: str) -> None:
        """
        Validates and stores a discount code for use at checkout.

        Only one discount code may be active at a time; applying a new
        code replaces the previous one.

        Raises:
            InvalidDiscountCodeError: if the code is unrecognised or expired.
        """
        self._pricing.validate_discount_code(code)
        self._discount_code = code.upper().strip()

    def remove_discount_code(self) -> None:
        """Clears the currently applied discount code, if any."""
        self._discount_code = None

    # ------------------------------------------------------------------
    # Totals & Summary
    # ------------------------------------------------------------------

    def get_subtotal(self) -> float:
        """Returns the sum of (unit_price × quantity) for all items."""
        return round(
            sum(i["unit_price"] * i["quantity"] for i in self._items.values()), 2
        )

    def get_discount_amount(self) -> float:
        """
        Returns the discount amount based on the active code.
        Returns 0.0 if no discount code is applied.
        """
        if not self._discount_code:
            return 0.0
        subtotal = self.get_subtotal()
        discounted = self._pricing.apply_discount(subtotal, self._discount_code)
        return round(subtotal - discounted, 2)

    def get_tax(self) -> float:
        """Returns the total tax across all current cart items."""
        return self._pricing.calculate_tax(list(self._items.values()))

    def get_total(self) -> float:
        """
        Returns the final order total:
          subtotal - discount + tax
        """
        return round(self.get_subtotal() - self.get_discount_amount() + self.get_tax(), 2)

    def get_item_count(self) -> int:
        """Returns the total number of individual units across all line items."""
        return sum(i["quantity"] for i in self._items.values())

    def get_items(self) -> list:
        """Returns a copy of the current cart items as a list of dicts."""
        return list(self._items.values())

    def is_empty(self) -> bool:
        """Returns True if the cart contains no items."""
        return len(self._items) == 0

    # ------------------------------------------------------------------
    # Checkout
    # ------------------------------------------------------------------

    def checkout(self) -> dict:
        """
        Finalises the cart and returns a structured order summary.

        Raises:
            EmptyCartError: if the cart contains no items.

        Returns:
            dict: order summary containing customer_id, line items,
                  subtotal, discount_code, discount_amount, tax,
                  total, and a timestamp.
        """
        if self.is_empty():
            raise EmptyCartError()

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
        return summary
