import datetime
"""Inventory management system
from abc import ABC, abstractmethod
class Product(ABC)?

Def __Init__(self)
Pid
Name
Price
Quantity

Def Display(self)

Def CalcTotal(self)
#total  = qty * self.price
Return total

PhysicalProduct(product)
COSTPERLB = 5.0

Def __Init__(self)
Weight

Def CalcShippingCost(self)
Shipping = COSTPERLB * weight
Return shipping

@override
Def CalcTotal(self)
Total = CalcShippingCost() + (qty*self.price)
Return total 

Digital Product
  - Has a file size attribute and a download URL.

  __init__
  file_size
  download_url


   - Has no shipping cost — its total price is always just the item price.


   - Stock is not limited in the traditional sense; purchasing a digital product does not reduce available stock.

PerishableProduct
   SHIPIING_COST = 3.00

   init
   super
   expiration_date


   check_exp()
   check expiration based on today's date
   datetime.date


   - Expired products cannot be added to a customer order.

"""





class Product:
    pid
