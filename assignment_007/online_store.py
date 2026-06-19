"""

Physical, Digital, Perishable products
Product Calss
    - productID
    - name
    - price
    - stock quantity



    1. Physical Product
        - Weight
            (shipping cost = 5 --> base fee)
        - overrides total price calculation
            ==> shipping_fee = shipping cost + weight * 2.5
            ==> Total cost = shipping_fee + (item price * item quantity)
        
    
    2. Digital Product
        - file size attribute and a download URL
        - no shipping cost -- > total price = item price
        - stock is unlimited
            (doesn't decrease when user "purchases")
    
    
    3. Perishable
        - expiration data attribute
        - method to check if product is expired based on todays date
            - if expired
                - DO NOT change stock
                - tell user they cannot purchase item
        
        - $5 shipping BUT is total order price > 25 --> shipping free


Store Class
    - add new product methos
    - removign product by ID
    - restock existig products
    - searching for products by name
    - List all in-stock product

    
Order
    - verify if product exists
    - verify the product in stock (AND not perishable)
    - deduct appropriate quantity from inventory (not digital)
    - return order summary with total cost

"""

from datetime import datetime, date
from time import sleep


class Product:
    def __init__(self, productID, name, price ,stock_quantity):
        self.productID = productID
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity
    
    def total_price(self, quantity):
        return self.price * quantity
    
    def display(self):
        print(f"ID    : {self.productID}")
        print(f"Name  : {self.name}")
        print(f"Price : ${self.price:.2f}")
        print(f"Stock : {self.stock_quantity}")


class PhysicalProduct(Product):
    def __init__(self, productID, name, price, stock_quantity, weight, shipping_cost=5):
        super().__init__(productID, name, price, stock_quantity)
        self.weight = weight
        self.shipping_cost = shipping_cost

    def total_price(self, quantity):
        shipping = self.weight * 2.5 + self.shipping_cost
        return super().total_price(quantity) + shipping
    
    def display(self):
        super().display()
        print(f"Weight: {self.weight} kg")

class DigitalProduct(Product):
    def __init__(self, productID, name, price, stock_quantity, file_size, download_link):
        super().__init__(productID, name, price, stock_quantity)
        self.file_size = file_size
        self.download_link = download_link
    
    def total_price(self, quantity):
        return super().total_price(quantity)
    
    def display(self):
        super().display()
        print(f"File Size: {self.file_size}kb")
        print(f"Download URL: {self.download_link}")
    

class PerishableProduct(Product):
    def __init__(self, productID, name, price, stock_quantity, expiration):
        super().__init__(productID, name, price, stock_quantity)
        self.expiration = expiration
    
    def is_expired(self):
        return self.expiration < date.today()
    
    def total_price(self, quantity):
        subtot = super().total_price(quantity)
        shipping = 0 if subtot > 25 else 4.99
        return subtot + shipping

    def display(self):
        super().display()
        print(f"Expires: {self.expiration}")


class StoreError(Exception):
    pass
class ProductNotFoundError(StoreError):
    pass
class ExpiredProductError(StoreError):
    pass
class OutOfStockError(StoreError):
    pass


class Store:
    def __init__(self):
        self.products = {}
        self._counter = 0
        self.order_history = []
    

    def add_prod(self, product):
        self._counter += 1
        product.productID = f"PRD-{self._counter:05d}"
        self.products[product.productID] = product

    def remove_product(self, productID):
        if productID not in self.products:
            raise ProductNotFoundError(f"Sorry! No product with ID {productID} found... Unable to remove product.")

        self.products.pop(productID)
    
    def restock(self, productID, amount):
        if amount <= 0:
            raise ValueError("Cannot restock that amount. Please enter a positive number.")
        
        if productID not in self.products:
            raise ProductNotFoundError(f"Sorry! No product with ID {productID} found... Unable to restock product.")
        
        self.products[productID].stock_quantity += amount

    def search(self, query):
        res = []
        for product in self.products.values():
            if query.lower() in product.name.lower():
                res.append(product)
        
        return res
    
    def list_in_stock(self):
        for id, prod in self.products.items():
            if prod.stock_quantity > 0:
                print(f"ID: {id}  |  {prod.name}  |  ${prod.price:.2f} | Quantity: {prod.stock_quantity}")
        
    def place_order(self, productID, quantity):
        if productID not in self.products:
            raise ProductNotFoundError(f"Sorry! No product with ID {productID}")
        product = self.products[productID]

        # check if a product is expired
        if isinstance(product, PerishableProduct) and product.is_expired():
            raise ExpiredProductError(f"{product.name} has expired and cannot be ordered.")

        if not isinstance(product, DigitalProduct):
            if product.stock_quantity < 0:
                raise OutOfStockError(f"Sorry! {product.name} is currently out of Stock")
            
            if quantity > product.stock_quantity:
                raise OutOfStockError(f"Sorry! We only have {product.stock_quantity} items left in stock for {product.name}.")
        
            product.stock_quantity -= quantity

        total = product.total_price(quantity)
        order = Order(product, quantity, total)
        self.order_history.append(order)

        # return {
        #     "name": product.name,
        #     "quantity": quantity,
        #     "unit_price": product.price,
        #     "total": total,
        #     "remaining_stock": product.stock_quantity,
        # }
        return order
    
    def view_history(self):
        if not self.order_history:
            print("No orders placed yet.")
            return
        for order in self.order_history:
            order.display()


class Order:
    def __init__(self, product, quantity, total):
        self.product_name = product.name
        self.product = product
        self.quantity = quantity
        self.total = total
        self.timestamp = datetime.now()     # to track order history

    
    def display(self):
        stamp = self.timestamp.strftime("%Y-%m-%d %H:%M")
        print(f"[{stamp}] {self.product_name} x{self.quantity} — ${self.total:.2f}")


def clear_console():
    print("\033[2J\033[H", end="", flush=True)


def print_order_summary(order):
    product = order.product
    unit = product.price
    qty = order.quantity
    subtotal = unit * qty
    shipping = order.total - subtotal

    print("\n" + "=" * 30)
    print("       Order Summary")
    print("=" * 30)
    print(f"  {order.product_name} x{qty}")
    print(f"  Unit Price : ${unit:.2f}")
    print(f"  Subtotal   : ${subtotal:.2f}")
    print(f"  Shipping   : ${shipping:.2f}")
    print("  " + "-" * 21)
    print(f"  Total      : ${order.total:.2f}")
    print("=" * 30)
    if not isinstance(product, DigitalProduct):
        print(f"Order placed! Remaining stock: {product.stock_quantity}")


def main():
    store = Store()

    while True:
        clear_console()
        print("_____________________")
        print("Online Store Menu:")
        print("_____________________")

        print("[1] Manager Menu")
        print("[2] Customer Menu")
        print("[3] Quit")

        print("Please select an option from above.")

        try:
            user_choice = int(input("> "))
        except ValueError:
            print("Please enter a number.")
            continue

        if user_choice == 1:
            while True: 
                clear_console()

                print("--- Manager Menu ---")
                print("[1] Add product")
                print("[2] Remove product")
                print("[3] Restock product")
                print("[4] List all inventory")
                print("[5] Back")

                print("Please select an option from above.")

                try:
                    main_menu = int(input("> "))
                except ValueError:
                    print("Please enter a number.")
                    continue

                if main_menu == 5:
                    break

                elif main_menu == 1:
                    while True:
                        print("--- Product Options ---")
                        print("[1] Physical")
                        print("[2] Digital")
                        print("[3] Perishable")
                        print("[4] Back")

                        try:
                            manager_add = int(input("> "))
                        except ValueError:
                            print("Please enter a number.")
                            continue

                        if manager_add == 1:
                            prod_name = input("Name: ")
                            try:
                                prod_price = float(input("Price: "))
                            except ValueError:
                                print("Enter a valid price in decimals!")
                                continue
                            
                            try:
                                prod_stock = int(input("Stock quantity: "))
                            except ValueError:
                                print("Product stock has to be a valid whole number")
                                continue
                            
                            try:
                                prod_weight = float(input("Product Weight: "))
                            except ValueError:
                                print("Product weight has to be a valid number in decimals.")
                                continue

                            product = PhysicalProduct(None, prod_name, prod_price, prod_stock, prod_weight)
                            store.add_prod(product)

                            print(f"\nAdded! {product.name} is now {product.productID}")
                            input("Press Enter to continue...")
                            break


                        elif manager_add == 2:
                            fname = input("File name: ")
                            
                            try:
                                fprice = float(input("Price: "))
                            except ValueError:
                                print("Enter a valid price in decimals!")
                                continue

                            try:
                                fsize = int(input("File Size (kb): "))
                            except ValueError:
                                print("Enter a valid size in kilobytes!")
                                continue

                            url = input("URL: ")

                            # def __init__(self, productID, name, price, stock_quantity, file_size, download_link):
                            product = DigitalProduct(None, fname, fprice, 999999, fsize, url)
                            store.add_prod(product)
                            
                            print(f"\nAdded! {product.name} is now {product.productID}")
                            input("Press Enter to continue...")
                            break

                        
                        elif manager_add == 3:
                            pname = input("Name: ")
                            try:
                                pprice = float(input("Price: "))
                            except ValueError:
                                print("Enter a valid price!")
                                continue
                            try:
                                pstock = int(input("Stock quantity: "))
                            except ValueError:
                                print("Stock must be a whole number!")
                                continue

                            while True:
                                raw = input("Expiration date (YYYY-MM-DD): ")
                                try:
                                    expiration = datetime.strptime(raw, "%Y-%m-%d").date()
                                    break
                                except ValueError:
                                    print("Please enter a valid date (YYYY-MM-DD).")

                            product = PerishableProduct(None, pname, pprice, pstock, expiration)
                            store.add_prod(product)
                            
                            print(f"\nAdded! {product.name} is now {product.productID}")
                            input("Press Enter to continue...")
                            break



                elif main_menu == 2:
                    clear_console()
                    store.list_in_stock()
                    pid = input("\nEnter the product ID to remove: ").strip().upper()
                    try:
                        store.remove_product(pid)
                        print(f"{pid} had been removed.")
                    except StoreError as e:
                        print(e)
                    input("Press Enter to continue...")

                elif main_menu == 3:
                    clear_console()
                    store.list_in_stock()
                    pid = input("\nEnter the product ID to restock: ").strip().upper()
                    try:
                        amount = int(input("Amount to add: "))
                        store.restock(pid, amount)
                        print(f"{pid} had been restocked.")
                    except ValueError:
                        print("Amount must be a whole number.")
                    except StoreError as e:
                        print(e)
                    input("Press Enter to continue...")

                elif main_menu == 4:
                    clear_console()
                    store.list_in_stock()
                    input("\nPress Enter to continue...")
                
        elif user_choice == 2:
            while True:
                clear_console()
                print("--- Customer Menu ---")
                print("[1] Browse all products")
                print("[2] Search by name")
                print("[3] Place an order")
                print("[4] Back")

                try:
                    cust_choice = int(input("> "))
                except ValueError:
                    print("Please enter a number.")
                    continue

                if cust_choice == 4:
                    print("Alright. Taking you back to the main menu...")
                    sleep(2)
                    break

                elif cust_choice == 1:
                    clear_console()
                    store.list_in_stock()
                    input("\nPress Enter to continue...")

                elif cust_choice == 2:
                    clear_console()
                    query = input("Search: ").strip()
                    results = store.search(query)
                    if not results:
                        print("No products matched.")
                    else:
                        print("\nResults:")
                        for prod in results:
                            print(f"  [{prod.productID}]  {prod.name}  |  ${prod.price:.2f}  |  In Stock: {prod.stock_quantity}")
                    input("\nPress Enter to continue...")

                elif cust_choice == 3:
                    clear_console()
                    store.list_in_stock()
                    pid = input("\nProduct ID: ").strip().upper()
                    try:
                        qty = int(input("Quantity: "))
                        order = store.place_order(pid, qty)
                        print_order_summary(order)
                    except ValueError:
                        print("Quantity must be a whole number.")
                    except StoreError as e:
                        print(f"\nError: {e}")
                    input("\nPress Enter to continue...")

        elif user_choice == 3:
            clear_console()
            print("Thanks for visiting! Byee")
            break



if __name__ == "__main__":
    main()