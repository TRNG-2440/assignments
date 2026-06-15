from abc import ABC, abstractmethod
from datetime import date

# Menu options Dicts
main_menu_text ="----------------------------\n" \
                "- Pystore Inventory System -\n" \
                "----------------------------\n"
main_menu_options = {0: "Quit", 1: "Manager Menu", 2: "Customer Menu"}

manager_menu_text = "\n----- Manager Menu ------"
manager_menu_options = {0: "Exit", 1: "Add Product", 2: "Remove Product", 3: "Restock Product", 4: "List All Inventory"}

customer_menu_text = "\n----- Customer Menu ------"
customer_menu_options = {0: "Exit", 1: "Browse all products", 2: "Search by name", 3: "Place an order"}

product_type_menu = "\nProduct Type:"
product_type_options = {1: "Physical", 2: "Digital", 3: "Perishable"}



###################################
# Custom items to help with Menus #
###################################

class MenuMachine():
    def __printOptions(self, menu_dict:dict):
        for key in menu_dict:
            print(f"[{key}] {menu_dict[key]}")
    
    def __validateUserInput(self, user_input, options:dict):
        try:
            user_input = int(user_input)
            return user_input in options
        except ValueError:
            return False

    def menu_with_input(self, menu_title:str, menu_dict:dict):
        while True:
            print(menu_title)
            self.__printOptions(menu_dict)
            user_in = input(f"\n>")
            hasUserInputValidOption = self.__validateUserInput(user_in, menu_dict)
            if hasUserInputValidOption == True:
                return int(user_in)
            else:
                print("Please input a valid option from the menu.")

###################################
# Required Classes for Assignment #
###################################
class Product(ABC):
    def __init__(self, product_id, name, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity

    def displayProductDetails(self):
        return {
            "Product ID": self.product_id,
            "Name": self.name,
            "Price": self.price,
            "Stock Quantity": self.stock_quantity
        }

    def calculateTotalPrice(self, quantity):
        return self.price * quantity

    def reduceStock(self, quantity):
        if quantity > self.stock_quantity:
            raise ValueError("Insufficient stock")
        self.stock_quantity -= quantity

class PhysicalProduct(Product):
    
    def __init__(self, product_id, name, price, stock_quantity, weight):
        super().__init__(product_id, name, price, stock_quantity)
        self.weight = weight
        self.shipping_rate_per_pound = 1.50

    def calculateShippingCost(self, quantity):
        return self.weight * quantity * self.shipping_rate_per_pound

    def calculateTotalPrice(self, quantity):
        subtotal = super().calculateTotalPrice(quantity)
        shipping = self.calculateShippingCost(quantity)
        return subtotal + shipping

    def displayProductDetails(self):
        details = super().displayProductDetails()
        details["Weight"] = self.weight
        return details

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock_quantity, file_size, download_url):
        super().__init__(product_id, name, price, stock_quantity)
        self.file_size = file_size
        self.download_url = download_url

    def calculateTotalPrice(self, quantity):
        return self.price * quantity

    def reduceStock(self, quantity):
        pass

    def displayProductDetails(self):
        details = super().displayProductDetails()
        details["File Size"] = self.file_size
        details["Download URL"] = self.download_url
        return details

class PerishableProduct(Product):
    flat_rate_shipping = 5.00
    free_shipping_threshold = 25.00

    def __init__( self, product_id, name, price, stock_quantity, expiration_date
    ):
        super().__init__(product_id, name, price, stock_quantity)
        self.expiration_date = expiration_date
        
    def isExpired(self):
        return date.today() > self.expiration_date

    def calculateShippingCost(self, quantity):
        subtotal = self.price * quantity
        if subtotal > self.free_shipping_threshold:
            print("Your are getting Free shipping!")
            return 0.0
        print(f"Flat shipping rate of ${self.flat_rate_shipping} applied!")
        return self.flat_rate_shipping

    def calculateTotalPrice(self, quantity):
        if self.isExpired():
            raise ValueError("Cannot order expired products")

        subtotal = self.price * quantity
        shipping = self.calculateShippingCost(quantity)

        return subtotal + shipping

    def reduceStock(self, quantity):
        super().reduceStock(quantity)

    def displayProductDetails(self):
        details = super().displayProductDetails()
        details["Expiration Date"] = self.expiration_date
        details["Expired"] = self.isExpired()
        return details

class Store():
    def __init__(self):
        self.products = []
        self.current_product_num = 1
        
    def generateProductId(self, prefix):
        product_id = f"{prefix}-{self.current_product_num:05d}"
        self.current_product_num += 1
        return product_id
    
    def addProduct(self, product):
        self.products.append(product)

    def removeProduct(self, product_id):
        for product in self.products:
            if product.product_id.lower() == product_id.lower():
                self.products.remove(product)
                print(f"Item with Product ID: {product.product_id} deleted")
                return
        raise ValueError(f"Product ID {product_id} not found")

    def restockProduct(self, product_id, quantity):
        if quantity <= 0:
            raise ValueError("Restock quantity must be positive")
        product = self.getProductById(product_id)
        product.stock_quantity += quantity

    def searchProductsByName(self, search_term):
        matches = []
        search_term = search_term.lower()
        for product in self.products:
            if search_term in product.name.lower():
                matches.append(product)
        return matches

    def listInStockProducts(self):
        in_stock = []
        for product in self.products:
            if product.stock_quantity > 0:
                in_stock.append(product)
        return in_stock

    def getProductById(self, product_id):
        for product in self.products:
            if product.product_id.lower() == product_id.lower():
                return product
        raise ValueError(f"Product ID {product_id} not found")

# This will act as main
def orderSystem():
    menu_printer = MenuMachine()
    PyStore = Store()
    while True:
        user_input = menu_printer.menu_with_input(main_menu_text, main_menu_options)
        if user_input == 1: # Manager Menu
            while True:
                user_input = menu_printer.menu_with_input(
                    manager_menu_text,
                    manager_menu_options
                )

                if user_input == 0:  # Exit manager menu
                    break

                elif user_input == 1:  # Add Product
                    try:
                        product_type = menu_printer.menu_with_input(
                            product_type_menu,
                            product_type_options
                        )

                        name = input("Product Name: ")
                        price = float(input("Price: "))
                        stock = int(input("Stock Quantity: "))

                        if product_type == 1:  # Physical
                            weight = float(input("Weight: "))

                            PyStore.addProduct(
                                PhysicalProduct(
                                    PyStore.generateProductId("PHY"),
                                    name,
                                    price,
                                    stock,
                                    weight
                                )
                            )

                        elif product_type == 2:  # Digital
                            file_size = input("File Size: ")
                            download_url = input("Download URL: ")

                            PyStore.addProduct(
                                DigitalProduct(
                                    PyStore.generateProductId("DIG"),
                                    name,
                                    price,
                                    stock,
                                    file_size,
                                    download_url
                                )
                            )

                        elif product_type == 3:  # Perishable
                            expiration_input = input(
                                "Expiration Date (YYYY-MM-DD): "
                            )

                            expiration_date = date.fromisoformat(expiration_input)

                            PyStore.addProduct(
                                PerishableProduct(
                                    PyStore.generateProductId("PER"),
                                    name,
                                    price,
                                    stock,
                                    expiration_date
                                )
                            )

                    except ValueError as e:
                        print(f"Error: {e}")

                elif user_input == 2:  # Remove Product
                    try:
                        product_id = input("Enter Product ID: ")
                        PyStore.removeProduct(product_id)

                    except ValueError as e:
                        print(f"Error: {e}")

                elif user_input == 3:  # Restock Product
                    try:
                        product_id = input("Enter Product ID: ")
                        quantity = int(input("Quantity to add: "))

                        PyStore.restockProduct(product_id, quantity)

                    except ValueError as e:
                        print(f"Error: {e}")

                elif user_input == 4:  # List Inventory
                    products = PyStore.products

                    if not products:
                        print("No products in inventory.")
                    else:
                        for product in products:
                            details = product.displayProductDetails()
                            print("\n----------------------")
                            for k, v in details.items():
                                print(f"{k}: {v}")
                            print("----------------------")
        elif user_input == 2: # Customer Menu
            while True:
                user_input = menu_printer.menu_with_input(
                    customer_menu_text,
                    customer_menu_options
                )

                if user_input == 0:  # Exit customer menu
                    break

                elif user_input == 1:  # Browse all products
                    products = PyStore.products

                    if not products:
                        print("No products available.")
                    else:
                        for product in products:
                            details = product.displayProductDetails()
                            print("\n----------------------")
                            for k, v in details.items():
                                print(f"{k}: {v}")
                            print("----------------------")

                elif user_input == 2:  # Search by name
                    search_term = input("Enter search term: ")
                    results = PyStore.searchProductsByName(search_term)

                    if not results:
                        print("No matching products found.")
                    else:
                        for product in results:
                            details = product.displayProductDetails()
                            print("\n----------------------")
                            for k, v in details.items():
                                print(f"{k}: {v}")
                            print("----------------------")

                elif user_input == 3:  # Place an order
                    try:
                        product_id = input("Enter Product ID: ")
                        quantity = int(input("Quantity: "))

                        product = PyStore.getProductById(product_id)
                        
                        if quantity <= 0:
                            print("Quantity must be greater than 0.")
                            continue

                        if isinstance(product, DigitalProduct):
                            total_price = product.calculateTotalPrice(quantity)
                            print(f"Order placed. Total: ${total_price:.2f}")
                            print(f"Download: {product.download_url}")
                            continue

                        if product.stock_quantity < quantity:
                            print("Error: Not enough stock available.")
                            continue

                        if isinstance(product, PerishableProduct) and product.isExpired():
                            print("Error: Cannot order expired products.")
                            continue

                        else:
                            product.reduceStock(quantity)
                            total_price = product.calculateTotalPrice(quantity)
                            print(f"Order placed. Total: ${total_price:.2f}")

                    except ValueError as e:
                        print(f"Error: {e}")
        elif user_input == 0: # Exit
            break
        else:
            print("Invalid Input!!!") # Note, it should not reach here, as menu machine should filter for valid inputs
            

# Run main            
orderSystem()