from datetime import datetime
from abc import ABC, abstractmethod
import json

class Product(ABC):
    def __init__(self, prod_id, name, price, quantity):
        self.prod_id = prod_id
        self.name = name
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def DisplayDetails(self):
        pass

    @abstractmethod
    def TotalPriceCalc(self):
        pass

    def ApplyDiscount(self, p):
        discounted = round((p / 100) * self.price, 2)
        self.price = round(self.price - discounted, 2)

class PhysicalProduct(Product):
    def __init__(self, prod_id, name, price, quantity, weight):
        super().__init__(prod_id, name, price, quantity)
        self.weight = weight

    def DisplayDetails(self):
        print(f" [{self.prod_id}] {self.name}, ${self.price:.2f}, {self.quantity} in stock, {self.weight} lbs")
    
    # shipping cost scales with weight
    def TotalPriceCalc(self):
        inp = input("Enter amount to buy: ")
        try:
            amount = int(inp)
        except ValueError:
            raise ValueError("Amount must be a whole number.")
        if amount <= 0: raise ValueError("Amount must be greater than 0.")
        elif self.quantity - amount < 0: raise ValueError("Amount exceeds current stock.")

        self.quantity -= amount
        subtotal = round(amount * self.price, 2)
        shipping = round(5 * self.weight, 2)
        total = round(subtotal + shipping, 2)
        print("==============================")
        print("        ORDER SUMMARY         ")
        print("==============================")
        print(f" {self.name} x{amount}")
        print(f" Unit Price : ${self.price:.2f}")
        print(f" Subtotal   : ${subtotal:.2f}")
        print(f" Shipping   : ${shipping:.2f} ({self.weight} lbs)")
        print("------------------------------")
        print(f" Total      : ${total:.2f}")
        return [self.name, amount, total, str(datetime.now())]

class DigitalProduct(Product):
    def __init__(self, prod_id, name, price, quantity, filesize, URL):
        super().__init__(prod_id, name, price, quantity)
        self.filesize = filesize
        self.URL = URL

    def DisplayDetails(self):
        print(f" [{self.prod_id}] {self.name}, ${self.price:.2f}, {self.quantity} in stock, {self.filesize} GB, {self.URL}")

    # quantity doesn't decrease, no shipping cost
    def TotalPriceCalc(self):
        inp = input("Enter amount to buy: ")
        try:
            amount = int(inp)
        except ValueError:
            raise ValueError("Amount must be a whole number.")
        if amount <= 0: raise ValueError("Amount must be greater than 0.")

        subtotal = round(amount * self.price, 2)
        print("==============================")
        print("        ORDER SUMMARY         ")
        print("==============================")
        print(f" {self.name} x{amount}")
        print(f" Unit Price : ${self.price:.2f}")
        print(f" Subtotal   : ${subtotal:.2f}")
        print(f" Shipping   : $0.00")
        print("------------------------------")
        print(f" Total      : ${subtotal:.2f}")
        return [self.name, amount, subtotal, str(datetime.now())]

class PerishableProduct(Product):
    def __init__(self, prod_id, name, price, quantity, expiration):
        super().__init__(prod_id, name, price, quantity)
        self.expiration = expiration

    def DisplayDetails(self):
        print(f" [{self.prod_id}] {self.name}, {self.price:.2f}, {self.quantity} in stock, Expires {self.expiration}")

    # checks before buying item, cannot buy if expired
    def ExpirationCheck(self):
        date = datetime.strptime(self.expiration, "%Y-%m-%d")
        if date.date() < datetime.today().date():
            raise ValueError(f"Product {self.prod_id} is expired.")
    
    # flat shipping rate, free if > $25.00
    def TotalPriceCalc(self):
        try:
            self.ExpirationCheck()
        except ValueError as e:
            raise ValueError(e)
        
        inp = input("Enter amount to buy: ")
        try:
            amount = int(inp)
        except ValueError:
            raise ValueError("Amount must be a whole number.")
        if amount <= 0: raise ValueError("Amount must be greater than 0.")
        elif self.quantity - amount < 0: raise ValueError("Amount exceeds current stock.")

        self.quantity -= amount
        subtotal = round(amount * self.price, 2)
        if subtotal >= 25: shipping = 0
        else: shipping = 3.99
        total = round(subtotal + shipping, 2)
        print("==============================")
        print("        ORDER SUMMARY         ")
        print("==============================")
        print(f" {self.name} x{amount}")
        print(f" Unit Price : ${self.price:.2f}")
        print(f" Subtotal   : ${subtotal:.2f}")
        if shipping == 0:
            print(f" Shipping   : $0.00 (Free Shipping)")
        else:
            print(f" Shipping   : ${shipping:.2f}")
        print("------------------------------")
        print(f" Total      : ${total:.2f}")
        return [self.name, amount, total, str(datetime.now())]

class Store:
    def __init__(self):
        self.inventory = []
        self.history = []
        self.curr_prod = 0

    # prod_id generator
    def CreateID(self):
        s = f"PRD-{self.curr_prod:05d}"
        self.curr_prod += 1
        return s

    # add products
    def AddPhysical(self):
        n = input("Name: ")
        inp_p = input("Price: ")
        try:
            p = round(float(inp_p), 2)
        except ValueError:
            raise ValueError("Price needs to be a number.")
        if p <= 0: raise ValueError("Price must be greater than 0.")
        inp_q = input("Quantity: ")
        try:
            q = int(inp_q)
        except ValueError:
            raise ValueError("Quantity needs to be a whole number.")
        if q <= 0: raise ValueError("Quantity must be at least 1.")
        inp_w = input("Weight: ")
        try:
            w = round(float(inp_w), 2)
        except ValueError:
            raise ValueError("Weight needs to be a number.")
        if w <= 0: raise ValueError("Weight must be greater than 0.")
        
        prod_id = self.CreateID()
        item = PhysicalProduct(prod_id, n, p, q, w)
        self.inventory.append(item)
        print(f"Successfully added item with id: {prod_id}.")
    
    def AddDigital(self):
        n = input("Name: ")
        inp_p = input("Price: ")
        try:
            p = round(float(inp_p), 2)
        except ValueError:
            raise ValueError("Price needs to be a number.")
        if p <= 0: raise ValueError("Price must be greater than 0.")
        inp_q = input("Quantity: ")
        try:
            q = int(inp_q)
        except ValueError:
            raise ValueError("Quantity needs to be a whole number.")
        if q <= 0: raise ValueError("Quantity must be at least 1.")
        inp_f = input("Filesize in GB: ")
        try:
            fs = round(float(inp_f), 2)
        except ValueError:
            raise ValueError("Filesize needs to be a number.")
        if fs <= 0: raise ValueError("Filesize must be greater than 0.")
        URL = input("URL: ")

        prod_id = self.CreateID()
        item = DigitalProduct(prod_id, n, p, q, fs, URL)
        self.inventory.append(item)
        print(f"Successfully added item with id: {prod_id}.")

    def AddPerishable(self):
        n = input("Name: ")
        inp_p = input("Price: ")
        try:
            p = round(float(inp_p), 2)
        except ValueError:
            raise ValueError("Price needs to be a number.")
        if p <= 0: raise ValueError("Price must be greater than 0.")
        inp_q = input("Quantity: ")
        try:
            q = int(inp_q)
        except ValueError:
            raise ValueError("Quantity needs to be a whole number.")
        if q <= 0: raise ValueError("Quantity must be at least 1.")
        d = input("Expiration date (YYYY-MM-DD): ")
        try:
            datetime.strptime(d, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError("Expiration needs to be a date.")
        
        prod_id = self.CreateID()
        item = PerishableProduct(prod_id, n, p, q, d)
        self.inventory.append(item)
        print(f"Successfully added item with id: {prod_id}.")

    def RemoveProduct(self):
        if not self.inventory:
            raise LookupError("No products being sold.")
        
        prod_id = input("Enter the prod_id of the product to delete: ")
        for item in self.inventory:
            if item.prod_id == prod_id:
                self.inventory.remove(item)
                print(f"{prod_id} successfully deleted.")
                return
        raise LookupError(f"Product {prod_id} not found.")

    def DiscountCategory(self, category):
        if not self.inventory:
            raise LookupError("No products being sold.")
        
        percent = input("Enter a percentage to discount (1-100): ")
        try:
            p = round(float(percent), 2)
        except ValueError:
            raise ValueError("Percentage must be a number.")
        if p < 1 or p > 100: raise ValueError("Percentage must be between 1 to 100.")

        counter = 0
        for item in self.inventory:
            if isinstance(item, category):
                item.ApplyDiscount(p)
                counter += 1
        
        if counter == 0: print("No products discounted.")
        elif category == PhysicalProduct: print("Successfully discounted \"physical products\".")
        elif category == DigitalProduct: print("Successfully discounted \"digital products\".")
        elif category == PerishableProduct: print("Successfully discounted \"perishable products\".")

    def LowStock(self):
        if not self.inventory:
            raise LookupError("No products being sold.")
        
        counter = 0
        for item in self.inventory:
            if item.quantity <= 5:
                if counter == 0:
                    print("==============================")
                    print("       LOW STOCK ITEMS        ")
                    print("==============================")
                item.DisplayDetails()
                counter += 1
        print("==============================")
        print(f"Printed {counter} low stock item(s).")

    def RestockProduct(self):
        if not self.inventory:
            raise LookupError("No products being sold.")
        prod_id = input("Enter a product to restock: ")
        inp_a = input("Enter an amount to restock with: ")
        try:
            amount = int(inp_a)
        except ValueError:
            raise ValueError("Amount needs to be a number.") 
        if amount <= 0:
            raise ValueError("Amount cannot be 0 or negative.")
        for item in self.inventory:
            if item.prod_id == prod_id:
                item.quantity += amount
                print(f"Successfully restocked {prod_id} with {amount} items. Total: {item.quantity}")
                return   
        raise LookupError(f"Product {prod_id} not found.")

    def LookupProduct(self):
        name = input("Enter the name of the product to search: ").lower()
        if not self.inventory:
            raise LookupError("No products being sold.")
        counter = 1
        for item in self.inventory:
            if name in item.name.lower():
                if counter == 1:
                    print("==============================")
                    print("           PRODUCTS           ")
                    print("==============================")
                item.DisplayDetails()
                counter += 1
        print("==============================")
        if counter == 1:
            raise LookupError("No matching products found.")
        else: print(f"{counter - 1} matching products found.")

    def ListAllProducts(self):
        if not self.inventory:
            raise LookupError("No products being sold.")
        print("==============================")
        print("           PRODUCTS           ")
        print("==============================")
        for item in self.inventory:
            item.DisplayDetails()
        print("==============================")
        print(f"Printed {len(self.inventory)} item(s).")

    def LookupToBuy(self):
        inp = input("Enter product ID of item to buy: ")
        for item in self.inventory:
            if item.prod_id == inp:
                try:
                    self.history.append(item.TotalPriceCalc())
                except ValueError as e:
                    raise ValueError(e)
                return
        raise LookupError(f"Product {inp} not found.")

    def ExpirationSweep(self):
        if not self.inventory:
            raise LookupError("No products being sold.")
        
        copy = self.inventory.copy()
        counter = 0
        for item in copy:
            if isinstance(item, PerishableProduct):
                date = datetime.strptime(item.expiration, "%Y-%m-%d")
                if date.date() < datetime.today().date():
                    self.inventory.remove(item)
                    print(f"{item.prod_id} successfully deleted.")
                    counter += 1
        if counter == 0: raise LookupError(f"No expired products found.")
        else: print(f"Successfully deleted {counter} expired products.")

    def ViewHistory(self):
        if not self.history: raise LookupError("Order history does not exist.")

        for h in self.history:
            print(f"{h[0]}, {h[1]} items, ${h[2]:.2f}, DATE/TIME: {h[3]}")
        print(f"Sucessfully printed {len(self.history)} orders.")

    def SaveData(self, filename="store_data.json"):
        data = {
            "products": [],
            "history": self.history
        }

        for p in self.inventory:
            p_data = {
                "prod_id": p.prod_id,
                "name": p.name,
                "price": p.price,
                "quantity": p.quantity,
            }

            if isinstance(p, PhysicalProduct):
                p_data["weight"] = p.weight
            elif isinstance(p, DigitalProduct):
                p_data["filesize"] = p.filesize
                p_data["URL"] = p.URL
            elif isinstance(p, PerishableProduct):
                p_data["expiration"] = p.expiration
            data["products"].append(p_data)

        with open(filename, "w") as file:
            json.dump(data, file)

    def LoadData(self, filename="store_data.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"{filename} does not exist.")
        
        self.inventory = []
        self.history = data["history"]

        for p in data["products"]:
            if "weight" in p:
                item = PhysicalProduct(p["prod_id"], p["name"], p["price"], p["quantity"], p["weight"])
            elif "filesize" in p:
                item = DigitalProduct(p["prod_id"], p["name"], p["price"], p["quantity"], p["filesize"], p["URL"])
            elif "expiration" in p:
                item = PerishableProduct(p["prod_id"], p["name"], p["price"], p["quantity"], p["expiration"])
            self.inventory.append(item)

def CLIMenu():
    store = Store()
    try:
        store.LoadData()
    except FileNotFoundError as e:
        print(f"Error: {e}")

    while True:
        print("==============================")
        print("       Inventory System       ")
        print("==============================")
        print(" [1] Manager Menu")
        print(" [2] Customer Menu")
        print(" [3] Quit")
        inp = input("Enter an option to proceed (1, 2, or 3): ")

        match inp:
            case "1":
                while True:
                    print("==============================")
                    print("         Manager Menu         ")
                    print("==============================")
                    print(" [1] Add product")
                    print(" [2] Remove product")
                    print(" [3] Restock product")
                    print(" [4] List all inventory")
                    print(" [5] Discount System")
                    print(" [6] Expiration Sweep")
                    print(" [7] Low stock alerts")
                    print(" [8] Back")
                    inp = input("Enter an option to proceed (1, 2, 3, 4, 5, 6, 7, or 8): ")

                    match inp:
                        case "1":
                            print("==============================")
                            print("         PRODUCT TYPE         ")
                            print("==============================")
                            print(" [1] Physical")
                            print(" [2] Digital")
                            print(" [3] Perishable")
                            inp = input("Enter an option to proceed (1, 2, or 3): ")

                            match inp:
                                case "1":
                                    try:
                                        store.AddPhysical()
                                    except ValueError as e:
                                        print(f"Error: {e}")
                                case "2":
                                    try:
                                        store.AddDigital()
                                    except ValueError as e:
                                        print(f"Error: {e}")
                                case "3":
                                    try:
                                        store.AddPerishable()
                                    except ValueError as e:
                                        print(f"Error: {e}")
                        case "2":
                            try:
                                store.RemoveProduct()
                            except (LookupError, ValueError) as e:
                                print(f"Error: {e}")
                        case "3":
                            try:
                                store.RestockProduct()
                            except (LookupError, ValueError) as e:
                                print(f"Error: {e}")
                        case "4":
                            try:
                                store.ListAllProducts()
                            except LookupError as e:
                                print(f"Error: {e}")
                        case "5":
                            print("==============================")
                            print("        APPLY DISCOUNT        ")
                            print("==============================")
                            print(" [1] Physical")
                            print(" [2] Digital")
                            print(" [3] Perishable")
                            inp = input("Enter an option to proceed (1, 2, or 3): ")

                            match inp:
                                case "1":
                                    try: 
                                        store.DiscountCategory(PhysicalProduct)
                                    except (LookupError, ValueError) as e:
                                        print(f"Error: {e}")
                                case "2":
                                    try: 
                                        store.DiscountCategory(DigitalProduct)
                                    except (LookupError, ValueError) as e:
                                        print(f"Error: {e}")
                                case "3":
                                    try: 
                                        store.DiscountCategory(PerishableProduct)
                                    except (LookupError, ValueError) as e:
                                        print(f"Error: {e}")
                        case "6":
                            try:
                                store.ExpirationSweep()
                            except (LookupError, ValueError) as e:
                                print(f"Error: {e}")
                        case "7":
                            try:
                                store.LowStock()
                            except LookupError as e:
                                print(f"Error: {e}")
                        case "8":
                            print("Store saved successfully.")
                            break
            case "2":
                while True:
                    print("==============================")
                    print("        Customer Menu         ")
                    print("==============================")
                    print(" [1] Browse all products")
                    print(" [2] Search by name")
                    print(" [3] Place an order")
                    print(" [4] Order History")
                    print(" [5] Back")
                    inp = input("Enter an option to proceed (1, 2, 3, or 4): ")

                    match inp:
                        case "1":
                            try:
                                store.ListAllProducts()
                            except LookupError as e:
                                print(f"Error: {e}")
                        case "2":
                            try:
                                store.LookupProduct()
                            except LookupError as e:
                                print(f"Error: {e}")
                        case "3":
                            try:
                                store.LookupToBuy()
                            except (LookupError, ValueError) as e:
                                print(f"Error: {e}")
                        case "4":
                            try:
                                store.ViewHistory()
                            except LookupError as e:
                                print(f"Error: {e}")
                        case "5":
                            print("Thank you for shopping with us!")
                            break
            case "3":
                print("Thank you for visiting. Exiting application.")
                store.SaveData()
                break

CLIMenu()