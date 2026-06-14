"""Defines `PhysicalProduct`, a `Product` subclass for shippable physical goods."""

from Product import Product


class PhysicalProduct(Product):
    """A tangible product that incurs a weight-based shipping cost."""

    def __init__(
        self,
        product_name: str,
        price: float,
        stock: int,
        weight: float,
        shipping_cost_per_unit: float,
    ) -> None:
        """Initialize a physical product.

        Args:
            product_name: The human-readable name of the product.
            price: The unit price of the product.
            stock: The initial available stock quantity.
            weight: The weight of a single unit (in kg).
            shipping_cost_per_unit: The shipping cost charged per kg of weight.
        """
        super().__init__(product_name, price, stock)
        self.weight: float = weight
        # Rate used to scale shipping cost based on the product's weight
        self.shipping_cost_per_kg: float = shipping_cost_per_unit

    def _get_shipping_cost(self) -> float:
        """Calculate shipping cost for one unit based on its weight.

        Returns:
            The product's weight multiplied by the per-kg shipping rate.
        """
        return self.weight * self.shipping_cost_per_kg

    def total_price(self, quantity: int) -> float:
        """Calculate the total price including shipping cost.

        Args:
            quantity: The number of units being purchased.

        Returns:
            The base total price (unit price * quantity) plus the
            per-unit shipping cost.
        """
        return super().total_price(quantity) + self.shipping_cost

    def display_product_details(self) -> None:
        """Print common product details plus physical-specific attributes
        (weight, shipping cost per kg, and total shipping cost)."""
        super().display_product_details()
        print(f"Unit Weight: {self.weight} kg")
        print(f"Shipping cost per kg: ${self.shipping_cost_per_kg}")
        print(f"Total shipping cost: ${self.shipping_cost}")
        print("==============================")
