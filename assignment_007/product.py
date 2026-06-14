from datetime import date
from typing import override

"""Inventory management system"""



class Product:

    def __init__(self,pid,name,price, qty):
        self._pid = pid
        self._name = name
        self._price = price
        self._qty = qty
    @property
    def get_name(self):
        return self._name
    @property
    def qty(self):
        return self._qty
    
    @qty.setter
    def restock(self,add):
        self._qty = self._qty + add
        print(f"{self._pid} restocked. {self._qty} left in stock.") 

    def display(self):
        print(f"{self._pid:<8} | {self._name:<15} | {self._price:>6,.2f} | In Stock:{self._qty:<3}")

    def calc_total(self, quantity):
        total  = quantity * self._price
        return total
    

    
class PhysicalProduct(Product):
    COSTPERLB = 5.0
    TYPE = 1
    #weight in lb

    def __init__(self,pid,name,price, qty, weight):
        super().__init__(pid,name,price, qty)
        self._weight = weight


    def calc_shipping_cost(self):
        shipping = self.COSTPERLB * self._weight
        return shipping
    
    def order_prod(self,qty):
        if (self._qty - qty) < 0:
            raise ValueError("Insufficient stock quantity.")
        else:
            self._qty -= qty
            subtotal = qty * self._price
            shipping = self.calc_shipping_cost()
            total = self.calc_total(qty)
            print("==============================")

            print("Order Summary")
            print("==============================")

            print(f"{self._name:<15} x{qty:>6}")
            print("------------------------------")
            print(f"{'Unit Price':<8} : {self._price:<6.2f}")
            print(f"{'Subtotal':<8} : {subtotal:<6.2f}")
            print(f"{'Shipping':<8} : {shipping:<6.2f}")
            print("------------------------------")
            print(f"{'Total':<8} : {total:<6.2f}")
            print("==============================")
            print(f"Order placed! Remaining stock: {self._qty}")


    @override
    def calc_total(self,quantity):
        total = self.calc_shipping_cost() + (quantity * self._price)
        return total 

    @override
    def display(self):
        print(f"{self._pid:<8} | {self._name:<15} | {self._price:>6,.2f} | In Stock:{self._qty:<3} | Unit weight: {self._weight:<5.2f}lb")


class DigitalProduct(Product):
   #file_size in mb
    TYPE = 2
    def __init__(self,pid,name,price, qty, url = "www.amazon.com", filesize = 6):
        super().__init__(pid,name,price, qty)
        self.url = url
        self.filesize = filesize

    def order_prod(self,qty):
        if (self._qty - qty) < 0:
            raise ValueError("Insufficient stock quantity.")
        else:
            self._qty -= qty
            subtotal = qty * self._price
            total = self.calc_total(qty)
            print("==============================")

            print("Order Summary")
            print("==============================")

            print(f"{self._name:<15} x{qty:>6}")
            print("------------------------------")
            print(f"{'Unit Price':<8} : {self._price:<6.2f}")
            print(f"{'Subtotal':<8} : {subtotal:<6.2f}")
            print(f"{'Shipping':<8} : {'0.00':<6.2f} (digital)")
            print("------------------------------")
            print(f"{'Total':<8} : {total:<6.2f}")
            print("==============================")
            print(f"Order placed! Remaining stock: {self._qty}")

   #Has no shipping cost — its total price is always just the item price.
    @override
    def calc_total(self, quantity):
        total = self._price
        return total 
    
    #Stock is not limited in the traditional sense; purchasing a digital product does not reduce available stock.
    @override
    def display(self):
        print(f"{self._pid:<8} | {self._name:<15} | {self._price:>6,.2f} | In Stock: {self._qty:<3}")
        print(f" | Filesize: {self.filesize:<5.2f}MB | url: {self.url}")

class PerishableProduct(Product):
    TODAY = date.today()
    SHIPPING_COST = 3.00
    TYPE = 3
    def __init__(self,pid,name,price, qty, exp):
        super().__init__(pid,name,price, qty)
        self.exp = exp

    def is_exp(self):
        """Returns True if Product is expired or expiring today"""
        #check expiration based on today's date
        # Expired products cannot be added to a customer order.
        exp_date = self.exp.date() if hasattr(self.exp, 'date') else self.exp
        if exp_date <= self.TODAY:
            print("Product cannot be puchased")
            return True
        else:
            return False
    def order_prod(self,qty):
        if self.is_exp():
            raise ValueError("This Product is expired and unable to be ordered.")
        elif (self._qty - qty) < 0:
            raise ValueError("Insufficient stock quantity.")
        else:
            self._qty -= qty
            subtotal = qty * self._price
            total = self.calc_total(qty)
            print("==============================")

            print("Order Summary")
            print("==============================")

            print(f"{self._name:<15} x{qty:>6}")
            print("------------------------------")
            print(f"{'Unit Price':<8} : {self._price:<6.2f}")
            print(f"{'Subtotal':<8} : {subtotal:<6.2f}")
            shipping_cost = 0 if subtotal >= 25 else self.SHIPPING_COST
            print(f"{'Shipping':<8} : {shipping_cost:<6.2f} (flat rate)")
            print("------------------------------")
            print(f"{'Total':<8} : {total:<6.2f}")
            print("==============================")
            print(f"Order placed! Remaining stock: {self._qty}")


    @override
    def calc_total(self, quantity):
        total_noship = quantity * self._price
        if total_noship >= 25:
            return total_noship
        else:
            total = total_noship  + self.SHIPPING_COST
            return total 
    
    @override
    def display(self):
        date_str = self.exp.isoformat()

        print(f"{self._pid:<8} | {self._name:<15} | {self._price:>6,.2f} | In Stock: {self._qty:<3}")
        print(f" | Expires: {date_str} | Shipping Cost: {self.SHIPPING_COST}")

