from digital_product import DigitalProduct
from exceptions import (
    ProductNotFoundError,
    OutOfStockError,
    ExpiredProductError
)


class Store:

    def __init__(self):
        self.inventory = []

    def add_product(self, product):
        self.inventory.append(product)

    def find_product(self, product_id):

        for product in self.inventory:

            if product.product_id == product_id:
                return product

        raise ProductNotFoundError(
            f"{product_id} not found."
        )

    def remove_product(self, product_id):

        if not self.find_product(product_id):
            raise ProductNotFoundError(
                f"{product_id} not found."
            )
        else:
            pass

        product = self.find_product(product_id)

        self.inventory.remove(product)

    def restock_product(
        self,
        product_id,
        quantity
    ):

        product = self.find_product(product_id)

        product.stock += quantity

    def search_products(self, search_term):

        results = []

        for product in self.inventory:

            if search_term.lower() in product.name.lower():
                results.append(product)

        return results

    def list_inventory(self):

        for product in self.inventory:

            if product.stock > 0:
                print(product.get_details())
            else:
                print(f"{product.name} is out of stock.")

    def place_order(
        self,
        product_id,
        quantity
    ):

        product = self.find_product(product_id)

        if hasattr(product, "is_expired"):

            if product.is_expired():
                raise ExpiredProductError(
                    f"{product.name} is expired."
                )

        if quantity > product.stock:
            raise OutOfStockError(
                "Insufficient stock."
            )

        total = product.calculate_total(quantity)

        if not isinstance(product, DigitalProduct):
            product.stock -= quantity

        return total