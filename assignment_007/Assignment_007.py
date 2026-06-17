from datetime import datetime


class Product:
    def __init__(self, product_id, name, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity
        
    def display_info(self):
        print(f"Product ID: {self.product_id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self.price}")
        print(f"Stock Quantity: {self.stock_quantity}")

    def cal_total(self,quantity):
        if quantity > self.stock_quantity:
            raise ValueError("Insufficient stock")
        return self.price * quantity
    
    
class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock_quantity, weight):
        super().__init__(product_id, name, price, stock_quantity)
        self.weight = weight

    def display_info(self):
        super().display_info()
        print(f"Weight: {self.weight}")
        
    def cal_shipping(self):
        shipping_cost = self.weight * 10
        return shipping_cost
    
    def cal_total(self, quantity):
        return super().cal_total(quantity) + self.cal_shipping()
    

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock_quantity, file_size, download_url):
        super().__init__(product_id, name, price, stock_quantity)
        self.file_size = file_size
        self.download_url = download_url

    def display_info(self):
        super().display_info()
        print(f"File Size: {self.file_size}")
        print(f"Download URL: {self.download_url}")
        

class PerishableProduct(Product):
    def __init__(self, product_id, name, price, stock_quantity, expiration_date):
        super().__init__(product_id, name, price, stock_quantity)
        self.expiration_date = datetime.strptime(expiration_date, "%m/%d/%Y")

    def display_info(self):
        super().display_info()
        print(f"Expiration Date: {self.expiration_date.strftime('%m/%d/%Y')}")
        
    def is_expired(self):
        return datetime.now() > self.expiration_date
    
    def cal_total(self, quantity):
        if self.is_expired():
            raise ValueError(f"{self.name} has expired and cannot be ordered.")
        subtotal = super().cal_total(quantity)
        if subtotal > 25:
            shipping = 0
        else:
            shipping = 2.99
        return subtotal + shipping
    
class Store:
    product_id_counter = 0

    def __init__(self):
        self.products = []

    def add_product(self, product_type):
        name = input("Name: ")
        price = float(input("Price: "))
        stock_quantity = int(input("Stock quantity: "))
        product_id = f"PRD-{Store.product_id_counter:06d}"
        Store.product_id_counter += 1

        if product_type == "PHYSICAL":
            weight = float(input("Weight: "))
            product = PhysicalProduct(product_id, name, price, stock_quantity, weight)
        elif product_type == "DIGITAL":
            file_size = input("File size: ")
            download_url = input("Download URL: ")
            product = DigitalProduct(product_id, name, price, stock_quantity, file_size, download_url)
        elif product_type == "PERISHABLE":
            expiration_date = input("Expiration date (MM/DD/YYYY): ")
            try:
                product = PerishableProduct(product_id, name, price, stock_quantity, expiration_date)
            except ValueError:
                print("Invalid date format. Product not added.")
                return
        else:
            print("Invalid product type.")
            return

        self.products.append(product)
        print(f"{product_type.title()} product added.")
        product.display_info()

    def remove_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                self.products.remove(product)
                print(f"Removed {product.name}.")
                return
        raise ValueError("Product not found.")

    def restock_product(self, product_id, quantity):
        for product in self.products:
            if product.product_id == product_id:
                product.stock_quantity += quantity
                print(f"Restocked {product.name}. New stock: {product.stock_quantity}")
                return
        raise ValueError("Product not found.")

    def search_products(self, term):
        term = term.lower()
        results = [p for p in self.products if term in p.name.lower()]
        return results

    def list_inventory(self):
        in_stock = [p for p in self.products if p.stock_quantity > 0]
        if not in_stock:
            print("No products in stock.")
        else:
            for product in in_stock:
                product.display_info()
                print("-" * 20)
                
    def place_order(self, product_id, quantity):
        product_ordered = None
        for product in self.products:
            if product.product_id == product_id:
                product_ordered = product
                break
        if not product_ordered:
            raise ValueError("Product not found.")

        total = product_ordered.cal_total(quantity)

        if not isinstance(product_ordered, DigitalProduct):
            product_ordered.stock_quantity -= quantity

        return total, product_ordered

def manager_menu(store):
    while True:
        print("--- Manager Menu ---")
        print("1. Add product")
        print("2. Remove product")
        print("3. Restock product")
        print("4. List all inventory")
        print("5. Back")
        choice = input("> ")

        if choice == "1":
            print("Product type:")
            print("1. Physical")
            print("2. Digital")
            print("3. Perishable")
            type_choice = input("> ")
            if type_choice == "1":
                store.add_product("PHYSICAL")
            elif type_choice == "2":
                store.add_product("DIGITAL")
            elif type_choice == "3":
                store.add_product("PERISHABLE")
            else:
                print("Invalid product type.")
        elif choice == "2":
            product_id = input("Product ID: ")
            try:
                store.remove_product(product_id)
            except ValueError as e:
                print(e)
        elif choice == "3":
            product_id = input("Product ID: ")
            try:
                quantity = int(input("Quantity to add: "))
                store.restock_product(product_id, quantity)
            except ValueError as e:
                print(e)
        elif choice == "4":
            store.list_inventory()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")
            
            
def customer_menu(store):
    while True:
        print("--- Customer Menu ---")
        print("1. Browse all products")
        print("2. Search by name")
        print("3. Place an order")
        print("4. Back")
        choice = input("> ")

        if choice == "1":
            store.list_inventory()
        elif choice == "2":
            term = input("Search: ")
            results = store.search_products(term)
            if not results:
                print("No matching products found.")
            else:
                for product in results:
                    product.display_info()
                    print("-" * 20)
        elif choice == "3":
            product_id = input("Product ID: ")
            try:
                quantity = int(input("Quantity: "))
                total, product = store.place_order(product_id, quantity)
                print("=" * 20)
                print("Order Summary")
                print(f"{product.name} x{quantity}")
                print(f"Total: ${total}")
                print("=" * 20)
                print(f"Order placed! Remaining stock: {product.stock_quantity}")
            except ValueError as e:
                print(e)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
            
            
store = Store()
while True:
    print("=" * 20)
    print("Isauro's Store Inventory System")
    print("=" * 20)
    print("1. Manager Menu")
    print("2. Customer Menu")
    print("3. Quit")
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