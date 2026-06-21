import unittest
from unittest.mock import patch,Mock
from cart import ShoppingCart
from cart_exceptions import InvalidQuantityError, CartItemNotFoundError,EmptyCartError, ItemNotFoundError, InvalidDiscountCodeError, InsufficientStockError




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
        self.assert_sku7_multi =  {'sku': 'SKU-007',"name": "Monitor Stand","unit_price": 44.99,"quantity": 4,"category": "Electronics"}
        self.assert_sku2 = {'sku' : 'SKU-002' ,"name": "USB-C Hub", "unit_price": 34.99, "quantity": 3, "category": "Electronics"}
        self.assert_sku2_one = {'sku' : 'SKU-002' ,"name": "USB-C Hub", "unit_price": 34.99, "quantity": 1, "category": "Electronics"}

    #test single item added
    def test_add_item(self):
        """test add item functionality"""
        self.shopping.add_item( "SKU-007", 1)
        items2 = self.shopping.get_items() #returns list of dicts in items
        self.assertEqual(items2[0],self.assert_sku7)

    #test that multiple items add to quantity in cart
    def test_add_multiple_items(self):
        """test add multiple items functionality"""
        self.shopping.add_item( "SKU-007", 1)
        self.shopping.add_item( "SKU-007", 3)
        items = self.shopping.get_items() #returns list of dicts in items
        self.assertEqual(items[0],self.assert_sku7_multi)

    #Check that list updates when one item is removed
    def test_remove_item(self):
        self.shopping.add_item( "SKU-007", 3)
        self.shopping.add_item( "SKU-002", 3)
        self.shopping.remove_item("SKU-007")
        items = self.shopping.get_items() #returns list of dicts in items
        self.assertEqual(items[0],self.assert_sku2)

    #test quantity is updated
    def test_update_quantity(self):
        self.shopping.add_item( "SKU-002", 3)
        self.shopping.update_quantity("SKU-002",1)
        items = self.shopping.get_items()
        self.assertEqual(items[0],self.assert_sku2_one)

    #test it throws exception when quantity requested is raised above the quantity in stock 
    def test_update_quantity_stock_exception(self):  
        with self.assertRaises(InsufficientStockError):
            self.shopping.add_item("SKU-002",1)
            self.shopping.update_quantity("SKU-002",13)



class TestInventoryManagement(unittest.TestCase):
    """The `ShoppingCart` relies on `InventoryService` to check stock levels before allowing
    items to be added. In a production environment this service would make a live call to an external
    inventory database — something unit tests must never depend on. Your job is to read `cart.py` and 
    `inventory.py`, understand the call chain between `ShoppingCart` and `InventoryService`, determine
    the appropriate method to patch to take control of it. Use Mocking"""
  
    def setUp(self):
        self.shopping = ShoppingCart()
        self.assert_sku2 = {'sku' : 'SKU-002' ,"name": "USB-C Hub", "unit_price": 34.99, "quantity": 2, "category": "Electronics"}


    #Simulate sufficient stock being available and verify the item is added successfully
    def test_mock_add_item(self):
        with patch("inventory.InventoryService.get_stock") as mock_get:
            mock_response = Mock()
            mock_response = 4
            mock_get.return_value = mock_response
            self.shopping.add_item("SKU-002",2)
            #Verify that the mocked method you patched is actually called when
            #`add_item` is invoked (use `assert_called_with` or `assert_called_once`)
            mock_get.assert_called_with("SKU-002")
            #Verify item added
            items = self.shopping.get_items()
            self.assertEqual(items[0],self.assert_sku2)



    #Simulate stock being unavailable and verify the correct exception is raised
    #Simulate the inventory service returning a lower stock level than the requested quantity
    def test_mock_get_inventory_with_exception(self):
        with patch("inventory.InventoryService.get_stock") as mock_get:
            mock_response = Mock()
            mock_response = 2
            mock_get.return_value = mock_response
            
            with self.assertRaises(InsufficientStockError):
                self.shopping.add_item("SKU-002",3)

    #Other exceptions already covered in other classes
 

class TestDiscountCodes(unittest.TestCase):
    """Write tests covering the full range of discount code behaviour: valid percentage-based codes,
    valid flat-rate codes, unrecognised codes, expired codes, and the removal of an applied code. 
    Verify that discount amounts are calculated correctly against known subtotals."""
    def setUp(self):
        self.shopping  = ShoppingCart()
        self.assert_sku7 =  {'sku': 'SKU-007',"name": "Monitor Stand","unit_price": 44.99,"quantity": 1,"category": "Electronics"}

    #use get_discount_amout()
    #Verify discount code calculated correctly Percent
    def test_discount_percent(self):
        discount_total = 9.0 #discount amount for testing
        self.shopping.add_item( "SKU-007", 2)
        self.shopping.apply_discount_code("SAVE10")
        discount = self.shopping.get_discount_amount()
        self.assertEqual(discount,discount_total)


    #Verify discount calculated correctly Flat
    def test_discount_flat(self):
        discount_total = 5.0 #discount amount for testing
        self.shopping.add_item( "SKU-007", 2)
        self.shopping.apply_discount_code("FLAT5")
        discount = self.shopping.get_discount_amount()
        self.assertEqual(discount,discount_total)


    #Code not in Discount Codes -> throw InvalidDiscountCodeError
    def test_discount_invalid(self):
        self.shopping.add_item( "SKU-007", 2)
        with self.assertRaises(InvalidDiscountCodeError):
            self.shopping.apply_discount_code("FLAT7")
            

    #Code expired -> throw InvalidDiscountCodeError
    def test_discount_expired(self):
        self.shopping.add_item( "SKU-007", 2)
        with self.assertRaises(InvalidDiscountCodeError):
            self.shopping.apply_discount_code("EXPIRED50")
             


    #Remove applied discount code -> verify subtotal before and after
    def test_removed_discount(self):
        discount_total = 9.0 #discount amount for testing
        self.shopping.add_item( "SKU-007", 2)
        self.shopping.apply_discount_code("SAVE10")
        discount = self.shopping.get_discount_amount()
        self.assertEqual(discount,discount_total)

        total = self.shopping.get_total()
        calc_total = 88.18
        self.assertEqual(total,calc_total)

        self.shopping.remove_discount_code()
        removed_total = self.shopping.get_total()
        calc_total_after_removal = 97.18
        self.assertEqual(removed_total,calc_total_after_removal)
    

class TestCalculations(unittest.TestCase):
    """Write tests that verify `get_subtotal`, `get_discount_amount`,
    get_tax`, and `get_total` return the correct values for a known cart configuration.
    Use a cart with a fixed set of items so that expected values can be calculated and hardcoded
    in your assertions. Include a test that confirms the total is correctly computed as 
    subtotal- discount + tax """
    def setUp(self):
        self.shopping  = ShoppingCart()
        
        self.shopping.add_item("SKU-001", 1)
        self.shopping.add_item("SKU-004", 2)
        self.shopping.add_item("SKU-005", 3)
        self.shopping.apply_discount_code("SAVE10")

    def test_total_after_everything(self):
        """Confirms get_total() == get_subtotal() - get_discount_amount() + get_tax()"""
        subtotal = self.shopping.get_subtotal()
        discount = self.shopping.get_discount_amount()
        tax = self.shopping.get_tax()
        total = self.shopping.get_total()
 
        self.assertEqual(subtotal, 138.94) #testing get_subtotal()
        self.assertEqual(discount, 13.89) #testing get_discount_amount()
        self.assertEqual(tax, 8.95)#testing get_tax()
        self.assertEqual(total, 134.00)#testing get_total()
 
        self.assertEqual(total, round(subtotal - discount + tax, 2))

class TestCheckoutAndExceptions(unittest.TestCase):
    """Test checkout and Exceptions"""

    def setUp(self):
        self.shopping = ShoppingCart()
        self.shopping.add_item("SKU-001", 1)
        self.shopping.add_item("SKU-004", 2)
        self.shopping.add_item("SKU-005", 3)
        self.shopping.apply_discount_code("SAVE10")

    # Calling `clear` resets all items and the discount code"""
    def test_clear_cart(self):
        self.shopping.clear()
        bool = self.shopping.is_empty()
        self.assertTrue(bool)

        no_item = self.shopping.get_item_count()
        self.assertEqual(no_item, 0)

        discount  = self.shopping.get_discount_amount()
        self.assertEqual(0.0,discount) 


    #Checking out an empty cart raises `EmptyCartError`
    def test_empty_cart(self):
        self.shopping.clear()
        with self.assertRaises(EmptyCartError):
            self.shopping.checkout()
    
    #Checking out a populated cart returns a summary dict containing all required keys
    def test_checkout_returns_summary_with_all_required_keys(self):
        summary = self.shopping.checkout()
 
        required_keys = {
            "customer_id",
            "timestamp",
            "items",
            "subtotal",
            "discount_code",
            "discount_amount",
            "tax",
            "total",
            "item_count",
        }
        self.assertIsInstance(summary, dict)
        self.assertTrue(required_keys.issubset(summary.keys()))
 
    def test_checkout_summary_values_are_correct(self):
        summary = self.shopping.checkout()
 
        self.assertEqual(summary["subtotal"], 138.94)
        self.assertEqual(summary["tax"], 8.95)
        self.assertEqual(summary["discount_code"], "SAVE10")
        self.assertEqual(summary["discount_amount"], 13.89)
        self.assertEqual(summary["total"], 134.00)
        self.assertEqual(summary["item_count"], 6)
        self.assertEqual(len(summary["items"]), 3)
 

    """- Adding an item with a zero or negative quantity raises `InvalidQuantityError`
    - Removing or updating an item that is not in the cart raises `CartItemNotFoundError`
    - Adding a SKU that does not exist in the product catalogue raises `ItemNotFoundError`"""

  

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(InvalidQuantityError):
             self.shopping.add_item("SKU_003",0)
                                    
    def test_add_item_2(self):
        with self.assertRaises(InvalidQuantityError):
            self.shopping.add_item("SKU-003",-1)

    def test_not_in_catalogue(self):
        with self.assertRaises(ItemNotFoundError):
             self.shopping.add_item("SKU_009",20)

    #check the remove_item method for this exception
    def test_not_found_error(self):
        with self.assertRaises(CartItemNotFoundError):
            self.shopping.remove_item("SKU-007")
    
    def test_not_found_error_update(self):
        with self.assertRaises(CartItemNotFoundError):
            self.shopping.update_quantity("SKU-009",4)