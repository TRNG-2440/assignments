"""
cart_exceptions.py

Custom exception hierarchy for the e-commerce shopping cart application.

This module is provided as part of the application under test for the
Shopping Cart Unit Testing activity. Do not modify this file.

All exceptions inherit from CartError, allowing callers to catch either
a specific exception type or any cart-related error with a single clause.
"""


class CartError(Exception):
    """Base exception for all shopping cart errors."""
    pass


class ItemNotFoundError(CartError):
    """Raised when an item does not exist in the product catalogue."""
    def __init__(self, sku: str):
        self.sku = sku
        super().__init__(f"No product found with SKU '{sku}'.")


class InsufficientStockError(CartError):
    """Raised when requested quantity exceeds available inventory."""
    def __init__(self, sku: str, requested: int, available: int):
        self.sku = sku
        self.requested = requested
        self.available = available
        super().__init__(
            f"Insufficient stock for SKU '{sku}': "
            f"requested {requested}, only {available} available."
        )


class InvalidQuantityError(CartError):
    """Raised when a quantity value is zero or negative."""
    def __init__(self, quantity: int):
        self.quantity = quantity
        super().__init__(
            f"Invalid quantity '{quantity}': quantity must be a positive integer."
        )


class InvalidDiscountCodeError(CartError):
    """Raised when a discount code is unrecognised or expired."""
    def __init__(self, code: str, reason: str = "invalid or expired"):
        self.code = code
        super().__init__(f"Discount code '{code}' is {reason}.")


class EmptyCartError(CartError):
    """Raised when checkout is attempted on an empty cart."""
    def __init__(self):
        super().__init__("Cannot check out: the cart is empty.")


class CartItemNotFoundError(CartError):
    """Raised when attempting to remove or update an item not in the cart."""
    def __init__(self, sku: str):
        self.sku = sku
        super().__init__(f"SKU '{sku}' is not in the cart.")
