import unittest
from unittest.mock import patch, MagicMock
from cart import ShoppingCart
from cart_exceptions import CartError



class TestItemManagement(unittest.TestCase):
    """"Write tests that verify the behaviour of `add_item`, `remove_item`, and `update_quantity
    `.Your tests should confirm that items are correctly added to the cart, that quantities accumulate
    when the same SKU is added more than once, and that remove and update operations behave correctly 
    for both valid and invalid inputs."""
    def setUp(self):
        """shop = ShoppingCart( self,   inventory_service: InventoryService = None, 
        pricing_service: PricingService = None,
        customer_id: str = None,)"""
        self.shopping = ShoppingCart()


        self.assert_sku7 =  {'sku': 'SKU-007',"name": "Monitor Stand","unit_price": 44.99,"quantity": 1,"category": "Electronics"}
        
    def test_add_item(self):
        
        self.shopping.add_item( "SKU-007", 1)

        items = self.shopping.get_items() #returns list of dicts in items
 
        self.assertEqual(items[0],self.assert_sku7)


        #try adding two of same sk
        #assert quantity increases



        # check all fields in item       self._items[sku] = {
                #"sku": sku,
               # "name": product["name"],
               # "unit_price": product["price"],
               # "quantity": quantity,
              #  "category": product["category"],
           # }






        #check if sku is in cart and if not assert the value of items.[sku,["quantity", 0]]


        #
        pass


class TestInventoryManagement(unittest.TestCase):
    """The `ShoppingCart` relies on `InventoryService` to check stock levels before allowing
    items to be added. In a production environment this service would make a live call to an external
    inventory database — something unit tests must never depend on. Your job is to read `cart.py` and 
    `inventory.py`, understand the call chain between `ShoppingCart` and `InventoryService`, determine
    the appropriate method to patch to take control of it. Use Mocking"""
    pass

class TestDiscountCodes(unittest.TestCase):
    """Write tests covering the full range of discount code behaviour: valid percentage-based codes,
    valid flat-rate codes, unrecognised codes, expired codes, and the removal of an applied code. 
    Verify that discount amounts are calculated correctly against known subtotals."""
    pass

class TestCalculations(unittest.TestCase):
    """Write tests that verify `get_subtotal`, `get_discount_amount`,
    get_tax`, and `get_total` return the correct values for a known cart configuration.
    Use a cart with a fixed set of items so that expected values can be calculated and hardcoded
    in your assertions. Include a test that confirms the total is correctly computed as 
    subtotal- discount + tax """
    pass
    
class TestCheckoutAndExceptions(unittest.TestCase):
    """Write tests for the `checkout` method and the following edge cases:
    - Checking out a populated cart returns a summary dict containing all required keys
    - Checking out an empty cart raises `EmptyCartError`
    - Calling `clear` resets all items and the discount code
    - Adding an item with a zero or negative quantity raises `InvalidQuantityError`
    - Removing or updating an item that is not in the cart raises `CartItemNotFoundError`
    - Adding a SKU that does not exist in the product catalogue raises `ItemNotFoundError`"""

    def setUp(self):
        #shopping  = ShoppingCart()
        #exceptions add_items:
        #assert
        #if qty < 0        "SKU-003": 0
        # ->InvalidQuantityError(quantity)

        #   "SKU-007": 5,
        #
        """    shopping.add_item(self, "SKU-007", 1)
        self.assertEqual()
        """
        #  assert sku not in PRODUCT_CATALOGUE    "SKU-009": 20,
        #  ItemNotFoundError(sku)


        #Simulate total quantity > available  ->  raise InsufficientStockError(sku, total_qty, available)

    pass
