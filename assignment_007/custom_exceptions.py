"""Custom exception classes used throughout the PyStore inventory system.

Each exception extends ValueError (or another built-in) and provides a
human-readable message tailored to the specific failure scenario, so callers
can simply ``print(e)`` to display useful feedback to the user.
"""

from datetime import date
from uuid import UUID


class ProductAlreadyExistsError(ValueError):
    """Raised when attempting to add a product whose ID is already in the store."""

    def __init__(self, product_id: UUID) -> None:
        """Initialize the error with the conflicting product ID.

        Args:
            product_id: The UUID of the product that already exists in the store.
        """
        super().__init__(f"Product with id: {product_id} already exists!")


class ProductDoesNotExistError(ValueError):
    """Raised when an operation references a product ID that isn't in the store."""

    def __init__(self, product_id: UUID) -> None:
        """Initialize the error with the missing product ID.

        Args:
            product_id: The UUID of the product that could not be found.
        """
        super().__init__(f"Product with id: {product_id} does not exist!")


class InvalidQuantityError(ValueError):
    """Raised when a quantity (stock, order amount, etc.) is not a positive value."""

    def __init__(self, quantity: int | float) -> None:
        """Initialize the error with the offending quantity.

        Args:
            quantity: The invalid (non-positive) quantity that triggered the error.
        """
        super().__init__(f"Given quantity: {quantity} is invalid! It must be positive")


class ProductExpiredError(ValueError):
    """Raised when an operation is attempted on an expired perishable product."""

    def __init__(
        self, product_id: UUID, product_name: str, expiration_date: date
    ) -> None:
        """Initialize the error with details about the expired product.

        Args:
            product_id: The UUID of the expired product.
            product_name: The display name of the expired product.
            expiration_date: The date on which the product expired.
        """
        super().__init__(f"{product_id}: {product_name} expired on {expiration_date}!")


class InvalidInputError(ValueError):
    """Raised when user-provided CLI input cannot be converted to the expected type."""

    def __init__(self, *args: object) -> None:
        """Initialize the error.

        Args:
            *args: Arguments forwarded to `ValueError.__init__`, typically a
                descriptive error message.
        """
        super().__init__(*args)
