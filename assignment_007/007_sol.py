#Solution to Assignment 7
#Alex Tran

#Online Store Inventory System




#Import ABCs and abstract methods, and datetime
from abc import ABC, abstractmethod
from datetime import date, datetime



#
class InventoryError(Exception):
    pass


#Create product abc
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
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value

    @property
    def stock_quantity(self):
        return self._stock_quantity

    @stock_quantity.setter
    def stock_quantity(self, value):
        if value < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self._stock_quantity = value

    def calculate_total(self, quantity):
        return self.price * quantity

    def reduce_stock(self, quantity):
        if quantity > self.stock_quantity:
            raise InventoryError("Not enough stock available.")
        self.stock_quantity -= quantity

    @abstractmethod
    def display_details(self):
        pass


#physical product class
class PhysicalProduct(Product):
    SHIPPING_RATE_PER_KG = 2.50

    def __init__(self, name, price, stock_quantity, weight):
        super().__init__(name, price, stock_quantity)
        self.weight = weight

    def calculate_shipping(self, quantity):
        return self.weight * quantity * self.SHIPPING_RATE_PER_KG

    def calculate_total(self, quantity):
        subtotal = self.price * quantity
        shipping = self.calculate_shipping(quantity)
        return subtotal + shipping

    def display_details(self):
        return (
            f"[{self.product_id}] {self.name} | "
            f"${self.price:.2f} | Stock: {self.stock_quantity} | "
            f"Weight: {self.weight} kg"
        )

#digital product class
class DigitalProduct(Product):
    def __init__(self, name, price, file_size, download_url):
        super().__init__(name, price, stock_quantity=999999)
        self.file_size = file_size
        self.download_url = download_url

    def calculate_total(self, quantity):
        return self.price * quantity

    def reduce_stock(self, quantity):
        pass

    def display_details(self):
        return (
            f"[{self.product_id}] {self.name} | "
            f"${self.price:.2f} | Digital Product | "
            f"File Size: {self.file_size} MB | URL: {self.download_url}"
        )

#perishable product class
class PerishableProduct(Product):
    FLAT_SHIPPING_RATE = 3.99
    FREE_SHIPPING_THRESHOLD = 25.00

    def __init__(self, name, price, stock_quantity, expiration_date):
        super().__init__(name, price, stock_quantity)
        self.expiration_date = expiration_date

    def is_expired(self):
        return date.today() > self.expiration_date

    def calculate_shipping(self, quantity):
        subtotal = self.price * quantity

        if subtotal > self.FREE_SHIPPING_THRESHOLD:
            return 0

        return self.FLAT_SHIPPING_RATE

    def calculate_total(self, quantity):
        subtotal = self.price * quantity
        shipping = self.calculate_shipping(quantity)
        return subtotal + shipping

    def display_details(self):
        status = "Expired" if self.is_expired() else "Fresh"
        return (
            f"[{self.product_id}] {self.name} | "
            f"${self.price:.2f} | Stock: {self.stock_quantity} | "
            f"Expires: {self.expiration_date} | {status}"
        )



#Store to allow the user to add, remove, search, and order products

class Store:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        self.products[product.product_id] = product

    def remove_product(self, product_id):
        if product_id not in self.products:
            raise InventoryError("Product ID does not exist.")
        del self.products[product_id]

    def restock_product(self, product_id, quantity):
        if product_id not in self.products:
            raise InventoryError("Product ID does not exist.")

        if quantity <= 0:
            raise InventoryError("Restock quantity must be positive.")

        self.products[product_id].stock_quantity += quantity

    def search_by_name(self, name):
        results = []

        for product in self.products.values():
            if name.lower() in product.name.lower():
                results.append(product)

        return results

    def list_in_stock_products(self):
        return [
            product for product in self.products.values()
            if isinstance(product, DigitalProduct) or product.stock_quantity > 0
        ]

    def place_order(self, product_id, quantity):
        if product_id not in self.products:
            raise InventoryError("Product ID does not exist.")

        if quantity <= 0:
            raise InventoryError("Quantity must be positive.")

        product = self.products[product_id]

        if isinstance(product, PerishableProduct) and product.is_expired():
            raise InventoryError(f"{product.name} has expired and cannot be ordered.")

        if not isinstance(product, DigitalProduct):
            if product.stock_quantity == 0:
                raise InventoryError("Product is out of stock.")

            if quantity > product.stock_quantity:
                raise InventoryError("Requested quantity exceeds available stock.")

        subtotal = product.price * quantity
        shipping = product.calculate_total(quantity) - subtotal
        total = product.calculate_total(quantity)

        product.reduce_stock(quantity)

        return {
            "name": product.name,
            "quantity": quantity,
            "unit_price": product.price,
            "subtotal": subtotal,
            "shipping": shipping,
            "total": total,
            "remaining_stock": product.stock_quantity
        }


#Get float and int values, depending on whether or not we need whole integer values or floating points for prices
def get_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
            else:
                return value
        except ValueError:
            print("Please enter a valid number.")


def get_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
            else:
                return value
        except ValueError:
            print("Please enter a valid whole number.")

#Get date from user in the proper format
def get_date(prompt):
    while True:
        try:
            date_text = input(prompt)
            return datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")

#displays the order for the user
def print_order_summary(summary):
    print("\n==============================")
    print("         Order Summary")
    print("==============================")
    print(f"{summary['name']} x{summary['quantity']}")
    print(f"Unit Price : ${summary['unit_price']:.2f}")
    print(f"Subtotal   : ${summary['subtotal']:.2f}")
    print(f"Shipping   : ${summary['shipping']:.2f}")
    print("---------------------")
    print(f"Total      : ${summary['total']:.2f}")
    print("==============================")
    print(f"Order placed! Remaining stock: {summary['remaining_stock']}")



# menu to display for the user to add product
def add_product_menu(store):
    print("\nProduct type:")
    print("[1] Physical")
    print("[2] Digital")
    print("[3] Perishable")

    choice = input("> ")

    name = input("Name: ")
    price = get_float("Price: ")

    try:
        if choice == "1":
            stock = get_int("Stock quantity: ")
            weight = get_float("Weight in kg: ")
            product = PhysicalProduct(name, price, stock, weight)

        elif choice == "2":
            file_size = get_float("File size in MB: ")
            download_url = input("Download URL: ")
            product = DigitalProduct(name, price, file_size, download_url)

        elif choice == "3":
            stock = get_int("Stock quantity: ")
            expiration_date = get_date("Expiration date (YYYY-MM-DD): ")
            product = PerishableProduct(name, price, stock, expiration_date)

        else:
            print("Invalid product type.")
            return

        store.add_product(product)
        print("\nProduct added.")
        print(product.display_details())

    except ValueError as error:
        print(f"Error: {error}")

#menu to display for the manaager
def manager_menu(store):
    while True:
        print("\n--- Manager Menu ---")
        print("[1] Add product")
        print("[2] Remove product")
        print("[3] Restock product")
        print("[4] List all inventory")
        print("[5] Back")

        choice = input("> ")

        try:
            if choice == "1":
                add_product_menu(store)

            elif choice == "2":
                product_id = input("Product ID: ")
                store.remove_product(product_id)
                print("Product removed.")

            elif choice == "3":
                product_id = input("Product ID: ")
                quantity = get_int("Restock quantity: ")
                store.restock_product(product_id, quantity)
                print("Product restocked.")

            elif choice == "4":
                products = store.list_in_stock_products()

                if not products:
                    print("No products in stock.")
                else:
                    for product in products:
                        print(product.display_details())

            elif choice == "5":
                break

            else:
                print("Invalid choice.")

        except InventoryError as error:
            print(f"Error: {error}")

#menu to display for the customer
def customer_menu(store):
    while True:
        print("\n--- Customer Menu ---")
        print("[1] Browse all products")
        print("[2] Search by name")
        print("[3] Place an order")
        print("[4] Back")

        choice = input("> ")

        try:
            if choice == "1":
                products = store.list_in_stock_products()

                if not products:
                    print("No products available.")
                else:
                    for product in products:
                        print(product.display_details())

            elif choice == "2":
                search_term = input("Search: ")
                results = store.search_by_name(search_term)

                if not results:
                    print("No matching products found.")
                else:
                    print("\nResults:")
                    for product in results:
                        print(product.display_details())

            elif choice == "3":
                product_id = input("Product ID: ")
                quantity = get_int("Quantity: ")

                summary = store.place_order(product_id, quantity)
                print_order_summary(summary)

            elif choice == "4":
                break

            else:
                print("Invalid choice.")

        except InventoryError as error:
            print(f"Error: {error}")


def main():
    store = Store()

    while True:
        print("\n------------------------------")
        print("   PyStore Inventory System")
        print("------------------------------")
        print("[1] Manager Menu")
        print("[2] Customer Menu")
        print("[3] Quit")

        choice = input("> ")

        if choice == "1":
            manager_menu(store)
        elif choice == "2":
            customer_menu(store)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


main()