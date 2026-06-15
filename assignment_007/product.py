from abc import abstractmethod
from abc import ABC


class Product(ABC):

    next_id = 1

    def __init__(self, name, price, stock):

        self.product_id = f"PRD-{Product.next_id:04}"
        Product.next_id += 1

        self.name = name
        self.price = price
        self.stock = stock

    @abstractmethod
    def calculate_total(self, quantity):
        
        pass

    @abstractmethod
    def get_details(self):
        pass