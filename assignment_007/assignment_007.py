from datetime import datetime, date


class Product:
    product_running_count = 1


    def __init__(self, name, price, stock_quantity):
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity
        self.product_id = self.create_product_id()


    def create_product_id(self):
        number = f"PRD-{Product.product_running_count:04d}"
        Product.product_running_count += 1
        return number


    def display_details(self):
        print(f"   [{self.product_id}]  {self.name}  |  ${self.price:.2f}  |  In Stock: {self.stock_quantity}")


    def calc_price(self, quantity):
        return self.price * quantity


class PhysicalProduct(Product):
    def __init__(self, name, price, stock_quantity, weight):
        super().__init__(name, price, stock_quantity)
        self.weight = weight


    def calc_shipping_cost(self, quantity):
        return self.weight * quantity * 2


    def calc_price(self, quantity):
        subtotal = self.price * quantity
        shipping = self.calc_shipping_cost(quantity)
        return subtotal + shipping


    def display_details(self):
        print(f"   [{self.product_id}]  {self.name}  |  ${self.price:.2f}  |  In Stock: {self.stock_quantity}  |  Weight: {self.weight}lbs")


class DigitalProduct(Product):
    def __init__(self, name, price, file_size, url):
        super().__init__(name, price, stock_quantity=0)
        self.file_size = file_size
        self.url = url


    def display_details(self):
        print(f"   [{self.product_id}]  {self.name}  |  ${self.price:.2f}  |  File Size: {self.file_size}mbs  |  URL: {self.url}")


class PerishableProduct(Product):
    def __init__(self, name, price, stock_quantity, expiration_date):
        super().__init__(name, price, stock_quantity)
        self.expiration_date = expiration_date


    def is_expired(self):
        if isinstance(self.expiration_date, str):
            exp_date = datetime.strptime(self.expiration_date, "%Y-%m-%d").date()
        else:
            exp_date = self.expiration_date

        return exp_date < date.today()


    def calc_price(self, quantity):
        subtotal = self.price * quantity
        shipping = 0 if subtotal > 25 else 3.99
        return subtotal + shipping


    def display_details(self):
        print(f"   [{self.product_id}]  {self.name}  |  ${self.price:.2f}  |  In Stock: {self.stock_quantity}  |  Expiration Date: {self.expiration_date}")


class Store:
    def __init__(self):
        self.products = {}


    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added to the store.")

        self.products[product.product_id] = product
        print(f"{product.name} added successfully.")
        product.display_details()


    def remove_product(self, product_id):
        if product_id not in self.products:
            raise ValueError(f"Product ID {product_id} was not found.")

        removed_product = self.products.pop(product_id)
        print(f"{removed_product.name} removed successfully.")


    def restock_product(self, product_id, quantity):
        if product_id not in self.products:
            raise ValueError(f"Product ID {product_id} was not found.")

        if quantity <= 0:
            raise ValueError("Restock quantity must be greater than 0.")

        product = self.products[product_id]

        if isinstance(product, DigitalProduct):
            raise ValueError(f"{product.name} is a digital product and does not need restocking.")

        product.stock_quantity += quantity
        print(f"{product.name} restocked successfully. New stock: {product.stock_quantity}")


    def search_product_name(self, name_partial):
        matches = []

        for product in self.products.values():
            if name_partial.lower() in product.name.lower():
                matches.append(product)

        return matches


    def list_in_stock(self):
        in_stock_products = []

        for product in self.products.values():
            if isinstance(product, DigitalProduct):
                in_stock_products.append(product)
            elif product.stock_quantity > 0:
                in_stock_products.append(product)

        return in_stock_products


    def list_all_inventory(self):
        return list(self.products.values())


    def place_order(self, product_id, quantity):
        if product_id not in self.products:
            raise ValueError(f"Product ID {product_id} was not found.")

        if quantity <= 0:
            raise ValueError("Order quantity must be greater than 0.")

        product = self.products[product_id]

        if isinstance(product, PerishableProduct) and product.is_expired():
            raise ValueError(f"{product.name} has expired and cannot be ordered.")

        if not isinstance(product, DigitalProduct):
            if product.stock_quantity <= 0:
                raise ValueError(f"{product.name} is out of stock.")

            if quantity > product.stock_quantity:
                raise ValueError(f"Only {product.stock_quantity} of {product.name} available.")

        subtotal = product.price * quantity
        total = product.calc_price(quantity)

        if isinstance(product, PhysicalProduct):
            shipping = product.calc_shipping_cost(quantity)
            shipping_message = "weight-based"
        elif isinstance(product, PerishableProduct):
            shipping = 0 if subtotal > 25 else 3.99
            if shipping == 0:
                shipping_message = "free over $25"
            else:
                shipping_message = "flat-rate"
        else:
            shipping = 0
            shipping_message = "no shipping"

        if not isinstance(product, DigitalProduct):
            product.stock_quantity -= quantity

        print("=" * 30)
        print("Order Summary")
        print("=" * 30)
        print(f"{product.name} x{quantity}")
        print(f"Unit Price : ${product.price:.2f}")
        print(f"Subtotal   : ${subtotal:.2f}")
        print(f"Shipping   : ${shipping:.2f} ({shipping_message})")
        print("-" * 30)
        print(f"Total      : ${total:.2f}")
        print("=" * 30)

        if isinstance(product, DigitalProduct):
            print("Order placed successfully.")
        else:
            print(f"Order placed! Remaining stock: {product.stock_quantity}")


# --------------------------------------------------------


def get_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Error: Please enter a valid whole number.")


def get_float(prompt):
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Error: Please enter a valid number.")


def get_date_string(prompt):
    while True:
        date_text = input(prompt).strip()

        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return date_text
        except ValueError:
            print("Error: Please enter a valid date in YYYY-MM-DD format.")


# --------------------------------------------------------


def add_product_cli(store):
    print("\nProduct type:")
    print("[1] Physical")
    print("[2] Digital")
    print("[3] Perishable")

    choice = input("> ").strip()

    name = input("Name: ").strip()
    price = get_float("Price: ")

    try:
        if choice == "1":
            stock_quantity = get_int("Stock quantity: ")
            weight = get_float("Weight: ")
            product = PhysicalProduct(name, price, stock_quantity, weight)

        elif choice == "2":
            file_size = get_float("File size: ")
            url = input("Download URL: ").strip()
            product = DigitalProduct(name, price, file_size, url)

        elif choice == "3":
            stock_quantity = get_int("Stock quantity: ")
            expiration_date = get_date_string("Expiration date (YYYY-MM-DD): ")
            product = PerishableProduct(name, price, stock_quantity, expiration_date)

        else:
            print("Error: Invalid product type.")
            return

        store.add_product(product)

    except Exception as e:
        print(f"Error: {e}")


def manager_menu(store):
    while True:
        print("\n--- Manager Menu ---")
        print("[1] Add product")
        print("[2] Remove product")
        print("[3] Restock product")
        print("[4] List all inventory")
        print("[5] Back")

        choice = input("> ").strip()

        if choice == "1":
            add_product_cli(store)

        elif choice == "2":
            product_id = input("Product ID: ").strip()

            try:
                store.remove_product(product_id)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "3":
            product_id = input("Product ID: ").strip()
            quantity = get_int("Restock quantity: ")

            try:
                store.restock_product(product_id, quantity)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            inventory = store.list_all_inventory()

            if not inventory:
                print("Inventory is empty.")
            else:
                print("\nCurrent Inventory:")
                for product in inventory:
                    product.display_details()

        elif choice == "5":
            break

        else:
            print("Error: Invalid menu choice.")


def customer_menu(store):
    while True:
        print("\n--- Customer Menu ---")
        print("[1] Browse all products")
        print("[2] Search by name")
        print("[3] Place an order")
        print("[4] Back")

        choice = input("> ").strip()

        if choice == "1":
            products = store.list_in_stock()

            if not products:
                print("No products available.")
            else:
                print("\nAvailable Products:")
                for product in products:
                    product.display_details()

        elif choice == "2":
            name_partial = input("Search: ").strip()
            results = store.search_product_name(name_partial)

            if not results:
                print("No matching products found.")
            else:
                print("Results:")
                for product in results:
                    product.display_details()

        elif choice == "3":
            product_id = input("Product ID: ").strip()
            quantity = get_int("Quantity: ")

            try:
                store.place_order(product_id, quantity)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            break

        else:
            print("Error: Invalid menu choice.")

def main():
    store = Store()

    while True:
        print("\n" + "=" * 30)
        print("PyStore Inventory System")
        print("=" * 30)
        print("[1] Manager Menu")
        print("[2] Customer Menu")
        print("[3] Quit")

        choice = input("> ").strip()

        if choice == "1":
            manager_menu(store)

        elif choice == "2":
            customer_menu(store)

        elif choice == "3":
            print("Goodbye.")
            break

        else:
            print("Error: Invalid menu choice.")


if __name__ == "__main__":
    main()