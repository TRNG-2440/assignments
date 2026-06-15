from abc import ABC, abstractmethod
from datetime import datetime

class InventoryError(Exception):
    pass

class ProductNotFoundError(InventoryError):
    pass

class OutOfStockError(InventoryError):
    pass

class ExpiredProductError(InventoryError):
    pass

class InvalidQuantityError(InventoryError):
    pass

class Product(ABC):

    def __init__(self, name, product_number, price, stock_quantity):
        self._name = name
        self._product_number = product_number
        self._price = price
        self._stock_quantity = stock_quantity

    @property
    def product_number(self):
        return self._product_number
    
    @property
    def stock(self):
        return self._stock_quantity
    
    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    def display_details(self):
        print(f"product #: {self._product_number}")
        print(f"name: {self._name}")
        print(f"Price: ${self._price:.2f}")
        print(f"Stock: {self._stock_quantity}")

    @abstractmethod
    def calculate_total_price(self, quantity):
        pass

    
class PhysicalProduct(Product):
    def __init__(self, name, product_number, price, stock_quantity, weight):
        super().__init__(name, product_number, price, stock_quantity)
        self._weight = weight
    
    def display_details(self):
        super().display_details()
        print(f"Weight: {self._weight} lbs")
    def calculate_shipping(self):
        return self._weight * 2.50
    
    def calculate_total_price(self, quantity):
        subtotal = self._price * quantity
        return subtotal + self.calculate_shipping()
        
class DigitalProduct(Product):
    def __init__(self, name, product_number, price, stock_quantity, file_size, download_url):
        super().__init__(name, product_number, price, stock_quantity)
        self._file_size = file_size
        self._download_url = download_url

    def calculate_total_price(self, quantity):
        return self._price * quantity

    def display_details(self):
        super().display_details()
        print(f"File Size: {self._file_size} MB")
        print(f"Download URL: {self._download_url}")

class PerishableProduct(Product):
    def __init__(self, name, product_number, price, stock_quantity, expiration_date):
        super().__init__(name, product_number, price, stock_quantity)
        self._expiration_date = expiration_date

    def calculate_total_price(self, quantity):
        subtotal = self._price * quantity
        if subtotal > 25:
            shipping = 0
        else:
            shipping = 3.99
        return subtotal + shipping
    
    def is_expired(self):
        return datetime.today().date() > self._expiration_date

    def display_details(self):
        super().display_details()
        print(f"Expires: {self._expiration_date}")

class Store:
    def __init__(self):
        self._products = []
        self._product_count = 1

    def generate_product_number(self):
        product_number = (f"PRD-{self._product_count:05d}")
        self._product_count += 1
        return product_number

    def add_product(self, product):
        self._products.append(product)
    
    def find_product(self, product_number):
        for product in self._products:
            if str.lower(product._product_number) == str.lower(product_number):
                return product
        return None

    def create_physical_product(self, name, price, stock, weight):
        product_number = self.generate_product_number()
        product = PhysicalProduct(name,product_number, price, stock, weight)
        self.add_product(product)
        return product
    
    def create_digital_product(self, name, price, stock, file_size, download_url):
        product_number = self.generate_product_number()
        product = DigitalProduct(name,product_number, price, stock, file_size, download_url)
        self.add_product(product)
        return product
    
    def create_Perishable_product(self, name, price, stock, expiration_date):
        product_number = self.generate_product_number()
        product = PerishableProduct(name,product_number, price, stock, expiration_date)
        self.add_product(product)
        return product

    def place_order(self, product_number, quantity):
        product = self.find_product(product_number)
        if product is None:
            raise ProductNotFoundError(f"Product '{product_number}' does not exist!")
        elif quantity <= 0:
            raise InvalidQuantityError("Quantity must be positive.")
        elif isinstance(product, PerishableProduct):
            if product.is_expired():
                raise ExpiredProductError(f"{product._name} has expired.")
        elif not isinstance(product, DigitalProduct):
            if quantity > product.stock:
                raise OutOfStockError(f"{product._name} is out of stock.")
        elif quantity > product.stock:
            raise OutOfStockError(f"Only {product.stock} item(s) available.")

        total = product.calculate_total_price(quantity)

        if not isinstance(product, DigitalProduct):
            product._stock_quantity -= quantity
        return {"name": product.name, "quantity": quantity, "product_price": product.price, "total": total}

    def search_products(self, search_term):
        matches = []
        for product in self._products:
            if search_term.lower() in product._name.lower():
                matches.append(product)
        return matches
    
    def list_products(self):
        for product in self._products:
            if product.stock > 0:
                product.display_details()
                print("*" * 25)

    def remove_product(self, product_number):
        product = self.find_product(product_number)
        if product is None:
            raise ProductNotFoundError(f"Product '{product_number}' does not exist!")
        else:
            self._products.remove(product)
        
    def restock_product(self, product_number, quantity):
        product = self.find_product(product_number)
        if product is None:
            raise ProductNotFoundError(f"Product '{product_number}' does not exist!")
        elif quantity <= 0:
            raise InvalidQuantityError("Quantity must be greater than 0!")
        else:
            product._stock_quantity += quantity
        
def manager_menu():
    while True:

        print("\n--- Manager Menu ---")
        print("1: Add Product")
        print("2: Remove Product")
        print("3: Restock Product")
        print("4: List Inventory")
        print("5: Back")

        return input("What Option would you like:  ")

def customer_menu():
    while True:

        print("\n--- Customer Menu ---")
        print("1: Browse Products")
        print("2: Search Products")
        print("3: Place Order")
        print("4: Back")

        return input("What Option would you like:  ")

store = Store()

while True:

    print("\n==============================")
    print("   PyStore Inventory System")
    print("==============================")
    print("1: Manager Menu")
    print("2: Customer Menu")
    print("3: Quit")

    choice = input("\nWhich menu would you like to see?    ")

    match choice:

        case "1":
            while True:
                menu = manager_menu()
                match menu:
                    case "1":
                        print("\nProduct Type")
                        print("1: Physical")
                        print("2: Digital")
                        print("3: Perishable")
                        try:
                            product_choice = int(input("Please select the type of product you would like: "))
                            match product_choice:
                                case 1:
                                    name = input("Please name the product: ")
                                    price = float(input("Please enter the price of the product: "))
                                    stock = int(input("How much of the product is in stock? "))
                                    weight = int(input("How much doe the product weigh in lbs: "))
                                    store.create_physical_product(name, price, stock, weight)
                                case 2:
                                    name = input("Please name the product: ")
                                    price = float(input("Please enter the price of the product: "))
                                    stock = int(input("How much of the product is in stock? "))
                                    file_size = int(input("How big is the file in MB? "))
                                    download_url = input("What is the download url? ")
                                    store.create_digital_product(name, price, stock, file_size, download_url)
                                case 3:
                                    name = input("Please name the product: ")
                                    price = float(input("Please enter the price of the product: "))
                                    stock = int(input("How much of the product is in stock? "))
                                    try:
                                        exp_date = datetime.strptime(input("Please enter the expiration date (YYYY-MM-DD):"), "%Y-%m-%d").date()
                                    except ValueError:
                                        print("Enter a valid date")
                                        continue
                                    store.create_Perishable_product(name, price, stock, exp_date)
                        except ValueError:
                            print("Invalid Price or quantity")
                            continue

                    case "2":
                        product_number = input("Product ID: ")
                        try:
                            store.remove_product(product_number)
                            print("Product removed.")
                        except ProductNotFoundError as e:
                            print(e)
                            continue
                        
                    case "3":
                        product_number = input("Product ID: ")

                        quantity = int(input("Quantity: "))
                        try:
                            store.restock_product(product_number,quantity)
                        except InventoryError as e:
                            print(e)
                            continue

                    case "4":
                        store.list_products()

                    case "5":
                        print("Exiting to Main Menu")
                        break
                    case _:
                        print("Please select a valid input.")
                        

        case "2":
            while True:
                menu = customer_menu()
                match menu:
                    case "1":
                        store.list_products()

                    case "2":
                        term = input("Search: ")
                        results = store.search_products(term)
                        for product in results:
                            product.display_details()
                        
                    case "3":
                        product_id = input("Please enter the product ID number: ")
                        quantity = int(input("How many would you like?  "))
                        try:
                            order = store.place_order(product_id,quantity)
                            print("\nOrder Summary")
                            print("-" * 30)
                            print(f"{order['name']} "f"x{order['quantity']}")
                            print(f"Unit Price: "f"${order['product_price']:.2f}")
                            print(f"Total: "f"${order['total']:.2f}")

                        except InventoryError as e:
                            print(f"Error: {e}")
                            continue

                    case "4":
                        print("Back to main menu!")
                        break

        case "3":
            print("Goodbye!")
            break

        case _:
            print("Please select one of the options provided in the menu!")
