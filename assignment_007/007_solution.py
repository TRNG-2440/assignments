from abc import ABC, abstractmethod
from datetime import date, datetime


class InventoryError(Exception):
    pass


class Product(ABC):
    next_id = 1

    def __init__(self, name, price, stock_quantity):
        self.product_id = self.generate_id()
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity

    @classmethod
    def generate_id(cls):
        product_id = f"PRD-{cls.next_id:04d}"
        cls.next_id += 1
        return product_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        value = float(value)
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value

    @property
    def stock_quantity(self):
        return self._stock_quantity

    @stock_quantity.setter
    def stock_quantity(self, value):
        value = int(value)
        if value < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self._stock_quantity = value

    def calculate_subtotal(self, quantity):
        return self.price * quantity

    def calculate_total_price(self, quantity):
        return self.calculate_subtotal(quantity) + self.calculate_shipping(quantity)

    def is_in_stock(self):
        return self.stock_quantity > 0

    def has_enough_stock(self, quantity):
        return self.stock_quantity >= quantity

    def reduce_stock(self, quantity):
        self.stock_quantity -= quantity

    @abstractmethod
    def calculate_shipping(self, quantity):
        pass

    @abstractmethod
    def display_details(self):
        pass


class PhysicalProduct(Product):
    SHIPPING_RATE_PER_KG = 2.50

    def __init__(self, name, price, stock_quantity, weight):
        super().__init__(name, price, stock_quantity)
        self.weight = weight

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Weight must be greater than 0.")
        self._weight = value

    def calculate_shipping(self, quantity):
        return self.weight * quantity * self.SHIPPING_RATE_PER_KG

    def display_details(self):
        return (
            f"[{self.product_id}] {self.name} | Physical | "
            f"${self.price:.2f} | Stock: {self.stock_quantity} | "
            f"Weight: {self.weight:.2f} kg"
        )


class DigitalProduct(Product):
    def __init__(self, name, price, file_size, download_url):
        super().__init__(name, price, 0)
        self.file_size = file_size
        self.download_url = download_url

    @property
    def file_size(self):
        return self._file_size

    @file_size.setter
    def file_size(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("File size must be greater than 0.")
        self._file_size = value

    @property
    def download_url(self):
        return self._download_url

    @download_url.setter
    def download_url(self, value):
        if not value.strip():
            raise ValueError("Download URL cannot be empty.")
        self._download_url = value.strip()

    def calculate_shipping(self, quantity):
        return 0

    def is_in_stock(self):
        return True

    def has_enough_stock(self, quantity):
        return True

    def reduce_stock(self, quantity):
        pass

    def display_details(self):
        return (
            f"[{self.product_id}] {self.name} | Digital | "
            f"${self.price:.2f} | Stock: Unlimited | "
            f"File Size: {self.file_size:.2f} MB | URL: {self.download_url}"
        )


class PerishableProduct(Product):
    FLAT_SHIPPING_RATE = 3.99
    FREE_SHIPPING_MINIMUM = 25.00

    def __init__(self, name, price, stock_quantity, expiration_date):
        super().__init__(name, price, stock_quantity)
        self.expiration_date = expiration_date

    @property
    def expiration_date(self):
        return self._expiration_date

    @expiration_date.setter
    def expiration_date(self, value):
        try:
            self._expiration_date = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Expiration date must be in YYYY-MM-DD format.")

    def is_expired(self):
        return date.today() > self.expiration_date

    def calculate_shipping(self, quantity):
        subtotal = self.calculate_subtotal(quantity)

        if subtotal > self.FREE_SHIPPING_MINIMUM:
            return 0

        return self.FLAT_SHIPPING_RATE

    def display_details(self):
        return (
            f"[{self.product_id}] {self.name} | Perishable | "
            f"${self.price:.2f} | Stock: {self.stock_quantity} | "
            f"Expires: {self.expiration_date}"
        )


class Store:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        self.products[product.product_id] = product

    def remove_product(self, product_id):
        product = self.find_product(product_id)
        del self.products[product.product_id]

    def restock_product(self, product_id, quantity):
        product = self.find_product(product_id)

        if isinstance(product, DigitalProduct):
            raise InventoryError("Digital products do not need restocking.")

        if quantity <= 0:
            raise InventoryError("Quantity must be greater than 0.")

        product.stock_quantity += quantity

    def find_product(self, product_id):
        product_id = product_id.strip().upper()

        if product_id not in self.products:
            raise InventoryError("Product ID does not exist.")

        return self.products[product_id]

    def search_by_name(self, search_term):
        search_term = search_term.lower().strip()
        results = []

        for product in self.products.values():
            if search_term in product.name.lower():
                results.append(product)

        return results

    def list_all_products(self):
        return list(self.products.values())

    def list_in_stock_products(self):
        return [product for product in self.products.values() if product.is_in_stock()]

    def place_order(self, product_id, quantity):
        product = self.find_product(product_id)

        if quantity <= 0:
            raise InventoryError("Quantity must be greater than 0.")

        if isinstance(product, PerishableProduct) and product.is_expired():
            raise InventoryError(f"{product.name} has expired and cannot be ordered.")

        if not product.is_in_stock():
            raise InventoryError(f"{product.name} is out of stock.")

        if not product.has_enough_stock(quantity):
            raise InventoryError("Quantity exceeds available stock.")

        subtotal = product.calculate_subtotal(quantity)
        shipping = product.calculate_shipping(quantity)
        total = product.calculate_total_price(quantity)

        product.reduce_stock(quantity)

        return subtotal, shipping, total, product


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Error: Please enter a whole number.")


def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Error: Please enter a number.")


def get_text(prompt):
    while True:
        text = input(prompt).strip()

        if text:
            return text

        print("Error: Input cannot be empty.")


def print_products(products):
    if not products:
        print("No products found.")
    else:
        for product in products:
            print(product.display_details())


def print_order_summary(product, quantity, subtotal, shipping, total):
    print()
    print("==============================")
    print("         Order Summary")
    print("==============================")
    print(f"  {product.name} x{quantity}")
    print(f"  Unit Price : ${product.price:.2f}")
    print(f"  Subtotal   : ${subtotal:.2f}")
    print(f"  Shipping   : ${shipping:.2f}")
    print("  ---------------------")
    print(f"  Total      : ${total:.2f}")
    print("==============================")

    if isinstance(product, DigitalProduct):
        print("Order placed! Digital product stock is unlimited.")
    else:
        print(f"Order placed! Remaining stock: {product.stock_quantity}")


def add_product_menu(store):
    print()
    print("Product type:")
    print("[1] Physical")
    print("[2] Digital")
    print("[3] Perishable")

    product_type = input("> ").strip()

    try:
        name = get_text("Name: ")
        price = get_float("Price: ")

        if product_type == "1":
            stock_quantity = get_int("Stock quantity: ")
            weight = get_float("Weight: ")

            product = PhysicalProduct(name, price, stock_quantity, weight)
            store.add_product(product)
            print("Physical product added.")
            print(product.display_details())

        elif product_type == "2":
            file_size = get_float("File size: ")
            download_url = get_text("Download URL: ")

            product = DigitalProduct(name, price, file_size, download_url)
            store.add_product(product)
            print("Digital product added.")
            print(product.display_details())

        elif product_type == "3":
            stock_quantity = get_int("Stock quantity: ")
            expiration_date = get_text("Expiration date (YYYY-MM-DD): ")

            product = PerishableProduct(name, price, stock_quantity, expiration_date)
            store.add_product(product)
            print("Perishable product added.")
            print(product.display_details())

        else:
            print("Invalid product type.")

    except ValueError as error:
        print(f"Error: {error}")


def manager_menu(store):
    while True:
        print()
        print("--- Manager Menu ---")
        print("[1] Add product")
        print("[2] Remove product")
        print("[3] Restock product")
        print("[4] List all inventory")
        print("[5] Back")

        choice = input("> ").strip()

        if choice == "1":
            add_product_menu(store)

        elif choice == "2":
            product_id = get_text("Product ID: ")

            try:
                store.remove_product(product_id)
                print("Product removed.")
            except InventoryError as error:
                print(f"Error: {error}")

        elif choice == "3":
            product_id = get_text("Product ID: ")
            quantity = get_int("Quantity to add: ")

            try:
                store.restock_product(product_id, quantity)
                print("Product restocked.")
            except InventoryError as error:
                print(f"Error: {error}")

        elif choice == "4":
            print()
            print("--- Inventory ---")
            print_products(store.list_all_products())

        elif choice == "5":
            break

        else:
            print("Invalid option.")


def customer_menu(store):
    while True:
        print()
        print("--- Customer Menu ---")
        print("[1] Browse all products")
        print("[2] Search by name")
        print("[3] Place an order")
        print("[4] Back")

        choice = input("> ").strip()

        if choice == "1":
            print()
            print("--- In-Stock Products ---")
            print_products(store.list_in_stock_products())

        elif choice == "2":
            search_term = get_text("Search: ")
            results = store.search_by_name(search_term)

            print()
            print("--- Search Results ---")
            print_products(results)

        elif choice == "3":
            product_id = get_text("Product ID: ")
            quantity = get_int("Quantity: ")

            try:
                subtotal, shipping, total, product = store.place_order(product_id, quantity)
                print_order_summary(product, quantity, subtotal, shipping, total)
            except InventoryError as error:
                print(f"Error: {error}")

        elif choice == "4":
            break

        else:
            print("Invalid option.")


def main():
    store = Store()

    while True:
        print()
        print("==============================")
        print("   PyStore Inventory System")
        print("==============================")
        print("[1] Manager Menu")
        print("[2] Customer Menu")
        print("[3] Quit")

        choice = input("> ").strip()

        if choice == "1":
            manager_menu(store)

        elif choice == "2":
            customer_menu(store)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()