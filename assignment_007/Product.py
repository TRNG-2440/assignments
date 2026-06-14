"""Defines the abstract base `Product` class and the `ProductType` enum.

`Product` provides the shared attributes and behavior (ID, name, price,
stock management, and price calculation) that all concrete product types
(physical, digital, perishable) build upon.
"""

from abc import ABC, abstractmethod
from enum import IntEnum
from uuid import UUID, uuid4

from custom_exceptions import InvalidQuantityError


class ProductType(IntEnum):
    """Enumeration of the supported product categories.

    The integer values double as the menu choice numbers shown to the user
    when selecting a product type in the CLI.
    """

    PHYSICAL = 1
    DIGITAL = 2
    PERISHABLE = 3

    def __str__(self) -> str:
        """Returns the lowercased name when called via str(), matching StrEnum behavior."""
        return self.name.lower()


class Product(ABC):
    """Abstract base class representing a generic store product.

    Subclasses must implement `_get_shipping_cost` to define how shipping
    is calculated for that product type, and may override `_set_stock`,
    `total_price`, and `display_product_details` to customize behavior.
    """

    def __init__(self, product_name: str, price: float, stock: int = 999) -> None:
        """Initialize a new product.

        Args:
            product_name: The human-readable name of the product.
            price: The unit price of the product.
            stock: The initial available stock quantity. Defaults to 999
                (effectively "unlimited" for products that don't track stock).
        """
        # Auto-generate a unique identifier for this product
        self.product_id: UUID = uuid4()
        self.product_name: str = product_name
        self.unit_price: float = price
        # Internal stock counter; accessed via the `stock` property
        self._stock: int = stock

    @property
    def stock(self) -> int:
        """int: The current available stock quantity for this product."""
        return self._get_stock()

    @stock.setter
    def stock(self, value: int) -> None:
        """Set the available stock quantity.

        Args:
            value: The new stock quantity to set.

        Raises:
            InvalidQuantityError: If `value` is not a positive number.
        """
        self._set_stock(value)

    def _get_stock(self) -> int:
        """Return the raw stock value.

        Subclasses can override this to customize how stock is reported
        (e.g. digital products that report unlimited stock).

        Returns:
            The current stock quantity.
        """
        return self._stock

    def _set_stock(self, value: int) -> None:
        """Validate and store a new stock quantity.

        Args:
            value: The new stock quantity to assign.

        Raises:
            InvalidQuantityError: If `value` is less than or equal to zero.
        """
        if value <= 0:
            raise InvalidQuantityError(value)
        self._stock = value

    @property
    def shipping_cost(self) -> float:
        """float: The shipping cost for a single unit of this product."""
        return self._get_shipping_cost()

    @abstractmethod
    def _get_shipping_cost(self) -> float:
        """Calculate the shipping cost for this product.

        Must be implemented by concrete subclasses, since shipping rules
        differ between physical, digital, and perishable products.

        Returns:
            The shipping cost as a float.
        """
        pass

    def display_product_details(self):
        """Print the common product details to the console.

        Subclasses should call `super().display_product_details()` and then
        print any additional, type-specific attributes.
        """
        print("==============================")
        print(f"Product Id: {self.product_id}")
        print(f"Product Name: {self.product_name}")
        print(f"Unit Price: ${self.unit_price}")
        print(f"In Stock: {self.stock}")

    def total_price(self, quantity: int) -> float:
        """Calculate the total price for purchasing a given quantity.

        The base implementation simply multiplies unit price by quantity,
        with no shipping cost included. Subclasses override this to add
        shipping or other type-specific adjustments.

        Args:
            quantity: The number of units being purchased.

        Returns:
            The total price (before any shipping adjustments) as a float.
        """
        return self.unit_price * quantity
