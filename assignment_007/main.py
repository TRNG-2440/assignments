# Mark White
# 06/14/2026
# Inventory Store

# This program is a CLI store that sells physical, digital, and perishable products
# there are two menus: the manager menu and the customer menu
# the manager menu allows the user to add, remove, restock, and list the inventory
# the customer menu allows the user to browse, search, and place orders.


from datetime import datetime

from store import Store
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from perishable_product import PerishableProduct


def manager_menu(store):

    while True:

        print("\n--- Manager Menu ---")
        print("1. Add Product")
        print("2. Remove Product")
        print("3. Restock Product")
        print("4. List Inventory")
        print("5. Back")

        choice = input("> ")

        if choice == "1":

            print("\n1. Physical")
            print("2. Digital")
            print("3. Perishable")

            product_type = input("> ")

            name = input("Name: ")
            price = float(input("Price: "))

            if product_type != "2":
                stock = int(input("Stock: "))

            if product_type == "1":

                weight = float(input("Weight: "))

                product = PhysicalProduct(
                    name,
                    price,
                    stock,
                    weight
                )

            elif product_type == "2":

                file_size = float(
                    input("File Size (MB): ")
                )

                url = input("Download URL: ")

                product = DigitalProduct(
                    name,
                    price,
                    file_size,
                    url
                )

            elif product_type == "3":

                date_string = input(
                    "Expiration Date (YYYY-MM-DD): "
                )

                expiration_date = datetime.strptime(
                    date_string,
                    "%Y-%m-%d"
                ).date()

                product = PerishableProduct(
                    name,
                    price,
                    stock,
                    expiration_date
                )

            store.add_product(product)

            print("Product added!")

        elif choice == "2":

            if not store.inventory:
                print("\nInventory is empty.")
                continue

            else:
                
                try:
                    product_id = input("Product ID: ")
                    store.remove_product(product_id)
                    print("Product removed.")

                except Exception as e:
                    print(f"Error: {e}")


        elif choice == "3":
            if not store.inventory: 
                print("\nInventory is empty.")
                continue

            else: 
                try:
                    store.list_inventory()
                    product_id = input("Product ID: ")
                    quantity = int(input("Quantity: "))

                    store.restock_product(
                        product_id,
                        quantity
                    )
                    print("Product restocked.")
                except Exception as e:
                    print(f"Error: {e}")

        elif choice == "4":

            if not store.inventory: 
                print("\nInventory is empty.")
                
            else:  
                store.list_inventory()

        elif choice == "5":
            break


def customer_menu(store):

    while True:

        print("\n--- Customer Menu ---")
        print("1. Browse Products")
        print("2. Search Products")
        print("3. Place Order")
        print("4. Back")

        choice = input("> ")

        if choice == "1":

            store.list_inventory()

        elif choice == "2":

            search = input("Search: ")

            results = store.search_products(search)

            for product in results:
                print(product.get_details())

        elif choice == "3":

            product_id = input("Product ID: ")
            quantity = int(input("Quantity: "))

            total = store.place_order(
                product_id,
                quantity
            )

            print(
                f"Order placed. Total: "
                f"${total:.2f}"
            )

        elif choice == "4":
            break


def main():

    store = Store()

    while True:

        print("\n=====Inventory Store=====") 
        print("1. Manager Menu")
        print("2. Customer Menu")
        print("3. Quit")

        choice = input("> ")

        if choice == "1":
            manager_menu(store)

        elif choice == "2":
            customer_menu(store)

        elif choice == "3":
            print("Leaving the store. Goodbye!")
            break


if __name__ == "__main__":
    main()