from datetime import datetime as dt
from store import Store


def main_menu():
    store = Store()
    while True:

        print("==============================")
        print("PyStore Inventory System")    
        print("==============================")
        print("[1] Manager Menu")
        print("[2] Customer Menu")
        print("[3] Quit")
        print()
        try:
            role = int(input("Select option(1-3): "))

            if role == 1:
                manager_menu(store)
            elif role == 2:
                customer_menu(store)
            elif role == 3:
                break
            else:
                print("Invalid option")
                print()
                continue
        except Exception as e:
            print(e)

def manager_menu(store):
        print() 
        print("-----Manager Menu-------")
        print()
        print("[1] Add product")
        print("[2] Remove product")
        print("[3] Restock product")
        print("[4] List all inventory")
        print("[5] Back")

        option = int(input("Please select option(1-5): "))

        match option:
            case 1: 
                print("Product type:")
                print("[1] Physical")
                print("[2] Digital")
                print("[3] Perishable")
                print()
                prod = int(input("Please select a type of product(1-3): "))

                match prod:
                    case 1:
                        phys_input(store)
                    case 2:
                        dig_input(store)
                    case 3:
                        peri_input(store)
                    case _: 
                        print("Invalid Selection.")

            case 2:
                remove_id=int(input("id to remove: "))
                store.remove_product(remove_id)

            case 3:
                restock_id = int(input("Product id: "))
                quantity = int(input("Quantity to restock: "))

                store.restock( restock_id ,quantity)
                
            case 4:
                store.display_all()
            case 5:
                return
             
def phys_input(store):
    try:
        name = input("Name: ")
        price = float(input("Price: "))
        qty = int(input("Stock quantity: "))
        expire = input("Expiration date(YYYY-MM-DD): ")
        exp = dt.fromisoformat(expire)
        store.add_product(1,name,price, qty,exp)

    except Exception as e:
        print("Exception: " + str(e))

def peri_input(store):
    try:
        name = input("Name: ")
        price = float(input("Price: "))
        qty = int(input("Stock quantity: "))
        expire = input("Expiration date(YYYY-MM-DD): ")
        exp = dt.fromisoformat(expire)
        store.add_product(3,name,price, qty,exp)

    except Exception as e:
        print("Exception: " + str(e))

def dig_input(store):
    try:
        name = input("Name: ")
        price = float(input("Price: "))
        qty = int(input("Stock quantity: "))
        expire = input("Expiration date(YYYY-MM-DD): ")
        exp = dt.fromisoformat(expire)
        store.add_product(2,name,price, qty,exp)

    except Exception as e:
        print("Exception: " + str(e))

def customer_menu(store):

    print() 
    print("-----Customer Menu-------")
    print()
    print("[1] Browse all products")
    print("[2] Search by name")
    print("[3] Place an order")
    print("[4] Back")

    option = int(input("Please select option(1-4): "))

    match option:
        case 1:
            store.display_all()
        case 2: 
            name = input("name to search: ")
            store.find_by_name(name)
        case 3: 
            try:
                id = int(input("Enter product id:"))
                qty = int(input("Enter quantity: "))
                store.order(id,qty)
            except Exception as e: 
                print(e)
        case 4:
            return
        case _: 
            print("Invalid input")



           














if __name__ == "__main__":
    main_menu()



