import datetime
import random
import string

class Product:
    def __init__(self, id, name, price, stock):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock

    def display_details(self):
        return (f"Product ID: {self.id}\nProduct name: {self.name}\nPrice: ${self.price:,.2f}\n")
    
    def subtotal(self, quantity):
        return self.price * quantity
    
    def order(self, quantity):
        self.stock -= quantity
        
    
class PhysicalProduct(Product):
    def __init__(self, id, name, price, stock, weight):
        super().__init__(id, name, price, stock)
        self.weight = weight
        self.shipping = .05 * weight

    def total_price(self, quantity):
        print("Total Price")
        return super().subtotal(quantity) + self.shipping_cost(quantity)
    
    def shipping_cost(self, quantity):
        print("Shipping cost")
        return self.shipping * quantity
    
    def display_details(self):
        return super().display_details() + f"Stock: {self.stock}\nWeight: {self.weight}kg\n"

class DigitalProduct(Product):
    def __init__(self, id, name, price, stock, file_size, url):
        super().__init__(id, name, price, stock)
        self.file_size = file_size
        self.url = url

    def display_details(self):
        return super().display_details() +  f"File Size: {self.file_size}\nURL: {self.url}\n"
    
    def total_price(self, quantity):
        return super().subtotal(quantity)

class PerishableProduct(Product): # expiration date
    def __init__(self, id, name, price, stock, expiration_date):
        if expiration_date < datetime.date.today():
            raise Exception ("Product is already expired.")
        super().__init__(id, name, price, stock)
        self.expiration_date = expiration_date
        self.shipping = 5.0

    def display_details(self):
        return super().display_details() + f"Stock: {self.stock}\nExpiration Date: {self.expiration_date}\n"
    
    def order(self, quantity):
        if self.expiration_date < datetime.date.today():
            raise Exception ("Product expired, cannot order.")
        super().order(quantity)

    def shipping_cost(self, quantity):
        if super().subtotal(quantity) >= 25:
            return 0.0
        return self.shipping
    
    def total_price(self, quantity):
        subtotal = super().subtotal(quantity)
        return subtotal + self.shipping_cost(quantity)

class Store: 
    inventory = []
    
    def random_id(self):
        chars = string.ascii_uppercase + string.digits
        new_id = ""
        try: 
            while True:
                for x in range (6):
                    new_id += random.choice(chars)
                self.find_product(new_id)
        except:
            return new_id

    def add_product(self, type):
        name = input("Enter the product name: ")
        price = float(input("Enter the price: "))
        id = self.random_id()
        
        match type:
            case "1": # physical product
                stock = int(input("Enter the stock quantity: "))
                weight = float(input("Enter the weight in kg: "))
                self.inventory.append(PhysicalProduct(id, name, price, stock, weight))
                return f"{name} successfully added. ID: {id}"
            
            case "2": # digital product
                file_size = input("Enter the file size: ")
                url = input("Enter the url: ")
                self.inventory.append(DigitalProduct(id, name, price, 1, file_size, url))
                return f"{name} successfully added. ID: {id}"

            case "3": # perishable
                stock = int(input("Enter the stock quantity: "))
                expiration_date_str = input("Enter the expiration date (YYYY/MM/DD): ")
                date_list = str.split(expiration_date_str, "/")
                year = int(date_list[0])
                month = int(date_list[1])
                day = int(date_list[2])
                expiration_date = datetime.date(year, month, day)
                self.inventory.append(PerishableProduct(id, name, price, stock, expiration_date))
                return f"{name} successfully added. ID: {id}"

            case _: # default
                raise Exception ("Invalid input.")
            
    def remove_product(self, id):
        product = self.find_product(id)
        self.inventory.remove(product)
        return f"{product.name} removed from inventory."
    
    def restock(self, id, amount):
        product = self.find_product(id)
        product.stock += amount
        return f"{amount} added to {product.name}, totaling {product.stock}"

    def search(self, name):
        flag = 0
        for product in self.inventory:
            if name.lower() in product.name.lower():
                print(product.display_details())
                flag = 1
        
        if (not flag):
            raise Exception ("Product not found.")
    
    def find_product(self, id):
        for product in self.inventory:
            if product.id == id:
                return product
        raise Exception ("Product not found.")
    
    def list_products(self):
        flag = 0
        for product in self.inventory:
            if product.stock:
                print(product.display_details())
                flag = 1
        
        if flag:
            return
        
        raise Exception ("No products in stock.")
    
    def list_inventory(self):
        if not self.inventory:
            raise Exception ("No products in inventory.")
        
        for product in self.inventory:
            print(product.display_details())
    
    def order(self, id):
        product = self.find_product(id)
        if not product.stock:
            raise Exception ("Not in stock.")
        
        if not type(product) is DigitalProduct:
            quantity = int(input("Enter the amount you want to order: "))
            if product.stock < quantity:
                raise Exception ("Not enough in stock.")
            product.order(quantity)
            return (f"Order Summary: \n{product.name} x{quantity}\nUnit price: ${product.price:.2f}\n"
                    f"Subtotal: ${product.subtotal(quantity):.2f}\nShipping: ${product.shipping_cost(quantity):.2f}\n"
                    f"Total: ${product.total_price(quantity):.2f}\n"
                    f"Order placed! Remaining stock: {product.stock}"
            )
        product.order(0)
        return (f"Order Summary: \n{product.name}\nPrice: ${product.price:.2f}\n"
                f"Order placed!"
            )

# manager menu
def manager_menu():
    while True:
        try:
            print("1. Add product\n2. Remove product\n3. Restock product\n4. List all inventory\n5. Back")
            choice = input("Choose an option: ")
            match choice:
                case "1":
                    print("1. Physical\n2. Digital\n3. Perishable")
                    type = input("Choose the product type: ")
                    print(store.add_product(type))

                case "2":
                    id = input("Enter the id of the product: ")
                    print(store.remove_product(id))

                case "3":
                    id = input("Enter the id of the product: ")
                    amount = int(input ("Enter the amount: "))
                    print (store.restock(id, amount))

                case "4":
                    store.list_inventory()

                case "5":
                    break

                case _:
                    raise Exception ("Invalid input.")

        except Exception as e:
            print(e)

# customer menu
def customer_menu():
    while True:
        try:
            print("1. Browse all products\n2. Search by name\n3. Place an order\n4. Back")
            choice = input("Choose an option: ")

            match choice:
                case "1":
                    store.list_products()

                case "2":
                    name = input("Enter a name to search: ")
                    store.search(name)

                case "3":
                    id = input("Enter the ID of the product: ")
                    print(store.order(id))

                case "4":
                    break

                case _:
                    raise Exception ("Invalid input.")

        except Exception as e:
            print (e)

# main menu
store = Store()
while True:
    print("1. Manager Menu\n2. Customer Menu\n3. Exit")
    choice = input ("Choose an option: ")

    match choice:
        case "1":
            manager_menu()
        case "2":
            customer_menu()
        case "3":
            break