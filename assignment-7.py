import uuid
import datetime as dt

class Product:
    def __init__(self, name, type_name, price=0.00, quantity=0):
        self.name = name
        self.price = price
        self.quantity = quantity

        self.type = type_name

        self.id: str = str(uuid.uuid4())

    def display_details(self):
        print("-" * 30)
        print("Product Details")
        print("-" * 30)
        print(f"ID         : {self.id}")
        print(f"Name       : {self.name}")
        print(f"Type       : {self.type}")
        print(f"Price      : ${self.price:.2f}")
        print(f"Stock      : {self.quantity}")

    def calc_total(self, quantity):
        return self.price * quantity


class PhysicalProduct(Product):
    def __init__(self, name, weight_lbs, type_name="Physical", price=0.00, quantity=0):

        super().__init__(name, type_name, price, quantity)
        self.weight_lbs = weight_lbs

    def calc_shipping_cost(self, quantity):
        return 0.50 * self.weight_lbs * quantity

    def calc_total(self, quantity):
        subtotal = super().calc_total(quantity)

        shipping = self.calc_shipping_cost(quantity)
        return subtotal + shipping

    def display_details(self):
        super().display_details()
        print(f"Weight     : {self.weight_lbs} lbs")

        print("-" * 30)


class DigitalProduct(Product):
    def __init__(self, name, file_size, url, type_name="Digital", price=0.00, quantity=0):
        super().__init__(name, type_name, price, quantity)
        self.file_size = file_size

        self.url = url

    def display_details(self):
        super().display_details()
        print(f"File Size  : {self.file_size}")

        print(f"URL        : {self.url}")
        print("-" * 30)


class PerishableProduct(Product):
    def __init__(self, name, expiration_date, type_name="Perishable", price=0.00, quantity=0):
        super().__init__(name, type_name, price, quantity)

        self.expiration_date = expiration_date

    def is_expired(self):
        return dt.date.today() > self.expiration_date

    def calc_shipping_cost(self, subtotal):
        
        if subtotal > 25.00:
            return 0.00
        else:
            return 5.00 

    def display_details(self):

        super().display_details()
        print(f"Expires    : {self.expiration_date}")

        print("-" * 30)


class Store:
    def __init__(self):
        self.inventory = {}

    def add_product(self, product):
        self.inventory[product.id] = product

        print(f"\n{product.type} product added.")
        if isinstance(product, PerishableProduct):

            print(f"   ID: {product.id}  |  {product.name}  |  ${product.price:.2f}  |  Expires: {product.expiration_date}")
        else:
            print(f"   ID: {product.id}  |  {product.name}  |  ${product.price:.2f}")

    def remove_product(self, product_id):
        if product_id not in self.inventory:

            raise KeyError("That product ID does not exist in the inventory.")
        removed = self.inventory.pop(product_id)

        print(f"Removed product: {removed.name} ({product_id})")

    def restock_product(self, product_id, quantity):
        if product_id not in self.inventory:

            raise KeyError("That product ID does not exist in the inventory.")
        if quantity <= 0:

            raise ValueError("Restock quantity must be positive.")
        self.inventory[product_id].quantity += quantity

        print(f"Restocked {self.inventory[product_id].name}. New balance: {self.inventory[product_id].quantity}")

    def search_by_name(self, query):

        results = [p for p in self.inventory.values() if query.lower() in p.name.lower()]
        return results

    def list_all(self):
        if not self.inventory:
            print("\nInventory is currently empty.")
            return
        for prod in self.inventory.values():

            if isinstance(prod, PerishableProduct):
                print(f"  [{prod.id}]  {prod.name}  |  ${prod.price:.2f}  |  In Stock: {prod.quantity}  |  Expires: {prod.expiration_date}")

            elif isinstance(prod, DigitalProduct):
                print(f"  [{prod.id}]  {prod.name}  |  ${prod.price:.2f}  |  In Stock: Unlimited")
            else:
                print(f"  [{prod.id}]  {prod.name}  |  ${prod.price:.2f}  |  In Stock: {prod.quantity}")


def run_manager_menu(store):
    while True:
        print("\nManager Menu")
        print("[1] Add product")
        print("[2] Remove product")
        print("[3] Restock product")
        print("[4] List all inventory")
        print("[5] Back")

        choice = input("\n> ").strip()

        try:
            match choice:
                case '1':
                    print("\nProduct type:")
                    print("[1] Physical")
                    print("[2] Digital")
                    print("[3] Perishable")
                    type_choice = input("> ").strip()

                    match type_choice:
                        case '1' | '2' | '3':
                            pass
                        case _:
                            print("Invalid product type option.")
                            continue

                    name = input("Name: ").strip()
                    if not name:
                        raise ValueError("Product name cannot be blank.")
                    
                    price = float(input("Price: "))
                    if price < 0:
                        raise ValueError("Price cannot be negative.")

                    quantity = int(input("Stock quantity: "))
                    if quantity < 0:
                        raise ValueError("Quantity cannot be negative.")

                    match type_choice:
                        case '1':
                            weight = float(input("Weight (lbs): "))
                            new_prod = PhysicalProduct(name, weight, price=price, quantity=quantity)

                        case '2':
                            size = float(input("File size (MB): "))
                            url = input("Download URL: ").strip()
                            new_prod = DigitalProduct(name, size, url, price=price, quantity=quantity)

                        case '3':
                            date_str = input("Expiration date (YYYY-MM-DD): ").strip()

                            exp_date = dt.datetime.strptime(date_str, "%Y-%m-%d").date()
                            new_prod = PerishableProduct(name, exp_date, price=price, quantity=quantity)
                    
                    store.add_product(new_prod)
                    print("\n" + "-" * 30)

                case '2':
                    prod_id = input("Product ID: ").strip()
                    store.remove_product(prod_id)
                    print("\n" + "-" * 30)

                case '3':
                    prod_id = input("Product ID: ").strip()

                    qty = int(input("Quantity: "))
                    store.restock_product(prod_id, qty)
                    print("\n" + "-" * 30)

                case '4':
                    print("\nInventory:")
                    store.list_all()
                    print("\n" + "-" * 30)

                case '5':
                    break
                case _:
                    print("Invalid choice. Please choose 1-5.")

        except (ValueError, KeyError) as e:
            print(f"Error: {e}")
            print("\n" + "-" * 30)


def run_customer_menu(store):
    while True:
        print("\n--- Customer Menu ---")
        print("[1] Browse all products")
        print("[2] Search by name")
        print("[3] Place an order")
        print("[4] Back")

        choice = input("\n> ").strip()

        match choice:
            case '1':
                print("\nProducts:")
                store.list_all()
                print("\n" + "-" * 30)

            case '2':
                query = input("Search: ").strip()

                results = store.search_by_name(query)
                if not results:
                    print("No products matched your search.")
                else:
                    print("\nResults:")
                    for p in results:
                        if isinstance(p, PerishableProduct):
                            print(f"  [{p.id}]  {p.name}  |  ${p.price:.2f}  |  In Stock: {p.quantity}  |  Expires: {p.expiration_date}")
                        elif isinstance(p, DigitalProduct):
                            print(f"  [{p.id}]  {p.name}  |  ${p.price:.2f}  |  In Stock: Unlimited")
                        else:
                            print(f"  [{p.id}]  {p.name}  |  ${p.price:.2f}  |  In Stock: {p.quantity}")
                print("\n" + "-" * 30)

            case '3':
                prod_id = input("Product ID: ").strip()

                if prod_id not in store.inventory:
                    print("Error: That product does not exist.")
                    print("\n" + "-" * 30)
                    continue
                
                prod = store.inventory[prod_id]

                try:
                    qty = int(input("Quantity: "))
                    if qty <= 0:
                        print("Error: Your order quantity has to be greater than 0.")

                        print("\n" + "-" * 30)
                        continue

                    if isinstance(prod, PerishableProduct) and prod.is_expired():
                        print(f"\nError: {prod.name} has expired.")
                        print("\n" + "-" * 30)
                        continue

                    if not isinstance(prod, DigitalProduct) and prod.quantity < qty:
                        print(f"Error: There isn't enough stock. Remaining stock: {prod.quantity}")
                        print("\n" + "-" * 30)
                        continue

                    subtotal = prod.price * qty
                    shipping = 0.00
                    shipping_label = ""

                    match prod:
                        case PhysicalProduct():
                            shipping = prod.calc_shipping_cost(qty)
                            shipping_label = "scaled by weight"
                        case PerishableProduct():
                            shipping = prod.calc_shipping_cost(subtotal)
                            shipping_label = "flat-rate" if shipping > 0 else "(free over $25)"
                        case DigitalProduct():
                            shipping = 0.00
                            shipping_label = "digital delivery"

                    total_cost = subtotal + shipping

                    print("=" * 30)
                    print("         Order Summary")
                    print("=" * 30)
                    print(f"  {prod.name} x{qty}")
                    print(f"  Unit Price : ${prod.price:.2f}")
                    print(f"  Subtotal   : ${subtotal:.2f}")
                    print(f"  Shipping   : ${shipping:.2f}  {shipping_label}")
                    print("  " + "-" * 21)
                    print(f"  Total      : ${total_cost:.2f}")
                    print("=" * 30)

                    if not isinstance(prod, DigitalProduct):
                        prod.quantity -= qty
                        print(f"Order placed! Remaining stock: {prod.quantity}")
                    else:
                        print("Order placed!")

                except ValueError:
                    print("Error: Please enter a valid integer for the .")
                
                print("\n" + "-" * 30)

            case '4':
                break
            case _:
                print("Please select a valid choice.")


def submenu(choice, store):
    match choice:
        case '1':
            run_manager_menu(store)
        case '2':
            run_customer_menu(store)


def main():
    store = Store()
    
    while True:
        print("-" * 30)
        print("PyStore Inventory System")
        print("-" * 30)
        print("\n[1] Manager Menu")
        print("[2] Customer Menu")
        print("[3] Quit")

        choice = input("\n> ").strip()

        match choice:
            case '1' | '2':
                submenu(choice, store)
            case '3':
                print("\nGoodbye!")

                break
            case _:
                print("Please select a valid choice.")


if __name__ == "__main__":
    main()