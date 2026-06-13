# Assignment 7 by Ariyan Shaikh

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
    def __init__(self, product_id, name, price, stock_quantity):
        super().__init__(product_id, name, price, stock_quantity)

def get_selection(num_selections: int) -> int:
    """
    Collects and validates users's Selection.
    Requires the number of selections passed as an int paramater
    """
    print()
    while True:
        try:
            selection = int(input("Select an option: "))        
            if selection > num_selections or selection < 1:
                raise Exception("Invalid input detected")
        except Exception as ex:
            print("\nThat is not a valid input. Please try again\n")
            return get_selection(num_selections)
        return selection


if __name__ == "__main__":
    print("=" * 40)
    print(f'{"PyStore Inventory System":^40}')
    print("=" * 40)

    print()
    print("[1] Manager Menu")
    print("[2] Customer Menu")
    print("[3] Quit")

    while True:
        menu_option = get_selection(3)
        match menu_option:
            case 1:
                pass
            case 2:
                pass
            case 3:
                print("Goodbye")
                break
