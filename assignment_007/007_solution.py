from abc import ABC, abstractmethod
from datetime import date, datetime
import json
import os


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

    @classmethod
    def update_next_id(cls, product_id):
        number = int(product_id.split("-")[1])

        if number >= cls.next_id:
            cls.next_id = number + 1

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

    def apply_discount(self, percent):
        if percent <= 0 or percent > 100:
            raise InventoryError("Discount percent must be between 1 and 100.")

        self.price = self.price * (1 - percent / 100)

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

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock_quantity": self.stock_quantity
        }

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

    def to_dict(self):
        data = super().to_dict()
        data["weight"] = self.weight
        return data


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

    def to_dict(self):
        data = super().to_dict()
        data["file_size"] = self.file_size
        data["download_url"] = self.download_url
        return data


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

    def to_dict(self):
        data = super().to_dict()
        data["expiration_date"] = str(self.expiration_date)
        return data


class Store:
    LOW_STOCK_LIMIT = 5

    def __init__(self):
        self.products = {}
        self.order_history = []

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

        order = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "product_name": product.name,
            "quantity": quantity,
            "total": total
        }

        self.order_history.append(order)

        return subtotal, shipping, total, product

    def apply_sale_by_type(self, product_type, percent):
        count = 0

        for product in self.products.values():
            if product_type == "physical" and isinstance(product, PhysicalProduct):
                product.apply_discount(percent)
                count += 1
            elif product_type == "digital" and isinstance(product, DigitalProduct):
                product.apply_discount(percent)
                count += 1
            elif product_type == "perishable" and isinstance(product, PerishableProduct):
                product.apply_discount(percent)
                count += 1

        return count

    def remove_expired_products(self):
        removed = []

        for product_id in list(self.products.keys()):
            product = self.products[product_id]

            if isinstance(product, PerishableProduct) and product.is_expired():
                removed.append(product)
                del self.products[product_id]

        return removed

    def get_low_stock_products(self):
        low_stock = []

        for product in self.products.values():
            if not isinstance(product, DigitalProduct):
                if product.stock_quantity < self.LOW_STOCK_LIMIT:
                    low_stock.append(product)

        return low_stock

    def save_inventory(self, filename):
        data = []

        for product in self.products.values():
            data.append(product.to_dict())

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_inventory(self, filename):
        if not os.path.exists(filename):
            return

        with open(filename, "r") as file:
            data = json.load(file)

        for item in data:
            product_type = item["type"]

            if product_type == "PhysicalProduct":
                product = PhysicalProduct(
                    item["name"],
                    item["price"],
                    item["stock_quantity"],
                    item["weight"]
                )
            elif product_type == "DigitalProduct":
                product = DigitalProduct(
                    item["name"],
                    item["price"],
                    item["file_size"],
                    item["download_url"]
                )
            elif product_type == "PerishableProduct":
                product = PerishableProduct(
                    item["name"],
                    item["price"],
                    item["stock_quantity"],
                    item["expiration_date"]
                )
            else:
                continue

            product.product_id = item["product_id"]
            Product.update_next_id(product.product_id)
            self.products[product.product_id] = product


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


def print_low_stock_alerts(store):
    low_stock_products = store.get_low_stock_products()

    if low_stock_products:
        print()
        print("Low Stock Alert:")

        for product in low_stock_products:
            print(f"{product.name} has only {product.stock_quantity} left.")


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


def sale_menu(store):
    print()
    print("Apply sale to product type:")
    print("[1] Physical")
    print("[2] Digital")
    print("[3] Perishable")

    choice = input("> ").strip()
    percent = get_float("Discount percent: ")

    try:
        if choice == "1":
            count = store.apply_sale_by_type("physical", percent)
        elif choice == "2":
            count = store.apply_sale_by_type("digital", percent)
        elif choice == "3":
            count = store.apply_sale_by_type("perishable", percent)
        else:
            print("Invalid product type.")
            return

        print(f"Sale applied to {count} product(s).")

    except InventoryError as error:
        print(f"Error: {error}")


def expiration_sweep_menu(store):
    removed_products = store.remove_expired_products()

    print()
    print("--- Expiration Sweep Report ---")

    if not removed_products:
        print("No expired products were removed.")
    else:
        for product in removed_products:
            print(f"Removed: {product.name} | Expired: {product.expiration_date}")


def manager_menu(store):
    while True:
        print()
        print("--- Manager Menu ---")
        print("[1] Add product")
        print("[2] Remove product")
        print("[3] Restock product")
        print("[4] List all inventory")
        print("[5] Apply sale by product type")
        print("[6] Remove expired perishable products")
        print("[7] Back")

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
                print_low_stock_alerts(store)
            except InventoryError as error:
                print(f"Error: {error}")

        elif choice == "4":
            print()
            print("--- Inventory ---")
            print_products(store.list_all_products())

        elif choice == "5":
            sale_menu(store)

        elif choice == "6":
            expiration_sweep_menu(store)

        elif choice == "7":
            break

        else:
            print("Invalid option.")


def print_order_history(store):
    print()
    print("--- Order History ---")

    if not store.order_history:
        print("No orders have been placed.")
        return

    for order in store.order_history:
        print(
            f"{order['timestamp']} | "
            f"{order['product_name']} x{order['quantity']} | "
            f"Total: ${order['total']:.2f}"
        )


def customer_menu(store):
    while True:
        print()
        print("--- Customer Menu ---")
        print("[1] Browse all products")
        print("[2] Search by name")
        print("[3] Place an order")
        print("[4] View order history")
        print("[5] Back")

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
                print_low_stock_alerts(store)
            except InventoryError as error:
                print(f"Error: {error}")

        elif choice == "4":
            print_order_history(store)

        elif choice == "5":
            break

        else:
            print("Invalid option.")


def main():
    filename = "inventory.json"
    store = Store()
    store.load_inventory(filename)

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
            store.save_inventory(filename)
            print("Inventory saved.")
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()