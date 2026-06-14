"""Defines the `Order` class, which represents a single customer order and
handles verification, stock deduction, and order summary display."""

from uuid import UUID, uuid4

from Product import Product
from Store import Store
from PerishableProduct import MINIMUM_ORDER_ABOVE, PerishableProduct
from custom_exceptions import (
    InvalidQuantityError,
    ProductDoesNotExistError,
    ProductExpiredError,
)


class Order:
    """Represents a customer's request to purchase a quantity of a product."""

    def __init__(self, store: Store, product: Product, quantity: int) -> None:
        """Initialize a new order.

        Args:
            store: The `Store` instance the product belongs to (used to
                verify availability and deduct stock).
            product: The `Product` being ordered.
            quantity: The number of units requested.
        """
        # Auto-generate a unique identifier for this order
        self.order_id: UUID = uuid4()
        self.store = store
        self.product = product
        self.quantity = quantity

    def checkout(self) -> None:
        """Attempt to place the order and either print a summary or a
        cancellation message.

        Verifies stock availability and deducts inventory via the store;
        if verification fails, the order is cancelled and a message is
        printed instead of the order summary.
        """
        if not self._verify_and_place_order():
            print(f"Order {self.order_id} cancelled!")
        else:
            self.generate_order_summary()

    def generate_order_summary(self) -> None:
        """Print a formatted receipt-style summary of the completed order.

        Includes the product name, quantity, unit price, subtotal,
        shipping cost (waived for perishable orders above the free-shipping
        threshold), and final total.
        """
        subtotal: float = self.product.unit_price * self.quantity
        shipping_cost: float = self.product.shipping_cost
        # Waive shipping for perishable orders whose subtotal exceeds the threshold
        if (
            isinstance(self.product, PerishableProduct)
            and subtotal > MINIMUM_ORDER_ABOVE
        ):
            shipping_cost = 0
        print("==============================")
        print("         ORDER SUMMARY        ")
        print("==============================")
        print(f" {self.product.product_name} x{self.quantity}")
        print(f" Unit Price : ${self.product.unit_price}")
        print(f" Subtotal : ${subtotal}")
        print(f" Shipping : ${shipping_cost}")
        print("---------------------")
        print(f" Total: ${self.product.total_price(self.quantity)}")
        print("==============================")

    def _verify_and_place_order(self) -> bool:
        """Check stock availability and deduct inventory for this order.

        Returns:
            True if the order was successfully verified and placed
            (stock deducted via the store); False if the order could not
            be fulfilled (insufficient stock, missing product, invalid
            quantity, or an expired perishable product).
        """
        product_id: UUID = self.product.product_id
        try:
            # Pre-check stock so we can give a friendly "only N left" message
            if self.product.stock < self.quantity:
                print(
                    f"{product_id}: {self.product.product_name} has only {self.product.stock} items left! Cannot order {self.quantity} items."
                )
                return False

            # Deduct stock through the store (handles digital products' no-op stock)
            self.store.sell_product(product_id, self.quantity)
        except ProductDoesNotExistError as e:
            print(e)
            return False
        except InvalidQuantityError as e:
            print(e)
            return False
        except ProductExpiredError as e:
            print(e)
            return False
        return True
