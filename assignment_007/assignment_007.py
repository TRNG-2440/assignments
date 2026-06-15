# dependencies
from datetime import date, datetime

# exception classes for store/order operations
class ProductNotFoundError(Exception):
    pass

class OutOfStockError(Exception):
    pass

class InsufficientStockError(Exception):
    pass

class ExpiredProductError(Exception):
    pass

# base Product class
class Product:
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int) -> None:
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity

    def subtotal(self, quantity: int) -> float:
        return self.price * quantity

    def shipping_cost(self, quantity: int) -> float:
        return 0.0

    def shipping_label(self, quantity: int) -> str:
        return ""

    def total_price(self, quantity: int) -> float:
        return self.subtotal(quantity) + self.shipping_cost(quantity)

    def details(self) -> None:
        print(f"[{self.product_id}]  {self.name}  |  ${self.price:.2f}  |  In Stock: {self.stock_quantity}")

# physical subclass
class PhysicalProduct(Product):
    SHIPPING_RATE = 1.50  # dollars per kg per item

    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, weight: float) -> None:
        super().__init__(product_id, name, price, stock_quantity)
        self.weight = weight

    def shipping_cost(self, quantity: int) -> float:
        return self.weight * quantity * self.SHIPPING_RATE

    def shipping_label(self, quantity: int) -> str:
        return "(weight-based)"

    def details(self) -> None:
        print(f"[{self.product_id}]  {self.name}  |  ${self.price:.2f}  |  In Stock: {self.stock_quantity}  |  Weight: {self.weight}kg")

# digital subclass
class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, file_size: float, download_url: str) -> None:
        # digital products are not limited by stock
        super().__init__(product_id, name, price, stock_quantity=0)
        self.file_size = file_size
        self.download_url = download_url

    def shipping_cost(self, quantity: int) -> float:
        return 0.0

    def details(self) -> None:
        print(f"[{self.product_id}]  {self.name}  |  ${self.price:.2f}  |  Size: {self.file_size}MB  |  URL: {self.download_url}")

# perishable subclass
class PerishableProduct(Product):
    FLAT_SHIPPING = 3.99
    FREE_SHIPPING_THRESHOLD = 25.00

    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, expiration_date: date) -> None:
        super().__init__(product_id, name, price, stock_quantity)
        self.expiration_date = expiration_date

    def is_expired(self) -> bool:
        return self.expiration_date < date.today()

    def shipping_cost(self, quantity: int) -> float:
        if self.subtotal(quantity) > self.FREE_SHIPPING_THRESHOLD:
            return 0.0
        return self.FLAT_SHIPPING

    def shipping_label(self, quantity: int) -> str:
        if self.subtotal(quantity) > self.FREE_SHIPPING_THRESHOLD:
            return "(free over $25)"
        return "(flat-rate)"

    def details(self) -> None:
        print(f"[{self.product_id}]  {self.name}  |  ${self.price:.2f}  |  In Stock: {self.stock_quantity}  |  Expires: {self.expiration_date.isoformat()}")

# Store class
class Store:
    def __init__(self) -> None:
        self.products = []
        # unique id counter, increasing by 1
        self.next_id = 1

    def generate_id(self) -> str:
        product_id = f"PRD-{self.next_id:04d}"
        self.next_id += 1
        return product_id

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def find_product(self, product_id: str):
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    def remove_product(self, product_id: str) -> Product:
        product = self.find_product(product_id)
        if product is None:
            raise ProductNotFoundError(f"No product with ID {product_id}.")
        self.products.remove(product)
        return product

    def restock_product(self, product_id: str, amount: int) -> Product:
        product = self.find_product(product_id)
        if product is None:
            raise ProductNotFoundError(f"No product with ID {product_id}.")
        if amount <= 0:
            raise ValueError("Restock amount must be positive.")
        product.stock_quantity += amount
        return product

    def search_by_name(self, query: str):
        query = query.lower()
        return [product for product in self.products if query in product.name.lower()]

    def list_in_stock(self):
        in_stock = []
        for product in self.products:
            # digital products are always available
            if isinstance(product, DigitalProduct) or product.stock_quantity > 0:
                in_stock.append(product)
        return in_stock

    def place_order(self, product_id: str, quantity: int) -> dict:
        product = self.find_product(product_id)
        if product is None:
            raise ProductNotFoundError(f"No product with ID {product_id}.")
        if quantity <= 0:
            raise ValueError("Order quantity must be positive.")

        if isinstance(product, PerishableProduct) and product.is_expired():
            raise ExpiredProductError(f"{product.name} has expired and cannot be ordered.")

        # digital products are not limited by stock
        if not isinstance(product, DigitalProduct):
            if product.stock_quantity <= 0:
                raise OutOfStockError(f"{product.name} is out of stock.")
            if quantity > product.stock_quantity:
                raise InsufficientStockError(
                    f"Only {product.stock_quantity} of {product.name} available."
                )

        subtotal = product.subtotal(quantity)
        shipping = product.shipping_cost(quantity)
        total = subtotal + shipping

        # deduct stock for everything except digital products
        if not isinstance(product, DigitalProduct):
            product.stock_quantity -= quantity

        return {
            "name": product.name,
            "quantity": quantity,
            "unit_price": product.price,
            "subtotal": subtotal,
            "shipping": shipping,
            "shipping_label": product.shipping_label(quantity),
            "total": total,
            "remaining_stock": None if isinstance(product, DigitalProduct) else product.stock_quantity,
        }

# helper input functions for the CLI
def prompt_int(message: str) -> int:
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def prompt_float(message: str) -> float:
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Invalid input. Please enter a number.")

def prompt_menu(message: str, low: int, high: int) -> int:
    while True:
        choice = prompt_int(message)
        if low <= choice <= high:
            return choice
        print("Invalid option. Try again.")

def prompt_date(message: str) -> date:
    while True:
        value = input(message)
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date. Please use the format YYYY-MM-DD.")

# manager menu
def manager_menu(store: Store) -> None:
    while True:
        print("\n--- Manager Menu ---")
        print("[1] Add product")
        print("[2] Remove product")
        print("[3] Restock product")
        print("[4] List all inventory")
        print("[5] Back")

        option = prompt_menu("> ", 1, 5)

        match option:
            case 1:  # add product
                print("\nProduct type:")
                print("[1] Physical")
                print("[2] Digital")
                print("[3] Perishable")
                product_type = prompt_menu("> ", 1, 3)

                name = input("Name: ")
                price = prompt_float("Price: ")

                match product_type:
                    case 1:  # physical
                        stock = prompt_int("Stock quantity: ")
                        weight = prompt_float("Weight (kg): ")
                        product = PhysicalProduct(store.generate_id(), name, price, stock, weight)
                        store.add_product(product)
                        print("\nPhysical product added.")
                        product.details()

                    case 2:  # digital
                        file_size = prompt_float("File size (MB): ")
                        download_url = input("Download URL: ")
                        product = DigitalProduct(store.generate_id(), name, price, file_size, download_url)
                        store.add_product(product)
                        print("\nDigital product added.")
                        product.details()

                    case 3:  # perishable
                        stock = prompt_int("Stock quantity: ")
                        expiration_date = prompt_date("Expiration date (YYYY-MM-DD): ")
                        product = PerishableProduct(store.generate_id(), name, price, stock, expiration_date)
                        store.add_product(product)
                        print("\nPerishable product added.")
                        product.details()

            case 2:  # remove product
                product_id = input("Product ID to remove: ")
                try:
                    removed = store.remove_product(product_id)
                    print(f"Removed {removed.name} ({removed.product_id}).")
                except ProductNotFoundError as e:
                    print(f"Error: {e}")

            case 3:  # restock product
                product_id = input("Product ID to restock: ")
                amount = prompt_int("Amount to add: ")
                try:
                    product = store.restock_product(product_id, amount)
                    print(f"Restocked {product.name}. New stock: {product.stock_quantity}")
                except (ProductNotFoundError, ValueError) as e:
                    print(f"Error: {e}")

            case 4:  # list all inventory
                if not store.products:
                    print("No products in inventory.")
                else:
                    print("\n--- Full Inventory ---")
                    for product in store.products:
                        product.details()

            case 5:  # back
                break

# customer menu
def customer_menu(store: Store) -> None:
    while True:
        print("\n--- Customer Menu ---")
        print("[1] Browse all products")
        print("[2] Search by name")
        print("[3] Place an order")
        print("[4] Back")

        option = prompt_menu("> ", 1, 4)

        match option:
            case 1:  # browse all in-stock products
                in_stock = store.list_in_stock()
                if not in_stock:
                    print("No products available.")
                else:
                    print("\nAvailable products:")
                    for product in in_stock:
                        product.details()

            case 2:  # search by name
                query = input("Search: ")
                results = store.search_by_name(query)
                if not results:
                    print("No matching products found.")
                else:
                    print("\nResults:")
                    for product in results:
                        product.details()

            case 3:  # place an order
                product_id = input("Product ID: ")
                quantity = prompt_int("Quantity: ")
                try:
                    summary = store.place_order(product_id, quantity)
                except (ProductNotFoundError, OutOfStockError, InsufficientStockError,
                        ExpiredProductError, ValueError) as e:
                    print(f"Error: {e}")
                    continue

                print("\n" + "=" * 30)
                print("         Order Summary")
                print("=" * 30)
                print(f"  {summary['name']} x{summary['quantity']}")
                print(f"  Unit Price : ${summary['unit_price']:.2f}")
                print(f"  Subtotal   : ${summary['subtotal']:.2f}")
                label = summary["shipping_label"]
                if label:
                    print(f"  Shipping   : ${summary['shipping']:.2f}  {label}")
                else:
                    print(f"  Shipping   : ${summary['shipping']:.2f}")
                print("  ---------------------")
                print(f"  Total      : ${summary['total']:.2f}")
                print("=" * 30)
                if summary["remaining_stock"] is None:
                    print("Order placed! (digital download)")
                else:
                    print(f"Order placed! Remaining stock: {summary['remaining_stock']}")

            case 4:  # back
                break

# main menu loop
store = Store()

while True:
    print("\n" + "=" * 30)
    print("   PyStore Inventory System")
    print("=" * 30, "\n")
    print("[1] Manager Menu")
    print("[2] Customer Menu")
    print("[3] Quit")

    option = prompt_menu("> ", 1, 3)

    match option:
        case 1:
            manager_menu(store)
        case 2:
            customer_menu(store)
        case 3:
            print("Goodbye!")
            break
