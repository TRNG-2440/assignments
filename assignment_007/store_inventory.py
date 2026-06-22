from abc import ABC, abstractmethod
from datetime import datetime

# base product class
class Product(ABC):

    # class var to generate unique product ids
    id_counter = 1

    def __init__(self, name, price, stock):
        self.product_id = f"PRD-{Product.id_counter:04d}"
        Product.id_counter += 1

        self.name = name
        self.price = price
        self.stock = stock

    # calc total cost for a quantity
    def calculate_total(self, quantity):
        return self.price * quantity

    # abstract method that every subclass must implement
    # use abstract bc every prod type displays diff details
    @abstractmethod
    def display_details(self):
        pass


# physical product
    def __init__(self, name, price, stock, weight):
        super().__init__(name, price, stock)
        self.weight = weight

    # shipping cost increases with weight
    def shipping_cost(self):
        return self.weight * 2

    # total has shipping cost
    def calculate_total(self, quantity):
        subtotal = self.price * quantity
        shipping = self.shipping_cost()
        return subtotal + shipping

    def display_details(self):
        print(
            f"[{self.product_id}] {self.name} | "
            f"${self.price:.2f} | Stock: {self.stock} | "
            f"Weight: {self.weight} lbs"
        )


# digutal product
class DigitalProduct(Product):

    def __init__(self, name, price, stock, file_size, download_url):
        super().__init__(name, price, stock)
        self.file_size = file_size
        self.download_url = download_url

    # no shipping cost
    def calculate_total(self, quantity):
        return self.price * quantity

    def display_details(self):
        print(
            f"[{self.product_id}] {self.name} | "
            f"${self.price:.2f} | "
            f"File Size: {self.file_size} MB"
        )


# perishable product
class PerishableProduct(Product):

    FLAT_SHIPPING = 3.99

    def __init__(self, name, price, stock, expiration_date):
        super().__init__(name, price, stock)

        # converts string date into datetime object
        self.expiration_date = datetime.strptime(
            expiration_date,
            "%Y-%m-%d"
        ).date()

    # checks if product is expired
    def is_expired(self):
        return datetime.today().date() > self.expiration_date

    # shipping free if subtotal exceeds $25
    def calculate_total(self, quantity):
        subtotal = self.price * quantity

        if subtotal > 25:
            shipping = 0
        else:
            shipping = self.FLAT_SHIPPING

        return subtotal + shipping

    def display_details(self):
        print(
            f"[{self.product_id}] {self.name} | "
            f"${self.price:.2f} | Stock: {self.stock} | "
            f"Expires: {self.expiration_date}"
        )


# store class
class Store:

    def __init__(self):
        self.inventory = {}

    # add product to inventory
    def add_product(self, product):
        self.inventory[product.product_id] = product

    # remove product
    def remove_product(self, product_id):
        if product_id not in self.inventory:
            raise ValueError("Product ID not found.")

        del self.inventory[product_id]

    # restock product
    def restock_product(self, product_id, quantity):
        if product_id not in self.inventory:
            raise ValueError("Product ID not found.")

        self.inventory[product_id].stock += quantity

    # search products by partial name match
    def search_products(self, keyword):
        results = []

        for product in self.inventory.values():
            if keyword.lower() in product.name.lower():
                results.append(product)

        return results

    # list all products currently in stock
    def list_products(self):
        for product in self.inventory.values():

            if isinstance(product, DigitalProduct):
                product.display_details()

            elif product.stock > 0:
                product.display_details()

    # place an order
    def place_order(self, product_id, quantity):

        if product_id not in self.inventory:
            raise ValueError("Product not found.")

        product = self.inventory[product_id]

        # check expiration for perishables
        if isinstance(product, PerishableProduct):
            if product.is_expired():
                raise ValueError(
                    f"{product.name} has expired and cannot be ordered."
                )

        # digital products do not reduce stock
        if isinstance(product, DigitalProduct):
            total = product.calculate_total(quantity)

        else:
            if product.stock <= 0:
                raise ValueError("Product is out of stock.")

            if quantity > product.stock:
                raise ValueError(
                    f"Only {product.stock} units available."
                )

            product.stock -= quantity
            total = product.calculate_total(quantity)

        print("Order Summary")
        print(f"{product.name} x{quantity}")
        print(f"Total: ${total:.2f}")

        return total


# CLI menu system
store = Store()

while True:

    print("PyStore Inventory System")
    print("[1] Manager Menu")
    print("[2] Customer Menu")
    print("[3] Quit")

    choice = input("> ")

    # manager menu
    if choice == "1":

        while True:

            print("Manager Menu")
            print("[1] Add Product")
            print("[2] Remove Product")
            print("[3] Restock Product")
            print("[4] List Inventory")
            print("[5] Back")

            manager_choice = input("> ")

            if manager_choice == "1":

                print("\nProduct Type")
                print("[1] Physical")
                print("[2] Digital")
                print("[3] Perishable")

                product_type = input("> ")

                try:
                    name = input("Name: ")
                    price = float(input("Price: "))
                    stock = int(input("Stock Quantity: "))

                    if product_type == "1":

                        weight = float(input("Weight: "))

                        product = PhysicalProduct(
                            name,
                            price,
                            stock,
                            weight
                        )

                    elif product_type == "2":

                        file_size = float(
                            input("File Size (MB): ")
                        )

                        url = input(
                            "Download URL: "
                        )

                        product = DigitalProduct(
                            name,
                            price,
                            stock,
                            file_size,
                            url
                        )

                    elif product_type == "3":

                        expiration = input(
                            "Expiration Date (YYYY-MM-DD): "
                        )

                        product = PerishableProduct(
                            name,
                            price,
                            stock,
                            expiration
                        )

                    else:
                        print("Invalid product type.")
                        continue

                    store.add_product(product)

                    print("\nProduct Added!")
                    product.display_details()

                except Exception as e:
                    print("Error:", e)

            elif manager_choice == "2":

                try:
                    pid = input("Product ID: ")
                    store.remove_product(pid)
                    print("Product removed.")

                except Exception as e:
                    print("Error:", e)

            elif manager_choice == "3":

                try:
                    pid = input("Product ID: ")
                    qty = int(input("Quantity to add: "))

                    store.restock_product(pid, qty)

                    print("Product restocked.")

                except Exception as e:
                    print("Error:", e)

            elif manager_choice == "4":
                store.list_products()

            elif manager_choice == "5":
                break

            else:
                print("Invalid option.")

    # customer menu
    elif choice == "2":

        while True:

            print("Customer Menu")
            print("[1] Browse Products")
            print("[2] Search Product")
            print("[3] Place Order")
            print("[4] Back")

            customer_choice = input("> ")

            if customer_choice == "1":

                store.list_products()

            elif customer_choice == "2":

                keyword = input("Search: ")

                results = store.search_products(keyword)

                if results:
                    for product in results:
                        product.display_details()
                else:
                    print("No matching products found.")

            elif customer_choice == "3":

                try:
                    pid = input("Product ID: ")
                    qty = int(input("Quantity: "))

                    store.place_order(pid, qty)

                except Exception as e:
                    print("Error:", e)

            elif customer_choice == "4":
                break

            else:
                print("Invalid option.")

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid option.")