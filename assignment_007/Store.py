"""Defines the `Store` class, which manages the product inventory for the
PyStore Inventory System (add/remove/restock/search/sell products)."""

from typing import List
from uuid import UUID, uuid4

from Product import Product
from custom_exceptions import (
    InvalidQuantityError,
    ProductAlreadyExistsError,
    ProductDoesNotExistError,
    ProductExpiredError,
)


class Store:
    """Manages a collection of `Product` instances and inventory operations."""

    def __init__(self) -> None:
        """Initialize an empty store with a generated ID and default name."""
        self.store_id: UUID = uuid4()
        self.store_name = "Pystore"
        # Maps product ID -> Product instance for fast lookup
        self.products: dict[UUID, Product] = {}

    def add_product(self, product: Product) -> None:
        """Add a new product to the inventory.

        Args:
            product: The `Product` instance to add.

        Raises:
            ProductAlreadyExistsError: If a product with the same ID is
                already present in the store (should not normally occur
                since IDs are auto-generated UUIDs).
        """
        if product.product_id in self.products:
            raise ProductAlreadyExistsError(product.product_id)
        else:
            self.products[product.product_id] = product

    def remove_product(self, product_id: UUID) -> None:
        """Remove a product from the inventory by its ID.

        Args:
            product_id: The UUID of the product to remove.

        Raises:
            ProductDoesNotExistError: If no product with the given ID exists.
        """
        if product_id in self.products:
            del self.products[product_id]
        else:
            raise ProductDoesNotExistError(product_id)

    def restock_product(self, product_id: UUID, quantity: int) -> None:
        """Increase the stock of an existing product.

        Args:
            product_id: The UUID of the product to restock.
            quantity: The number of additional units to add to stock.

        Raises:
            InvalidQuantityError: If `quantity` is not positive.
            ProductDoesNotExistError: If no product with the given ID exists.
            ProductExpiredError: If the product is a perishable item that
                has already expired.
        """
        if quantity <= 0:
            raise InvalidQuantityError(quantity)

        if product_id not in self.products:
            raise ProductDoesNotExistError(product_id)

        product: Product = self.products[product_id]
        # Block restocking of expired perishable products
        if hasattr(product, "is_expired") and getattr(product, "is_expired"):
            raise ProductExpiredError(
                product_id, product.product_name, getattr(product, "expiration_date")
            )

        try:
            # Uses the `stock` property setter, which validates the new value
            product.stock += quantity
        except InvalidQuantityError as e:
            print(e)

    def sell_product(self, product_id: UUID, quantity: int) -> None:
        """Decrease a product's stock to fulfill a sale.

        Args:
            product_id: The UUID of the product being sold.
            quantity: The number of units being sold.

        Raises:
            InvalidQuantityError: If `quantity` is not positive, or if
                deducting it would result in an invalid stock value.
            ProductDoesNotExistError: If no product with the given ID exists.
        """
        if quantity <= 0:
            raise InvalidQuantityError(quantity)

        if product_id not in self.products:
            raise ProductDoesNotExistError(product_id)

        product: Product = self.products[product_id]
        try:
            # Uses the `stock` property setter, which validates the new value
            product.stock -= quantity
        except InvalidQuantityError:
            raise InvalidQuantityError(quantity)

    def get_product(self, product_id: UUID) -> Product:
        """Retrieve a product by its ID.

        Args:
            product_id: The UUID of the product to retrieve.

        Returns:
            The `Product` instance associated with `product_id`.

        Raises:
            ProductDoesNotExistError: If no product with the given ID exists.
        """
        if product_id not in self.products:
            raise ProductDoesNotExistError(product_id)
        return self.products[product_id]

    def search_by_product_name(self, search_str: str) -> None:
        """Search for and display products whose name contains the given string.

        The match is case-insensitive and supports partial matches.

        Args:
            search_str: The substring to search for within product names.
        """
        filtered_products = [
            product
            for product in self.products.values()
            if search_str.lower() in product.product_name.lower()
        ]
        if filtered_products:
            self._list_products(filtered_products)
        else:
            print("No products found!")

    @staticmethod
    def _list_products(products: List[Product]) -> None:
        """Print details for each product in the given list.

        Args:
            products: The list of `Product` instances to display.
        """
        for product in products:
            product.display_product_details()
            print()

    def list_all_products(self) -> None:
        """Print details for every product currently in the inventory.

        If the inventory is empty, prints a "No products found!" message
        instead.
        """
        if self.products:
            for product in self.products.values():
                product.display_product_details()
                print()
        else:
            print("No products found!")
