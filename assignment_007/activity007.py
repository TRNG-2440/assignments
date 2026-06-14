from abc import ABC
from datetime import date
import re

SHIPPING_RATE = 10.0
MENU_WIDTH = 31

class ProductTypeError(Exception):
    """raised when Product Type is wrong"""
    def __init__(self, message="Incorrect Prototype"):
        super().__init__(f"{message}")

class Product(ABC):
    __total_products = 0

    def __init__(self, name="", price=0.0, qty=0):
        self.id = self.generate_id()
        self.name = name
        self.price = price
        self.quantity = qty

    def details(self):
        return f"name: {self.name}\nid: {self.id}\nprice: {self.price}\n quantity: {self.quantity}\n"

    def total_price(self, qty):
        return self.price * qty
    
    def generate_id(self):
        """generate product id"""
        base = 1 * (10**5)
        prod = Product.__total_products
        Product.__total_products += 1

        return base + prod

class PhysicalProduct(Product):
    def __init__(self, name="", price=0.0, qty=0, weight=0.0, rate=0.0):
        super().__init__(name, price, qty)
        self.weight_kg = weight
        self.shipping_rate = rate
    
    def details(self):
        sup = super().details()
        return f"{sup}weight: {self.weight_kg}\n"
    
    def shipping(self, rate):
        return self.weight_kg * rate
    
    def total_price(self, qty):
        return self.price * qty + self.shipping(self.shipping_rate)

class DigitalProduct(Product):
    def __init__(self, name="", price=0.0, qty=None, size=0):
        super().__init__(name, price, qty)
        self.size_kb = size

    def details(self):
        sup = super().details()
        return f"{sup}size: {self.size_kb}\n"
    
    def total_price(self):
        return self.price

class PerishableProduct(Product):
    def __init__(self, name="", price=0.0, qty=0, exp_date=None):
        super().__init__(name, price, qty)
        self.expiration = exp_date
    
    def is_expired(self):
        return self.expiration < date.today()
    
    def shipping(self, total):
        return total if total < 25.0 else total + 25.0

class Store():
    def __init__(self):
        self.inventory = {}
        self.main_options = ["Manager Menu", 
                             "Customer Menu"]
        self.manager_options = ["Add product",
                                "Remove product",
                                "Restock product",
                                "List all inventory"]
        self.customer_options = ["Browse all products",
                                 "Search by name",
                                 "Place an order"]
        self.product_options = ["Physical",
                                "Digital",
                                "Perishable"]

    def add_item(self, item):
        self.inventory[item.id] = item

    def remove(self, id):
        return self.inventory.pop(id)

    def add_inventory(self, item, qty):
        if type(item) not in (PerishableProduct, PhysicalProduct):
            raise ProductTypeError
        else:
            self.inventory[item.id].quantity += qty
            
    def search_name(self, exp):
        for item in self.inventory.values():
            if re.search(exp, item.name):
                print(f"{item.name}{item.id}")
    
    def list_instock(self):
        stock = [item for item in self.inventory.values() if item.qty > 0]
        for item in stock:
            print(item.details())

    def list_all(self):
        for item in self.inventory.values():
            print(item.details())

    def create_order(self):
        pass

# self.main_options
# self.manager_options 
# self.customer_options
# self.product_options

# "Add product",
# "Remove product",
# "Restock product",
# "List all inventory"
    def manager_menu(self):
        print("manager options")
        
        while True:
            print_menu(*self.manager_options)
            user_selection = get_selection(len(self.manager_options))
            match user_selection:
                case 1: # Add product
                    self.product_menu()
                case 2: # Remove product
                    name = input("search product: ")
                    self.search_name(name)
                    id = valid_int("id to remove: ")
                    self.remove(id)
                case 3: # Restock product
                    name = input("search product: ")
                    self.search_name(name)
                    id = valid_int("item: ")
                    qty = valid_int("qty to add: ")
                    self.add_inventory(self.inventory[id], qty)
                case 4: # List all inventory
                    self.list_all()
                case 0:
                    print("returning to main menu")
                    return None
            
    def customer_menu(self):
        print("customer options")
        print_menu(*self.customer_options)
        user_selection = get_selection(len(self.customer_options))
        match user_selection:
            case 1: # "Browse all products"
                self.list_all()
            case 2: # "Search by name",
                name = input("product: ")
                self.search_name(name)
            case 3: # "Place an order"
                self.create_order()
            case 0:
                print("returning to main menu")
                return None
            
    def product_menu(self):
        print("Product type")
        print_menu(*self.product_options)
        user_selection = get_selection(len(self.product_options))
        match user_selection:
            case 1: # Phys
                name = input("product: ")
                price = get_price("price: ")
                qty = valid_int("quantity: ")
                weight = valid_int("weight: ")
                self.add_item(PhysicalProduct(name, price, qty, weight, SHIPPING_RATE))
            case 2: # Digital
                name = input("product: ")
                price = get_price("price: ")
                qty = valid_int("quantity: ")
                size = valid_int("size in kb: ")
                self.add_item(DigitalProduct(name, price, qty, size))
            case 3: # Parishable
                name = input("product: ")
                price = get_price("price: ")
                qty = valid_int("quantity: ")
                exp = valid_int("days before expiration: ")
                self.add_item(PerishableProduct(name, price, qty, exp))
            case 0:
                print("no product created")
                return None

    def run(self):
        w = 31
        border = "=" * w + "\n"
        title = "Grocery Store"
        banner = f"{border}{title: ^{w}}\n{border}"
        print(banner)
        while True:
            print_menu(*self.main_options)
            user_selection = get_selection(len(self.main_options))
            match user_selection:
                case 1: # Manager
                    self.manager_menu()
                case 2: # customer
                    self.customer_menu()
                case 0: # exit
                    print("exiting...\nGoodbye")
                    return user_selection

def print_menu(*args:str) -> None:
    w = MENU_WIDTH
    """
    print main menu from list
    """
    print()
    for idx, item in enumerate(args, 1):
        print(f"[{idx}] {item:.>{w}}")
    print("[0]" + "." * (w-4) + " exit")

def get_selection(lim:int = 0) -> int:
    """
    get selection from user, return int within limit
    - repeat on ValueError
    """
    valid = False
    while not valid:
        try:
            sel = int(input(f"> "))
        except ValueError:
            print("bad value")
            continue
        except Exception as e:
            raise e
        print()
        match sel:
            case sel if sel < 0 :
                print("value too low")
                valid = False
            case sel if sel > lim:
                print("value too high")
                valid = False
            case _:
                valid = True
    return sel

def get_price(msg=f"> ") -> float:
    """
    get input for price
    - repeat on ValueError
    """
    while True:
        try:
            sel = float(input(msg))
        except ValueError:
            print("bad value")
            continue
        except Exception as e:
            raise e
        if sel > 0.0:
            return sel

def valid_int(msg=f"> "):
    while True:
        try:
            sel = int(input(msg))
        except ValueError:
            print("bad value")
            continue
        except Exception as e:
            raise e
        if sel > 0.0:
            return sel


if __name__ == "__main__":
    s = Store()

    s.run()