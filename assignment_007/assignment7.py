"""
Assignment 7
# Python Coding Activity 7 - Online Store Inventory System

## Objective

In this activity, you will design and implement an inventory management system for an online store. You will practice core OOP concepts including:

- Abstract base classes and interface design
- Inheritance with specialized subclass behavior
- Encapsulation and property validation
- Polymorphism through shared methods with type-specific logic
- Composition (a `Store` class that owns and manages product objects)
- Exception handling for invalid inventory operations
- Basic CLI interaction via a menu-driven loop

---

## Instructions

You will build an inventory system that supports three types of products: **Physical**, **Digital**, and **Perishable**. Each product type shares a common interface but has unique behaviors and attributes.

1. Create a base `Product` class that holds common attributes such as product ID, name, price, and stock quantity. It should support a method to display product details and a method to calculate a total price for a given quantity.

2. Create a `PhysicalProduct` subclass with the following unique behavior:
   - Has a weight attribute (in kg or lbs) used to calculate a shipping cost. Shipping cost should scale with weight.
   - Overrides the total price calculation to include the calculated shipping cost.

3. Create a `DigitalProduct` subclass with the following unique behavior:
   - Has a file size attribute and a download URL.
   - Has no shipping cost — its total price is always just the item price.
   - Stock is not limited in the traditional sense; purchasing a digital product does not reduce available stock.

4. Create a `PerishableProduct` subclass with the following unique behavior:
   - Has an expiration date attribute.
   - Includes a method to check if the product is expired based on today's date. You will need to import the `datetime` module.
   - Expired products cannot be added to a customer order.
   - Has a flat-rate shipping cost applied to all orders. However, if the pre-shipping order total exceeds $25.00, shipping is free.

5. Create a `Store` class that manages the full product inventory. It should support:
   - Adding a new product of any supported type to the inventory
   - Removing a product by ID
   - Restocking an existing product (increasing its quantity)
   - Searching for products by name (partial matches count)
   - Listing all in-stock products

6. Create a simple `Order` system — when a customer places an order, the store should:
   - Verify the product exists and is in stock (and not expired, if perishable)
   - Deduct the appropriate quantity from inventory (except for digital products)
   - Return an order summary with the total cost including any applicable shipping

7. Build a CLI menu loop that lets the user interact with the store as either a **store manager** (add, remove, restock products) or a **customer** (browse, search, and place orders).

---

## Example Interaction

```
==============================
   PyStore Inventory System
==============================

[1] Manager Menu
[2] Customer Menu
[3] Quit

> 1

--- Manager Menu ---
[1] Add product
[2] Remove product
[3] Restock product
[4] List all inventory
[5] Back

> 1

Product type:
[1] Physical
[2] Digital
[3] Perishable
> 3

Name: Organic Strawberries
Price: 4.99
Stock quantity: 30
Expiration date (YYYY-MM-DD): 2025-06-15

Perishable product added.
   ID: PRD-0041  |  Organic Strawberries  |  $4.99  |  Expires: 2025-06-15

------------------------------

> 2

--- Customer Menu ---
[1] Browse all products
[2] Search by name
[3] Place an order
[4] Back

> 2
Search: straw

Results:
  [PRD-0041]  Organic Strawberries  |  $4.99  |  In Stock: 30  |  Expires: 2025-06-15

> 3
Product ID: PRD-0041
Quantity: 5

==============================
         Order Summary
==============================
  Organic Strawberries x5
  Unit Price : $4.99
  Subtotal   : $24.95
  Shipping   : $3.99  (flat-rate)
  ---------------------
  Total      : $28.94
==============================
Order placed! Remaining stock: 25

------------------------------

> 3
Product ID: PRD-0041
Quantity: 6

==============================
         Order Summary
==============================
  Organic Strawberries x6
  Unit Price : $4.99
  Subtotal   : $29.94
  Shipping   : $0.00  (free over $25)
  ---------------------
  Total      : $29.94
==============================
Order placed! Remaining stock: 19

------------------------------

> 3
Product ID: PRD-0041
Quantity: 2

Error: Organic Strawberries has expired and cannot be ordered.
```

> **NOTE:** The example above is for illustrative purposes - either the order would succeed, or it would fail for expired products, not both.

---

## Requirements Checklist

- [ ] A base `Product` class exists with shared attributes and a price calculation method
- [ ] `PhysicalProduct` calculates shipping cost based on weight and includes it in the total
- [ ] `DigitalProduct` has no shipping cost and its stock is unaffected by purchases
- [ ] `PerishableProduct` stores an expiration date and correctly identifies expired products
- [ ] `PerishableProduct` applies a flat-rate shipping cost to all orders
- [ ] `PerishableProduct` shipping is waived when the pre-shipping order total exceeds $25.00
- [ ] Expired `PerishableProduct` items are blocked from being ordered
- [ ] A `Store` class manages a collection of products and supports add, remove, restock, and search
- [ ] Product IDs are auto-generated and unique
- [ ] Searching by name supports partial, case-insensitive matches
- [ ] Placing an order correctly deducts stock (except for digital products)
- [ ] Orders for out-of-stock items are rejected with a clear error message
- [ ] Orders for quantities exceeding available stock are rejected
- [ ] Restocking a non-existent product ID raises an appropriate error
- [ ] Removing a product that does not exist raises an appropriate error
- [ ] The CLI handles invalid input (bad product IDs, non-numeric quantities, invalid dates) without crashing
- [ ] Each product type overrides the detail display method to show its unique attributes

---

## Stretch Goals

- **Discount System** — Add a `apply_discount(percent)` method to the base `Product` class that temporarily reduces a product's price. Add a manager menu option to apply a store-wide sale to all products of a given type.

- **Persistence** — Save and load the full inventory to/from a JSON file so product data survives between sessions. You will need to handle serialization carefully to preserve each subclass's unique attributes and restore the correct type on load.

- **Expiration Sweep** — Add a manager menu option that scans the inventory and automatically removes all expired `PerishableProduct` items, printing a report of what was removed.

- **Order History** — Track all placed orders in memory with a timestamp, product name, quantity, and total cost. Add a customer menu option to view past orders from the current session.

- **Low Stock Alerts** — After every order or restock operation, check if any product's stock has fallen below a defined threshold (e.g. 5 units) and print a warning to the manager view.
"""
from abc import ABC, abstractmethod
from datetime import datetime, date
from enum import StrEnum

from assignments.shared.menu import Menu


class ProductType(StrEnum):
    PHYSICAL = "Physical"
    DIGITAL = "Digital"
    PERISHABLE = "Perishable"

class Product(ABC):

    def __init__(self, type: ProductType, id: str, name: str, price: float, quantity: int):
        self._type = type
        self._id = id
        self._name = name
        self._price = price
        self._quantity = quantity

    def display_str(self) -> str:
        return (f"Name: {self._name}"
                f"\nType: {self._type}"
                f"\nID: {self._id}"
                f"\nPrice per Unit: ${self._price:,.2f}"
                f"\nQuantity Available: {self._quantity}"
                )

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def get_quantity(self):
        return self._quantity

    def increase_quantity(self, quantity_to_add: int):
        if quantity_to_add < 0:
            raise ValueError(f"Must add a positive quantity, instead got: {quantity_to_add}")
        self. _quantity += quantity_to_add

    @abstractmethod
    def get_cost(self, to_buy: int) -> float:
        """
        Gets the cost for purchasing an amount of product
        :param to_buy:
        """
        pass

    @abstractmethod
    def buy(self, amount: int) -> bool:
        """
        Purchases the product.
        :param amount:
        :raises ValueError if there is not enough quantity to purchase the product:
        :returns True if successful:
        """
        pass

class PhysicalProduct(Product):

    def __init__(self, id: str, name: str, price: float, quantity: int, weight_kg: float, shipping_cost_kg: float):
        super().__init__(ProductType.PHYSICAL, id, name, price, quantity)
        self.weight_kg = weight_kg
        self.shipping_cost_kg = shipping_cost_kg

    def display_str(self) -> str:
        return super().display_str() + (f"\nWeight of Item: {self.weight_kg:,.1f}kg"
                                        f"\nShipping cost per kg: ${self.shipping_cost_kg:,.2f}")

    def get_cost(self, to_buy: int) -> float:
        return to_buy * self.weight_kg * self.shipping_cost_kg + to_buy * self._price

    def buy(self, amount: int) -> bool:
        if amount > self._quantity:
            raise ValueError(f"Insufficient Quantity (Quantity: {self._quantity}, Wanted: {amount})")
        self._quantity -= amount
        return True

class DigitalProduct(Product):

    def __init__(self, id: str, name: str, price: float, quantity: int, file_size_mb: float, download_url: str):
        super().__init__(ProductType.DIGITAL, id, name, price, quantity)
        self._file_size_mb = file_size_mb
        self._download_url = download_url

    def display_str(self) -> str:
        return super().display_str() + (f"\nFile Size: {self._file_size_mb:,.1f}MB"
                                        f"\nDownload URL: {self._download_url}")

    def get_file_size(self):
        return self._file_size_mb

    def get_download_url(self):
        return self._download_url

    def get_cost(self, to_buy: int) -> float:
        return self._price * to_buy

    def buy(self, amount: int) -> bool:
        return True



class PerishableProduct(Product):

    def __init__(self, id: str, name: str, price: float, quantity: int, expiration_date: date, shipping_cost: float, shipping_free_limit: float):
        super().__init__(ProductType.PERISHABLE, id, name, price, quantity)
        self._expiration_date = expiration_date
        self._shipping_cost = shipping_cost
        self._shipping_free_limit = shipping_free_limit

    def display_str(self) -> str:
        return super().display_str() + (f"\nExpiration: {self._expiration_date:}"
                                        f"\nShipping Cost: {self._shipping_cost}"
                                        f"\nFree Shipping Minimum: {self._shipping_free_limit}")

    def get_cost(self, to_buy: int) -> float:
        total: float = to_buy * self._price
        if total >= self._shipping_free_limit:
            return total
        return total + self._shipping_cost

    def buy(self, amount: int) -> bool:
        if date.today() > self._expiration_date:
            raise Expired(f"This product expired on {self._expiration_date}")
        if amount > self._quantity:
            raise ValueError(f"Insufficient Quantity (Quantity: {self._quantity}, Wanted: {amount})")
        self._quantity -= amount
        return True

class Expired(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Store:
    PRICE_PER_KG = 0.10
    PERISHABLE_SHIPPING = 5
    PERISHABLE_MIN_FREE = 25


    def __init__(self):
        self._products: dict[str, Product] = {}
        self._next_id = 0

    def create_product(self,
                       type: ProductType,
                       name: str,
                       price: float,
                       quantity: int,
                       /,
                       weight_kg: float = None,
                       file_size_mb: float = None,
                       download_url: str = None,
                       expiration_date: date = None) -> Product:
        new_product: Product
        match type:
            case ProductType.PHYSICAL:
                if weight_kg is None or weight_kg <= 0:
                    raise ValueError(f"Physical Products must have a positive weight, found: {weight_kg}")
                new_product = PhysicalProduct(self._generate_product_id(), name, price, quantity, weight_kg, self.PRICE_PER_KG)

            case ProductType.DIGITAL:
                if file_size_mb is None or file_size_mb <= 0:
                    raise ValueError(f"Digital Products must have a positive file size, found: {file_size_mb}")

                if download_url is None:
                    raise ValueError(f"Digital Products must have a download url, found: {download_url}")

                new_product = DigitalProduct(self._generate_product_id(), name, price, quantity, file_size_mb, download_url)

            case ProductType.PERISHABLE:
                if expiration_date is None:
                    raise ValueError(f"Perishable Products must have an expiration date, found: {expiration_date}")

                new_product = PerishableProduct(self._generate_product_id(), name, price, quantity, expiration_date, self.PERISHABLE_SHIPPING, self.PERISHABLE_MIN_FREE)

        self._products[new_product.get_id()] = new_product
        return new_product

    def _generate_product_id(self):
        prd_id: str = "PRD_" + str(self._next_id)
        self._next_id += 1
        return prd_id

    def remove_product(self, id: str) -> bool:
        if id in self._products:
            del self._products
            return True
        return False

    def search_product(self, name: str) -> list[Product]:
        found_products: list[Product] = []
        for product in self._products.values():
            if name.lower() in product.get_name():
                found_products.append(product)
        return found_products

    def get_product(self, id: str) -> Product:
        return self._products[id]

    def has_product(self, prod_id: str):
        return prod_id in self._products

    def restock_product(self, id: str, quantity_to_add: int) -> bool:
        if id in self._products:
            self._products[id].increase_quantity(quantity_to_add)
            return True
        return False

    def get_in_stock_products(self) -> list[Product]:
        return [product for product in self._products.values() if product.get_quantity() > 0]

    def get_all_products(self) -> list[Product]:
        return [product for product in self._products.values()]


class StoreMenu(Menu):
    def __init__(self, store: Store):
        super().__init__({
            "Manager Menu": self.manager_menu,
            "Customer Menu": self.customer_menu,
        },
            add_quit=True
        )
        self.store = store

    def manager_menu(self) -> None:
        ManagerMenu(self.store).start()

    def customer_menu(self) -> None:
        pass

class ManagerMenu(Menu):

    def __init__(self, store: Store):
        super().__init__({
            "Add product": self.add_product,
            "Remove product": self.remove_product,
            "Restock product": self.restock_product,
            "List all inventory": self.list_all_inventory,
            "Back": self.quit
        })
        self.store = store

    def add_product(self) -> None:
        AddProductMenu(self.store).do_selection()

    def remove_product(self) -> None:
        print("Remove Product")
        product_id: str = Menu.get_str("Product ID: ", test=lambda text: self.store.has_product(text))
        if self.store.remove_product(product_id):
            print(f"Removed Product {product_id}")

    def restock_product(self) -> None:
        print("Restock Product")
        product_id: str = Menu.get_str("Product ID: ", test=lambda text: self.store.has_product(text))
        quantity: int = Menu.get_positive_int("Additional Quality: ")

        self.store.restock_product(product_id, quantity)
        print(f"Restocked Product: {product_id} (+{quantity}")

    def list_all_inventory(self) -> None:
        print(Menu.MINOR_DIVIDER)
        for product in self.store.get_all_products():
            print(product.display_str())
            print(Menu.MINOR_DIVIDER)


class CustomerMenu(Menu):

    def __init__(self, store: Store):
        super().__init__({
            "Browse all products": self.browse_all_products,
            "Search by name": self.search_by_name,
            "Place an order": self.place_an_order,
            "Back": self.quit,
        })
        self.store = store

    def browse_all_products(self) -> None:
        print(Menu.MINOR_DIVIDER)
        for product in self.store.get_in_stock_products():
            print(product.display_str())
            print(Menu.MINOR_DIVIDER)

    def search_by_name(self) -> None:
        search: str = Menu.get_str("Search: ")
        results: list[Product] = self.store.search_product(search)
        if len(results) == 0:
            print("No search results found")
            return
        print(Menu.MINOR_DIVIDER)
        for product in results:
            print(product.display_str())
            print(Menu.MINOR_DIVIDER)

    def place_an_order(self) -> None:
        product_id: str = Menu.get_str("Product ID: ", test=lambda text: self.store.has_product(text))
        quantity: int = Menu.get_positive_int("Quality: ")
        product: Product = self.store.get_product(product_id)

        try:
            if product.buy(quantity):
                price: float = product.get_cost(quantity)
                print(f"Bought {product.get_name()} x{quantity} for {price}")
        except ValueError as e:
            print(e.args[0])
        except Expired as e:
            print(e.args[0])



class AddProductMenu(Menu):

    def __init__(self, store: Store):
        super().__init__({
            str(ProductType.PHYSICAL): lambda : self.add_product(ProductType.PHYSICAL),
            str(ProductType.DIGITAL): lambda : self.add_product(ProductType.DIGITAL),
            str(ProductType.PERISHABLE): lambda : self.add_product(ProductType.PERISHABLE),
        })
        self.store = store

    def add_product(self, type: ProductType):

        name: str = input("Name: ")
        price: float = Menu.get_currency("Price: ")
        quantity: int = Menu.get_positive_int("Stock quantity: ")

        new_product: Product

        match type:
            case ProductType.PHYSICAL:
                weight_kg: float = Menu.get_positive_float("Weight (kg): ")
                new_product = self.store.create_product(type, name, price, quantity, weight_kg=weight_kg)
            case ProductType.DIGITAL:
                file_size_mb: float = Menu.get_positive_float("File Size (MB): ")
                download_url: str = Menu.get_str("Download URL: ")
                new_product = self.store.create_product(type, name, price, quantity, file_size_mb=file_size_mb, download_url=download_url)
            case ProductType.PERISHABLE:
                expiration_date: date = Menu.get_date("Expiration Date (YYYY-MM-DD): ")
                new_product = self.store.create_product(type, name, price, quantity, expiration_date=expiration_date)

        print("")
        print("Product Added.")
        print(new_product.display_str())

if __name__ == "__main__":
    store = Store()
    StoreMenu(store).start()
