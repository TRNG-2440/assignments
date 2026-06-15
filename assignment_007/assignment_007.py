# Assignment 7 by Ariyan Shaikh

from datetime import datetime
import random

class Product:
    """
    Product base class used to implement.
    Phisical product, Digital produce and perishiable product
    This is an abstract class.
    """
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity
    
    def display_product_details(self) -> None:
        """
        Prints product all product attributes
        """
        print(f"Product ID: {self.product_id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self.price:.2f}")
        print(f"Stock quantity: {self.stock_quantity}")
    
    def get_price(self, quantity: int) -> float:
        """
        This function takes a quantity as an int parm and returns the total price for that amount
        """
        return round(self.price * quantity, 2)

class PhysicalProduct(Product):
    """
    Subclass of Product, unique attributes: weight and cost per lb
    """
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, weight: float, cost_per_lb: float):
        super().__init__(product_id, name, price, stock_quantity)
        self.weight = weight
        self.cost_per_lb = cost_per_lb

    def display_product_details(self) -> None:
        """
        Overrides the display method to include unique attributes
        """
        print(f"[{self.product_id}] {self.name} | Price: ${self.price:.2f} | Stock: {self.stock_quantity} | Weight: {self.weight} lbs")

    def get_price(self, quantity: int) -> float:
        """
        Takes weight and quantity and returns a total price with shipping cost included
        """
        base_price = self.price * quantity
        shipping = self.get_shipping(quantity)
        return round(base_price + shipping, 2)
    
    def get_shipping(self, quantity: int) -> float:
        """
        Takes quantity and returns shipping cost
        """
        return round(self.weight * self.cost_per_lb * quantity, 2)

class DigitalProduct(Product):
    """
    Subclass of Product, unique attributes: file size and download URL
    """
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, file_size: int, download_url: str):
        super().__init__(product_id, name, price, stock_quantity)
        self.file_size = file_size
        self.download_url = download_url
    
    def display_product_details(self) -> None:
        """
        Overrides the display method to include unique attributes
        """
        print(f"[{self.product_id}] {self.name} | Price: ${self.price:.2f} | Stock: Infinite | Size: {self.file_size}MB")

    def get_price(self, quantity: int) -> float:
        """
        Takes quantity parameter and returns the base price total without shipping.
        """
        return round(self.price * quantity, 2)

class PerishableProduct(Product):
    """
    Subclass of Product, unique attributes: expiration date
    """
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, expiration_date: datetime):
        super().__init__(product_id, name, price, stock_quantity)
        self.expiration_date = expiration_date
    
    def display_product_details(self) -> None:
        """
        Overrides the display method to include unique attributes
        """
        date_str = self.expiration_date.strftime("%Y-%m-%d")
        print(f"[{self.product_id}] {self.name} | Price: ${self.price:.2f} | Stock: {self.stock_quantity} | Expires: {date_str}")

    def is_expired(self) -> bool:
        """
        Returns true if expired and false if not.
        """
        if self.expiration_date < datetime.now():
            return True
        return False
    
    def flat_rate(self, quantity: int) -> bool:
        """
        Returns true if flat rate shipping cost should be applied and false if not.
        """
        # Checks pre-shipping total base cost
        if (self.price * quantity) < 25.00:
            return True
        return False

class Store:
    """
    Store inventory manager class to handle inventory collections.
    """
    def __init__(self):
        self.products = []

    def generate_id(self) -> str:
        """
        Generates a unique random string product ID matching spec examples
        """
        return f"PRD-{random.randint(1000, 9999)}"
        
    def add_product(self, product: Product) -> None:
        """
        Appends a fully initialized product object to the store list
        """
        self.products.append(product)

    def remove_product(self, product_id: str) -> None:
        """
        Removes a product by ID. Raises Exception if missing.
        """
        for prod in self.products:
            if prod.product_id == product_id:
                self.products.remove(prod)
                return
        raise Exception("Product ID not found.")

    def restock_product(self, product_id: str, amount: int) -> None:
        """
        Increases existing product stock. Raises Exception if missing.
        """
        for prod in self.products:
            if prod.product_id == product_id:
                prod.stock_quantity += amount
                return
        raise Exception("Product ID not found.")

    def search_by_name(self, query: str) -> list:
        """
        Finds matching items via case-insensitive substring searching
        """
        matches = []
        for prod in self.products:
            if query.lower() in prod.name.lower():
                matches.append(prod)
        return matches


def get_selection(num_selections: int) -> int:
    """
    Collects and validates users's Selection.
    Requires the number of selections passed as an int paramater
    """
    while True:
        try:
            selection = int(input("> "))        
            if selection > num_selections or selection < 1:
                raise Exception("Invalid input detected")
            return selection
        except Exception as ex:
            print("\nThat is not a valid input. Please try again\n")


if __name__ == "__main__":
    store = Store()
    
    while True:
        print("=" * 30)
        print(f'{"PyStore Inventory System":^30}')
        print("=" * 30)
        print("[1] Manager Menu")
        print("[2] Customer Menu")
        print("[3] Quit")
        
        main_choice = get_selection(3)
        
        if main_choice == 3:
            print("Goodbye!")
            break
            
        elif main_choice == 1:
            while True:
                print("\n--- Manager Menu ---")
                print("[1] Add product")
                print("[2] Remove product")
                print("[3] Restock product")
                print("[4] List all inventory")
                print("[5] Back")
                
                mgr_choice = get_selection(5)
                
                if mgr_choice == 5:
                    break
                    
                elif mgr_choice == 1:
                    print("\nProduct type:")
                    print("[1] Physical")
                    print("[2] Digital")
                    print("[3] Perishable")
                    p_type = get_selection(3)
                    
                    name = input("Name: ")
                    try:
                        price = float(input("Price: "))
                        stock = int(input("Stock quantity: "))
                        p_id = store.generate_id()
                        
                        if p_type == 1:
                            weight = float(input("Weight (lbs): "))
                            cost_lb = float(input("Shipping cost per lb: "))
                            new_prod = PhysicalProduct(p_id, name, price, stock, weight, cost_lb)
                        elif p_type == 2:
                            f_size = int(input("File Size (MB): "))
                            url = input("Download URL: ")
                            new_prod = DigitalProduct(p_id, name, price, stock, f_size, url)
                        elif p_type == 3:
                            date_in = input("Expiration date (YYYY-MM-DD): ")
                            exp_date = datetime.strptime(date_in, "%Y-%m-%d")
                            new_prod = PerishableProduct(p_id, name, price, stock, exp_date)
                            
                        store.add_product(new_prod)
                        print(f"\nProduct added.")
                        new_prod.display_product_details()
                    except Exception as e:
                        print(f"\nError processing inputs: {e}. Return to menu.")
                        
                elif mgr_choice == 2:
                    rem_id = input("Product ID to remove: ")
                    try:
                        store.remove_product(rem_id)
                        print("Product successfully removed.")
                    except Exception as e:
                        print(f"Error: {e}")
                        
                elif mgr_choice == 3:
                    rest_id = input("Product ID: ")
                    try:
                        amt = int(input("Quantity to add: "))
                        store.restock_product(rest_id, amt)
                        print("Inventory restocked.")
                    except Exception as e:
                        print(f"Error: {e}")
                        
                elif mgr_choice == 4:
                    print("\n--- Current Store Inventory ---")
                    if not store.products:
                        print("Inventory is completely empty.")
                    for prod in store.products:
                        prod.display_product_details()
                        
        elif main_choice == 2:
            while True:
                print("\n--- Customer Menu ---")
                print("[1] Browse all products")
                print("[2] Search by name")
                print("[3] Place an order")
                print("[4] Back")
                
                cust_choice = get_selection(4)
                
                if cust_choice == 4:
                    break
                    
                elif cust_choice == 1:
                    print("\nAvailable Products:")
                    in_stock = [p for p in store.products if p.stock_quantity > 0 or isinstance(p, DigitalProduct)]
                    if not in_stock:
                        print("No items currently available.")
                    for prod in in_stock:
                        prod.display_product_details()
                        
                elif cust_choice == 2:
                    query = input("Search: ")
                    results = store.search_by_name(query)
                    print("\nResults:")
                    if not results:
                        print("No matching products found.")
                    for prod in results:
                        prod.display_product_details()
                        
                elif cust_choice == 3:
                    ord_id = input("Product ID: ")
                    # Locate target product
                    target_prod = None
                    for p in store.products:
                        if p.product_id == ord_id:
                            target_prod = p
                            break
                            
                    if not target_prod:
                        print("Error: That product ID does not exist.")
                        continue
                        
                    try:
                        qty = int(input("Quantity: "))
                        if qty <= 0:
                            print("Error: Quantity must be greater than zero.")
                            continue
                    except ValueError:
                        print("Error: Invalid numeric input.")
                        continue
                        
                    # Handle Validation checks
                    if isinstance(target_prod, PerishableProduct) and target_prod.is_expired():
                        print(f"Error: {target_prod.name} has expired and cannot be ordered.")
                        continue
                        
                    if not isinstance(target_prod, DigitalProduct) and target_prod.stock_quantity < qty:
                        print(f"Error: Insufficient stock. Available items: {target_prod.stock_quantity}")
                        continue
                    
                    # Cost Calculations Setup
                    subtotal = round(target_prod.price * qty, 2)
                    shipping = 0.00
                    
                    if isinstance(target_prod, PhysicalProduct):
                        shipping = target_prod.get_shipping(qty)
                    elif isinstance(target_prod, PerishableProduct):
                        if target_prod.flat_rate(qty):
                            shipping = 3.99
                            shipping_note = "(flat-rate)"
                        else:
                            shipping = 0.00
                            shipping_note = "(free over $25)"
                            
                    total_cost = round(subtotal + shipping, 2)
                    
                    # Print Order Receipt
                    print("=" * 30)
                    print(f'{"Order Summary":^30}')
                    print("=" * 30)
                    print(f"  {target_prod.name} x{qty}")
                    print(f"  Unit Price : ${target_prod.price:.2f}")
                    print(f"  Subtotal   : ${subtotal:.2f}")
                    if isinstance(target_prod, PerishableProduct):
                        print(f"  Shipping   : ${shipping:.2f}  {shipping_note}")
                    else:
                        print(f"  Shipping   : ${shipping:.2f}")
                    print("  " + "-" * 21)
                    print(f"  Total      : ${total_cost:.2f}")
                    print("=" * 30)
                    
                    # Complete order adjustment
                    if not isinstance(target_prod, DigitalProduct):
                        target_prod.stock_quantity -= qty
                        print(f"Order placed! Remaining stock: {target_prod.stock_quantity}")
                    else:
                        print("Order placed! Your download link will be emailed to you.")