from datetime import datetime

from product import Product

class PerishableProduct(Product):

    FLAT_SHIPPING = 3.99

    def __init__(self, name, price, stock, expiration_date):
        super().__init__(name, price, stock)
        self.expiration_date = expiration_date

    def is_expired(self):
        return datetime.now() > self.expiration_date
    
    def calculate_total(self, quantity):
        subtotal = self.price * quantity

        if subtotal > 25:
            shipping = 0
        else:
            shipping = self.FLAT_SHIPPING

        return subtotal + shipping
    
    def get_details(self):
        return f"Product ID: {self.product_id} | \nName: {self.name} | \nPrice: {self.price} | \nStock: {self.stock} | \nExpiration Date: {self.expiration_date}"
        
