"""Defines `PerishableProduct`, a `Product` subclass for goods that expire
and use flat-rate shipping (waived above a minimum order total)."""

from datetime import date

from Product import Product
from custom_exceptions import InvalidQuantityError, ProductExpiredError

# Flat shipping fee applied to every perishable order
SHIPPING_FEE = 3.99
# Pre-shipping order total above which shipping is waived
MINIMUM_ORDER_ABOVE = 25


class PerishableProduct(Product):
    """A product with an expiration date and flat-rate shipping.

    Shipping is a flat fee per order, unless the pre-shipping order total
    exceeds `MINIMUM_ORDER_ABOVE`, in which case shipping is free. Expired
    products cannot have their stock increased or be sold.
    """

    def __init__(
        self,
        product_name: str,
        price: float,
        stock: int,
        expiration_date: str,
    ) -> None:
        """Initialize a perishable product.

        Args:
            product_name: The human-readable name of the product.
            price: The unit price of the product.
            stock: The initial available stock quantity.
            expiration_date: The expiration date as an ISO format string
                (YYYY-MM-DD).
        """
        super().__init__(product_name, price, stock)
        # Parse the ISO date string into a `date` object for comparisons
        self.expiration_date: date = date.fromisoformat(expiration_date)

    @property
    def is_expired(self) -> bool:
        """bool: True if today's date is on or after the expiration date."""
        return date.today() >= self.expiration_date

    def _get_shipping_cost(self) -> float:
        """Return the flat shipping fee applied to perishable products.

        Returns:
            The constant `SHIPPING_FEE` value.
        """
        return SHIPPING_FEE

    def _set_stock(self, value: int) -> None:
        """Validate and store a new stock quantity, blocking expired products.

        Args:
            value: The new stock quantity to assign.

        Raises:
            InvalidQuantityError: If `value` is less than or equal to zero.
            ProductExpiredError: If the product has already expired.
        """
        if value <= 0:
            raise InvalidQuantityError(value)
        if self.is_expired:
            raise ProductExpiredError(
                self.product_id, self.product_name, self.expiration_date
            )
        self._stock = value

    def total_price(self, quantity: int) -> float:
        """Calculate the total price, applying flat shipping unless the
        pre-shipping total exceeds the free-shipping threshold.

        Args:
            quantity: The number of units being purchased.

        Returns:
            The pre-shipping total plus the flat shipping fee, or just the
            pre-shipping total if it exceeds `MINIMUM_ORDER_ABOVE`.
        """
        pre_shipping_total: float = super().total_price(quantity)
        return (
            pre_shipping_total + SHIPPING_FEE
            if pre_shipping_total <= MINIMUM_ORDER_ABOVE
            else pre_shipping_total
        )

    def display_product_details(self) -> None:
        """Print common product details plus the expiration date."""
        super().display_product_details()
        print(f"Expires By: {self.expiration_date}")
        print("==============================")
