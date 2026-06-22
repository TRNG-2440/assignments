from abc import ABC, abstractmethod
from datetime import date
import random
import string


class ProductNotFoundError(Exception):
    pass

class OutOfStockError(Exception):
    pass

class ExpiredProductError(Exception):
    pass

class InvalidQuantityError(Exception):
    pass


class Product(ABC):

    _id_counter = 40

    def __init__(self, name: str, price: float, stock: int):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        Product._id_counter += 1
        self._product_id = f"PRD-{Product._id_counter:04d}"
        self._name = name
        self._price = price
        self._stock = stock

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @property
    def stock(self) -> int:
        return self._stock

    def deduct_stock(self, qty: int) -> None:
        if qty <= 0:
            raise InvalidQuantityError("Quantity must be a positive integer.")
        if qty > self._stock:
            raise OutOfStockError(
                f"Only {self._stock} unit(s) of '{self._name}' are available."
            )
        self._stock -= qty

    def restock(self, qty: int) -> None:
        if qty <= 0:
            raise InvalidQuantityError("Restock quantity must be a positive integer.")
        self._stock += qty

    @abstractmethod
    def shipping_cost(self, qty: int) -> float:
        pass

    @abstractmethod
    def total_price(self, qty: int) -> float:
        pass

    @abstractmethod
    def display_details(self) -> str:
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self._product_id} name={self._name!r}>"


class PhysicalProduct(Product):

    SHIPPING_RATE = 2.50

    def __init__(self, name: str, price: float, stock: int, weight_kg: float):
        super().__init__(name, price, stock)
        if weight_kg <= 0:
            raise ValueError("Weight must be greater than zero.")
        self._weight_kg = weight_kg

    @property
    def weight_kg(self) -> float:
        return self._weight_kg

    def shipping_cost(self, qty: int = 1) -> float:
        return round(self._weight_kg * self.SHIPPING_RATE * qty, 2)

    def total_price(self, qty: int) -> float:
        return round(self._price * qty + self.shipping_cost(qty), 2)

    def display_details(self) -> str:
        return (
            f"  ID: {self._product_id}  |  {self._name}  |  ${self._price:.2f}  |"
            f"  In Stock: {self._stock}  |  Weight: {self._weight_kg} kg  |"
            f"  Shipping: ${self.shipping_cost(1):.2f}/unit"
        )


class DigitalProduct(Product):

    def __init__(self, name: str, price: float, stock: int,
                 file_size_mb: float, download_url: str):
        super().__init__(name, price, stock)
        if file_size_mb <= 0:
            raise ValueError("File size must be greater than zero.")
        self._file_size_mb = file_size_mb
        self._download_url = download_url

    @property
    def file_size_mb(self) -> float:
        return self._file_size_mb

    @property
    def download_url(self) -> str:
        return self._download_url

    def shipping_cost(self, qty: int = 1) -> float:
        return 0.0

    def total_price(self, qty: int) -> float:
        return round(self._price * qty, 2)

    def deduct_stock(self, qty: int) -> None:
        if qty <= 0:
            raise InvalidQuantityError("Quantity must be a positive integer.")

    def display_details(self) -> str:
        return (
            f"  ID: {self._product_id}  |  {self._name}  |  ${self._price:.2f}  |"
            f"  In Stock: Unlimited  |  Size: {self._file_size_mb} MB  |"
            f"  URL: {self._download_url}"
        )


class PerishableProduct(Product):

    FLAT_SHIPPING = 3.99
    FREE_SHIPPING_THRESHOLD = 25.00

    def __init__(self, name: str, price: float, stock: int,
                 expiration_date: date):
        super().__init__(name, price, stock)
        self._expiration_date = expiration_date

    @property
    def expiration_date(self) -> date:
        return self._expiration_date

    def is_expired(self) -> bool:
        return date.today() > self._expiration_date

    def shipping_cost(self, qty: int = 1) -> float:
        subtotal = self._price * qty
        if subtotal > self.FREE_SHIPPING_THRESHOLD:
            return 0.0
        return self.FLAT_SHIPPING

    def total_price(self, qty: int) -> float:
        subtotal = self._price * qty
        return round(subtotal + self.shipping_cost(qty), 2)

    def display_details(self) -> str:
        status = "  ⚠ EXPIRED" if self.is_expired() else ""
        return (
            f"  ID: {self._product_id}  |  {self._name}  |  ${self._price:.2f}  |"
            f"  In Stock: {self._stock}  |  Expires: {self._expiration_date}{status}"
        )


class Store:

    def __init__(self, store_name: str = "PyStore"):
        self._name = store_name
        self._inventory: dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        self._inventory[product.product_id] = product

    def remove_product(self, product_id: str) -> None:
        if product_id not in self._inventory:
            raise ProductNotFoundError(f"No product with ID '{product_id}' found.")
        del self._inventory[product_id]

    def restock_product(self, product_id: str, qty: int) -> None:
        if product_id not in self._inventory:
            raise ProductNotFoundError(f"No product with ID '{product_id}' found.")
        self._inventory[product_id].restock(qty)

    def search_by_name(self, query: str) -> list[Product]:
        q = query.strip().lower()
        return [p for p in self._inventory.values() if q in p.name.lower()]

    def list_in_stock(self) -> list[Product]:
        results = []
        for p in self._inventory.values():
            if isinstance(p, DigitalProduct):
                results.append(p)
            elif p.stock > 0:
                results.append(p)
        return results

    def place_order(self, product_id: str, qty: int) -> dict:
        if product_id not in self._inventory:
            raise ProductNotFoundError(f"No product with ID '{product_id}' found.")

        product = self._inventory[product_id]

        if isinstance(product, PerishableProduct) and product.is_expired():
            raise ExpiredProductError(
                f"{product.name} has expired and cannot be ordered."
            )

        product.deduct_stock(qty)

        subtotal = product.price * qty
        shipping = product.shipping_cost(qty)
        total = product.total_price(qty)

        return {
            "product": product,
            "qty": qty,
            "unit_price": product.price,
            "subtotal": subtotal,
            "shipping": shipping,
            "total": total,
            "remaining_stock": product.stock if not isinstance(product, DigitalProduct) else "Unlimited",
        }


def divider(char: str = "-", width: int = 30) -> None:
    print(char * width)

def header(title: str, width: int = 30) -> None:
    print("=" * width)
    print(f"   {title}")
    print("=" * width)

def print_order_summary(summary: dict) -> None:
    p = summary["product"]
    shipping_label = ""

    if isinstance(p, PerishableProduct):
        if summary["shipping"] == 0.0:
            shipping_label = "(free over $25)"
        else:
            shipping_label = "(flat-rate)"
    elif isinstance(p, PhysicalProduct):
        shipping_label = "(weight-based)"

    print()
    header("Order Summary")
    print(f"  {p.name} x{summary['qty']}")
    print(f"  Unit Price : ${summary['unit_price']:.2f}")
    print(f"  Subtotal   : ${summary['subtotal']:.2f}")
    print(f"  Shipping   : ${summary['shipping']:.2f}  {shipping_label}".rstrip())
    print(f"  {'-' * 21}")
    print(f"  Total      : ${summary['total']:.2f}")
    print("=" * 30)
    print(f"Order placed! Remaining stock: {summary['remaining_stock']}")

def prompt_int(prompt: str) -> int | None:
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        print("  Invalid input — please enter a whole number.")
        return None

def prompt_float(prompt: str) -> float | None:
    raw = input(prompt).strip()
    try:
        return float(raw)
    except ValueError:
        print("  Invalid input — please enter a number.")
        return None

def prompt_date(prompt: str) -> date | None:
    raw = input(prompt).strip()
    try:
        return date.fromisoformat(raw)
    except ValueError:
        print("  Invalid date — use YYYY-MM-DD format.")
        return None


def cli_add_product(store: Store) -> None:
    print("\nProduct type:")
    print("  [1] Physical")
    print("  [2] Digital")
    print("  [3] Perishable")
    choice = input("\n> ").strip()

    if choice not in ("1", "2", "3"):
        print("  Invalid choice.")
        return

    name = input("Name: ").strip()
    if not name:
        print("  Name cannot be empty.")
        return

    price = prompt_float("Price: ")
    if price is None or price < 0:
        print("  Price must be a non-negative number.")
        return

    if choice == "2":
        stock_default = 1
    else:
        stock = prompt_int("Stock quantity: ")
        if stock is None or stock < 0:
            print("  Stock must be a non-negative integer.")
            return

    try:
        if choice == "1":
            weight = prompt_float("Weight (kg): ")
            if weight is None or weight <= 0:
                print("  Weight must be positive.")
                return
            product = PhysicalProduct(name, price, stock, weight)
            label = "Physical"

        elif choice == "2":
            size = prompt_float("File size (MB): ")
            if size is None or size <= 0:
                print("  File size must be positive.")
                return
            url = input("Download URL: ").strip()
            if not url:
                print("  URL cannot be empty.")
                return
            product = DigitalProduct(name, price, stock_default, size, url)
            label = "Digital"

        else:
            exp = prompt_date("Expiration date (YYYY-MM-DD): ")
            if exp is None:
                return
            product = PerishableProduct(name, price, stock, exp)
            label = "Perishable"

        store.add_product(product)
        print(f"\n{label} product added.")
        print(product.display_details())

    except ValueError as e:
        print(f"  Error: {e}")


def manager_menu(store: Store) -> None:
    while True:
        print("\n--- Manager Menu ---")
        print("  [1] Add product")
        print("  [2] Remove product")
        print("  [3] Restock product")
        print("  [4] List all inventory")
        print("  [5] Back")

        choice = input("\n> ").strip()

        if choice == "1":
            cli_add_product(store)

        elif choice == "2":
            pid = input("Product ID to remove: ").strip().upper()
            try:
                store.remove_product(pid)
                print(f"  Product {pid} removed.")
            except ProductNotFoundError as e:
                print(f"  Error: {e}")

        elif choice == "3":
            pid = input("Product ID to restock: ").strip().upper()
            qty = prompt_int("Quantity to add: ")
            if qty is None:
                continue
            try:
                store.restock_product(pid, qty)
                print(f"  Restocked {pid}.  New stock: {store._inventory[pid].stock}")
            except (ProductNotFoundError, InvalidQuantityError) as e:
                print(f"  Error: {e}")

        elif choice == "4":
            products = list(store._inventory.values())
            if not products:
                print("  Inventory is empty.")
            else:
                print()
                divider()
                for p in products:
                    print(p.display_details())
                divider()

        elif choice == "5":
            break

        else:
            print("  Invalid option.")

        divider()


def customer_menu(store: Store) -> None:
    while True:
        print("\n--- Customer Menu ---")
        print("  [1] Browse all products")
        print("  [2] Search by name")
        print("  [3] Place an order")
        print("  [4] Back")

        choice = input("\n> ").strip()

        if choice == "1":
            products = store.list_in_stock()
            if not products:
                print("  No products currently in stock.")
            else:
                print()
                divider()
                for p in products:
                    print(p.display_details())
                divider()

        elif choice == "2":
            query = input("Search: ").strip()
            results = store.search_by_name(query)
            if not results:
                print("  No products matched your search.")
            else:
                print("\nResults:")
                for p in results:
                    print(p.display_details())

        elif choice == "3":
            pid = input("Product ID: ").strip().upper()
            qty = prompt_int("Quantity: ")
            if qty is None:
                continue
            try:
                summary = store.place_order(pid, qty)
                print_order_summary(summary)
            except (ProductNotFoundError, OutOfStockError,
                    ExpiredProductError, InvalidQuantityError) as e:
                print(f"\n  Error: {e}")

        elif choice == "4":
            break

        else:
            print("  Invalid option.")

        divider()


def seed_store(store: Store) -> None:
    store.add_product(PhysicalProduct("Mechanical Keyboard", 89.99, 15, 1.2))
    store.add_product(PhysicalProduct("Ergonomic Mouse", 49.99, 20, 0.25))
    store.add_product(DigitalProduct("Python Pro Course", 29.99, 1, 2048.0,
                                     "https://pystore.example.com/dl/python-pro"))
    store.add_product(PerishableProduct("Organic Strawberries", 4.99, 30,
                                        date(2026, 12, 31)))
    store.add_product(PerishableProduct("Greek Yogurt", 3.49, 50,
                                        date(2025, 1, 1)))


def main() -> None:
    store = Store("PyStore")
    seed_store(store)

    while True:
        print()
        header("PyStore Inventory System")
        print()
        print("  [1] Manager Menu")
        print("  [2] Customer Menu")
        print("  [3] Quit")

        choice = input("\n> ").strip()

        if choice == "1":
            manager_menu(store)
        elif choice == "2":
            customer_menu(store)
        elif choice == "3":
            print("\nGoodbye!\n")
            break
        else:
            print("  Invalid option — choose 1, 2, or 3.")


if __name__ == "__main__":
    main()