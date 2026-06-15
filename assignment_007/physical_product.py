from product import Product

class PhysicalProduct(Product):

    def __init__(self, name, price, stock, weight):
        super().__init__(name, price, stock)
        self.weight = weight

    def shipping_cost(self, quantity):
        return self.weight * quantity *1.50
    
    def calculate_total(self, quantity):
        return self.price * quantity

    def get_details(self):
        return f"Product ID: {self.product_id}\nName: {self.name}\nPrice: {self.price}\nStock: {self.stock}\nWeight: {self.weight}"