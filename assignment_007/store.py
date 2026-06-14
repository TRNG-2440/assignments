from product import PhysicalProduct, DigitalProduct, PerishableProduct
"""    - Expired products cannot be added to a customer order.

STORE
 - Adding a new product of any supported type to the inventory
   - Removing a product by ID
   - Restocking an existing product (increasing its quantity)
   - Searching for products by name (partial matches count)
   - Listing all in-stock products




"""
class Store:
    id = 99999

    def __init__(self):
        self._products = {}
    def order(self,id,qty):
        #is product in stock
        #inventory - qty for all except digital
        #return order summary with total cost including shipping
        if id in self._products:
            if qty > 0:
                self._products[id].order_prod(qty)
            else:
                raise ValueError("Quantity must be > 0 ")
        else:
            raise ValueError(f"{id} not found in store.")
         
    def add_product(self,type,name,price, qty,*args):
        """ [1] Physical
            [2] Digital
            [3] Perishable  ->  """
        price = float(price)
        qty = int(qty)
        if type == 1:
            self.id = self.id  + 1
            weight = args[0]
            self._products[self.id] = PhysicalProduct(self.id,name,price, qty, weight)
            print("Physical product added.")
            self._products[self.id].display()

        elif type == 2:
            self.id = self.id + 1
            if args:
                url,filesize = args
                self._products[self.id] = DigitalProduct(self.id,name,price, qty,url,filesize)
            else:
                self._products[self.id] = DigitalProduct(self.id,name,price, qty)
            print("Digital product added.")
            self._products[self.id].display()

        elif type == 3:
            self.id = self.id + 1
            exp = args[0]
            self._products[self.id] = PerishableProduct(self.id,name,price,qty,exp)
            print("Perishable product added.")
            self._products[self.id].display()
        else:
            raise Exception("Invalid Selection")

    def remove_product(self,id):
        try:
            del self._products[id]
            print(f"{id} removed from store.")

        except KeyError:
            print(f"{id} not found in store")
        
    def find_by_name(self,name):
        found = False
        for id, prod in self._products.items():
            if name in prod.get_name():
                found = True
                prod.display()
        if not found:
            print("No matching products found.")
        
        
    def restock(self, id,add):
        add = int(add)
        if(add < 0):
            raise ValueError("Restock Quantity must be larger than 0.")
        elif self._products.get(id).TYPE == 2:
            raise ValueError("Digital Products do not need restocking")
        else:
            self._products.get(id).restock(add)

    def display_all(self):
        if self._products:
            for id,product in self._products.items():
                product.display()
        else:
            print("Store is empty")

