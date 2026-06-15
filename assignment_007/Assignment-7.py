import random
import datetime

class Product:
    def __init__(self, productID, name, price, stock):
        self.productID = productID
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"ID: {self.productID} | {self.name} | Price: ${self.price:.2f} | Stock: {self.stock}"

    def total_price(self):
        return self.price
    
    def get_id(self):
        return self.productID
    
    def get_name(self):
        return self.name
    
    def get_price(self):
        return self.price
    
    def get_stock(self):
        return self.stock
    
    def restock(self, amount):
        self.stock += amount

    
    
        
class DigitalProduct(Product):
    def __init__(self, productID, name, price, stock, file_size, url):
        super().__init__(productID, name, price, stock)
        self.file_size = file_size
        self.url = url
    
    def get_size(self):
        return self.file_size
    
    def get_url(self):
        return self.url
    
    def get_total(self, quantity):
        if quantity > self.stock:
            raise ValueError("Not enough stock for this!")
        return self.price * quantity
    
    def get_ship_cost():
        return 0
    
    
class PhysicalProduct(Product):
    def __init__(self, productID, name, price, stock, weight):
        super().__init__(productID, name, price, stock)
        self.weight = weight
        self.shipping_cost = weight * 0.1 
    
    def get_total(self, quantity):
        if quantity > self.stock:
            raise ValueError("Not enough stock for this purchase!")
        self.stock = self.stock - quantity

        return quantity * (self.shipping_cost + self.price)
    
    def get_ship_cost(self):
        return self.shipping_cost
    
class PerishableProduct(Product):
    def __init__(self, productID, name, price, stock, expiration_date):
        super().__init__(productID, name, price, stock)
        self.expiration = expiration_date

    def is_expired(self):
        return datetime.datetime.now() > self.expiration
    
    def get_total(self, quantity):
        if self.is_expired():
            raise ValueError("Cannot shipped expired items!")
        
        if quantity > self.stock:
            raise ValueError("Not enough stock for this purchase!")

        
        subtotal = quantity * self.price

        shipping = 0.0 if subtotal > 25 else 5.0

        self.stock = self.stock - quantity

        return subtotal + shipping
                
    
class Store:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        self.products[product.productID] = product

    def search_product(self, query):
        results = [p for p in self.products.values() if query.lower() in p.name.lower()]
        return results
    
    def get_product(self, number):
        return self.products.get(number)
    
    def list_products(self):
        print("\n--- Current Products ---")
        for p in self.products.values():
            print(p)

    def restock(self, pid, amount):
        self.products[pid].restock(amount)

    def remove_product(self, number):
        del self.products[number]

    def process_order(self, pid, quantity):
        if pid not in self.products:
            raise NameError("Product not found")
        
        product = self.products[pid]
        try:
            total = product.get_total(quantity)
            print(f"Order processed! Total for {quantity} {product.name}(s): ${total:.2f}")
        except ValueError as e:
            print (f"Order failed: {e}")
    
        
def main():
    store = Store()
    print('''
==============================
   PyStore Inventory System
==============================

''')
    while True:
        print("[1] Manager Menu\n[2] Customer Menu\n[0] Quit")
        mode = input("> ")

        match mode:
        # Manager Mode
        
            case "1":
                print("--- Manager Menu ---")
                print("[1] Add product [2] Remove product [3] Restock product [4] List all inventory [5] Back")
                while True:
                    mana = input("> ")

                    match mana:
                        case "1":
                            # Manager add product
                            print("--- Product Types ---")
                            print("[1] Physical [2] Digital [3] Perishable")

                            type = input("> ")
                            name = input("Name: ")
                            try: 
                                price = float(input("Price: "))
                            except ValueError as e:
                                print(f"Invalid price: {e}")
                                continue

                            try:
                                stock = int(input("Stock"))
                            except ValueError as e:
                                print(f"Invalid stock: {e}")
                                continue
                            match type:
                                case "1":
                                    id = "PHY" + str(random.randint(0, 999))
                                    try:
                                        weight = float(input("Weight: "))
                                        store.add_product(PhysicalProduct(id, name, price, stock, weight))
                                    except ValueError as e:
                                        print(f"Invalid Weight: {e}")
                                        continue

                                case "2":
                                    id = "DIG" + str(random.randint(0, 999))
                                    file_size = float(input("File Size: "))
                                    url = input("URL: ")
                                    store.add_product(DigitalProduct(id, name, price, stock, file_size, url))
                                case "3":
                                    id = "PER" + str(random.randint(0, 999))
                                    try:
                                        date = input("Expiration Date (format: YYYY-MM-DD):")
                                        expiration_date = datetime.datetime.strptime(date, "%Y-%m-%d")
                                        store.add_product(PerishableProduct(id, name, price, stock, expiration_date))
                                    except ValueError as e:
                                        print(f"Invalid Date: {e}")
                                        continue

                        case "2":
                            # Manager remove product
                            select = input("Put in the product ID: ")
                            sel_prod = store.get_product(select)
                            if not sel_prod:
                                raise ValueError("Product not found!")
                            
                            else:
                                store.remove_product(select)
                                print("Product successfully removed!")
                        case "3":
                            # Manager restock
                            select = input("Put in the product ID: ")
                            sel_prod = store.get_product(select)
                            if not sel_prod:
                                raise ValueError("Product not found!")
                            else:
                                try:
                                    restock = int(input("How much do you want to restock?"))
                                    store.restock(select, restock)
                                except ValueError as e:
                                    print(f"Restock failed: {e}")
                                    continue
                        case "4":
                            store.list_products()

                        case "5":
                            break
            # Customer Mode
            case "2":
                pid = input("Enter Product ID to order: ")
                try:
                    qty = int(input("Enter quantity: "))
                    print(store.process_order(pid, qty))
                except ValueError as e:
                    print(f"Invalid quantity: {e}")
                    continue

            # Exit
            case "0":
                print("Thanks for visiting the PyStore!")
                break

main()