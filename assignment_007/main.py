"""Command-line entry point for the PyStore Inventory System.

Provides a menu-driven loop allowing the user to act as a store manager
(add/remove/restock/list products) or a customer (browse/search/place
orders).
"""

from typing import Any, Optional
from uuid import UUID

from Store import Store
from Product import Product, ProductType
from ProductFactory import ProductFactory
from Order import Order
from custom_exceptions import InvalidQuantityError
from utils import try_cast_to_float, try_cast_to_int


def print_product_types() -> None:
    """Print the list of available product types and their menu numbers."""
    print("Product Type:")
    for product_type in ProductType:
        print(f"[{product_type.value}] {product_type}")


def create_product(product_type: ProductType) -> Optional[Product]:
    """Prompt the user for product details and construct a new `Product`.

    Collects shared attributes (name, price) plus any attributes specific
    to the given `product_type` (e.g. weight and shipping rate for
    physical products, expiration date for perishable products), then
    delegates construction to `ProductFactory`.

    Args:
        product_type: The type of product to create.

    Returns:
        The newly created `Product` instance, or `None` if construction
        did not occur.

    Raises:
        Exception: Any exception raised while reading input or validating
            values (e.g. `InvalidQuantityError`) is re-raised to the caller.
    """
    try:
        # Attributes common to all product types
        kwargs: dict[str, Any] = {
            "product_name": input("Name: "),
            "price": try_cast_to_float(prompt="Unit price: "),
        }

        if kwargs["price"] and kwargs["price"] <= 0:
            raise InvalidQuantityError(kwargs["price"])

        if product_type == ProductType.PHYSICAL:
            # Physical products require stock, weight, and a shipping rate
            kwargs["stock"] = try_cast_to_int(prompt="Stock quantity: ")
            kwargs["weight"] = try_cast_to_float(prompt="Weight (kg): ")
            kwargs["shipping_cost_per_unit"] = try_cast_to_float(
                prompt="Shipping Cost per kg ($): "
            )

            if kwargs["stock"] and kwargs["stock"] <= 0:
                raise InvalidQuantityError(kwargs["stock"])
            if kwargs["weight"] and kwargs["weight"] <= 0:
                raise InvalidQuantityError(kwargs["weight"])
            if (
                kwargs["shipping_cost_per_unit"]
                and kwargs["shipping_cost_per_unit"] <= 0
            ):
                raise InvalidQuantityError(kwargs["shipping_cost_per_unit"])

        elif product_type == ProductType.DIGITAL:
            # Digital products require a file size and download URL (no stock)
            kwargs["file_size_in_mb"] = try_cast_to_float(prompt="File Size (MB): ")
            kwargs["download_url"] = input("Download Link URL: ")
        elif product_type == ProductType.PERISHABLE:
            # Perishable products require stock and an expiration date
            kwargs["stock"] = try_cast_to_int(prompt="Stock Quantity: ")
            kwargs["expiration_date"] = input("Expiration Date (YYYY-MM-DD): ")

            if kwargs["stock"] and kwargs["stock"] <= 0:
                raise InvalidQuantityError(kwargs["stock"])
        new_product = ProductFactory.create_product(product_type, **kwargs)
    except Exception as e:
        raise e

    return new_product


def manager_menu() -> None:
    """Run the interactive manager menu loop.

    Allows the manager to add, remove, restock, and list products until
    they choose to return to the main menu.
    """
    while True:
        print("--- Manager Menu ---")
        print("[1] Add product")
        print("[2] Remove product")
        print("[3] Restock product")
        print("[4] List all inventory")
        print("[5] Back")

        action = 0
        try:
            action: int = try_cast_to_int(prompt="Enter your choice: ")  # type: ignore
        except Exception as e:
            print(e)
            continue

        match action:
            case 1:
                # Add a new product of the chosen type to the store
                print_product_types()
                try:
                    product_type: ProductType = ProductType(
                        try_cast_to_int(prompt="Enter product_type: ")
                    )
                    product: Optional[Product] = create_product(product_type)
                    if product:
                        store.add_product(product)
                        product.display_product_details()
                except Exception as e:
                    print(e)
            case 2:
                # Remove a product from the store by ID
                store.list_all_products()
                try:
                    product_id: UUID = UUID(input("Enter product id to remove: "))
                    store.remove_product(product_id)
                except Exception as e:
                    print(e)
            case 3:
                # Increase the stock of an existing product
                store.list_all_products()
                try:
                    product_id: UUID = UUID(input("Enter product id to restock: "))
                    stock: int = try_cast_to_int("Enter quantity to add: ")  # type: ignore
                    store.restock_product(product_id, stock)
                except Exception as e:
                    print(e)
            case 4:
                # Display the full inventory
                store.list_all_products()
            case 5:
                # Return to the main menu
                break
            case _:
                print("Invalid choice! Try again...")


def customer_menu() -> None:
    """Run the interactive customer menu loop.

    Allows the customer to browse all products, search by name, and place
    orders until they choose to return to the main menu.
    """
    while True:
        print("--- Customer Menu ---")
        print("[1] Browse all products")
        print("[2] Search by name")
        print("[3] Place an order")
        print("[4] Back")

        action = 0
        try:
            action: int = try_cast_to_int(prompt="Enter your choice: ")  # type: ignore
        except Exception as e:
            print(e)
            continue

        match action:
            case 1:
                # Display all available products
                store.list_all_products()
            case 2:
                # Search for products by (partial, case-insensitive) name
                try:
                    search_str: str = input("Search: ")
                    store.search_by_product_name(search_str)
                except Exception as e:
                    print(e)
            case 3:
                # Place an order for a product by ID and quantity
                try:
                    product_id: UUID = UUID(input("Product id: "))
                    stock: int = try_cast_to_int("Quantity to add: ")  # type: ignore
                    product: Product = store.get_product(product_id)

                    order: Order = Order(store, product, stock)
                    order.checkout()
                except Exception as e:
                    print(e)
            case 4:
                # Return to the main menu
                break
            case _:
                print("Invalid choice! Try again...")


if __name__ == "__main__":
    # Create the store instance shared by both the manager and customer menus
    store: Store = Store()
    while True:
        print("==============================")
        print(f"{store.store_name} Inventory System")
        print("==============================")

        print("[1] Manager Menu")
        print("[2] Customer Menu")
        print("[3] Quit")

        menu = 0
        try:
            menu = try_cast_to_int(prompt="Enter your choice: ")
        except Exception as e:
            print(e)
            continue

        match menu:
            case 1:
                manager_menu()
            case 2:
                customer_menu()
            case 3:
                # Exit the application
                break
            case _:
                print("Invalid choice! Try again...")
