# Shopping Cart — Unit Testing Activity

## Objective

In this activity, you will write a comprehensive unit test suite for a pre-built shopping cart module that simulates an enterprise e-commerce application. You will practice:

- Writing unit tests using Python's built-in `unittest` module
- Organising tests into logical `TestCase` classes
- Using `setUp` and `tearDown` to manage test state
- Testing both expected outputs and expected exceptions
- Using `Mock` and `MagicMock` (as relevant) to isolate units under test from external dependencies
- Identifying and writing tests for edge cases and boundary conditions

---

## Setup

This activity spans five Python modules. Do **not** modify any of them — they collectively form the application under test.

| Module | Purpose |
|---|---|
| `cart_exceptions.py` | All custom exception classes used across the application |
| `catalogue.py` | Static data: product catalogue, discount codes, and tax rates |
| `inventory.py` | `InventoryService` — simulates a database-backed stock level service |
| `pricing.py` | `PricingService` — handles discount code validation and tax calculation |
| `cart.py` | `ShoppingCart` — core cart logic; the primary class under test |

Create a new file called `test_shopping_cart.py` in the same directory. All of your tests will live in this file.

At a minimum, your test file will need the following imports to get started:

```python
import unittest
from unittest.mock import patch, MagicMock
from cart import ShoppingCart
from cart_exceptions import CartError
```

As you work through each test area, inspect the relevant modules to identify which additional classes and exceptions you need to import. Discovering what each module exposes and when its exceptions are raised is part of the exercise.

---

## Instructions

You will write tests that cover the five areas below. Each area should be its own `TestCase` class. Use `setUp` in each class to construct a fresh `ShoppingCart` instance (and any supporting objects) before every test — never share state between tests.

### 1. Item Management
Write tests that verify the behaviour of `add_item`, `remove_item`, and `update_quantity`. Your tests should confirm that items are correctly added to the cart, that quantities accumulate when the same SKU is added more than once, and that remove and update operations behave correctly for both valid and invalid inputs.

### 2. Inventory Checks with Mocking
The `ShoppingCart` relies on `InventoryService` to check stock levels before allowing items to be added. In a production environment this service would make a live call to an external inventory database — something unit tests must never depend on. Your job is to read `cart.py` and `inventory.py`, understand the call chain between `ShoppingCart` and `InventoryService`, determine the appropriate method to patch to take control of it.

Write tests that use mocking to:
- Simulate sufficient stock being available and verify the item is added successfully
- Simulate stock being unavailable and verify the correct exception is raised
- Simulate the inventory service returning a lower stock level than the requested quantity
- Verify that the mocked method you patched is actually called when `add_item` is invoked (use `assert_called_with` or `assert_called_once`)

### 3. Discount Codes
Write tests covering the full range of discount code behaviour: valid percentage-based codes, valid flat-rate codes, unrecognised codes, expired codes, and the removal of an applied code. Verify that discount amounts are calculated correctly against known subtotals.

### 4. Pricing and Tax Calculations
Write tests that verify `get_subtotal`, `get_discount_amount`, `get_tax`, and `get_total` return the correct values for a known cart configuration. Use a cart with a fixed set of items so that expected values can be calculated and hardcoded in your assertions. Include a test that confirms the total is correctly computed as `subtotal - discount + tax`.

### 5. Checkout and Edge Cases
Write tests for the `checkout` method and the following edge cases:
- Checking out a populated cart returns a summary dict containing all required keys
- Checking out an empty cart raises `EmptyCartError`
- Calling `clear` resets all items and the discount code
- Adding an item with a zero or negative quantity raises `InvalidQuantityError`
- Removing or updating an item that is not in the cart raises `CartItemNotFoundError`
- Adding a SKU that does not exist in the product catalogue raises `ItemNotFoundError`

---

## Example: Using Mocks

Below is a minimal example of how `unittest.mock.patch.object` works. This example patches a method on a made-up class — it is intentionally unrelated to the shopping cart module so that applying the same pattern to your own tests remains your work to do.

```python
import unittest
from unittest.mock import patch

class DatabaseService:
    def _query_db(self, key: str) -> int:
        # imagine this opens a real DB connection
        ...

class ReportGenerator:
    def __init__(self):
        self._db = DatabaseService()

    def get_record_count(self, key: str) -> int:
        return self._db._query_db(key)


class TestReportGenerator(unittest.TestCase):

    def setUp(self):
        self.report = ReportGenerator()

    # Recall that patch as a context manager using 'with'
    # would look something like this:
    # with patch('DatabaseService._query_db') as mock_query:
    #     mock_query.return_value = 50
    #     other mocked code...
    @patch.object(DatabaseService, "_query_db")
    def test_get_record_count(self, mock_query):
        # Control what the "database" returns without a real connection
        mock_query.return_value = 50

        result = self.report.get_record_count("some-key")

        self.assertEqual(result, 50)
        mock_query.assert_called_once_with("some-key")
```

The key ideas to take from this example:
- `@patch.object(ClassName, "method_name")` replaces the named method for the duration of the test
- The mock is injected as an argument to the test method (`mock_query` above)
- `return_value` controls what the patched method returns when called
- `assert_called_once_with(...)` verifies the mock was called with the expected arguments

> **NOTE:** The class, method names, and scenario above are fictional. Identifying which module to import from, which class and method to patch, and what to assert after patching is part of the activity.

---

## Requirements Checklist

- [ ] All tests are contained in `test_shopping_cart.py`
- [ ] Tests are organised into at least 5 `TestCase` subclasses, one per area above
- [ ] Every `TestCase` class uses `setUp` to initialise a fresh cart before each test
- [ ] `add_item` is tested for: valid addition, duplicate SKU accumulation, invalid SKU, invalid quantity, and insufficient stock
- [ ] `remove_item` is tested for: successful removal and removing a SKU not in the cart
- [ ] `update_quantity` is tested for: valid update, invalid quantity, insufficient stock, and updating a SKU not in the cart
- [ ] Discount code tests cover: valid percent code, valid flat code, expired code, unrecognised code, and code removal
- [ ] Tax and subtotal tests use a known cart configuration with hardcoded expected values
- [ ] `get_total` is verified as the correct combination of subtotal, discount, and tax
- [ ] `checkout` is tested for both a populated cart (valid summary returned) and an empty cart (`EmptyCartError` raised)
- [ ] `clear` is tested to confirm all items and discount codes are removed
- [ ] All exception-raising scenarios use `assertRaises` (via `with self.assertRaises(...)` context manager)
- [ ] No test relies on or mutates state from another test

---

## Stretch Goals

- **Parameterised Tests** — Use `unittest`'s `subTest` context manager to run the same test logic across multiple inputs in a single test method. For example, test several invalid quantity values (`0`, `-1`, `-100`) or multiple discount codes in one loop without duplicating test methods.
- **Mock Side Effects** — Instead of returning a fixed value, configure your mock to raise an exception on the first call and return a valid value on the second using `side_effect`. Use this to test how the cart behaves when the inventory service is temporarily unavailable.
- **Test Coverage Report** — Install the `coverage` package (`pip install coverage`) and run your suite with `coverage run -m unittest test_shopping_cart.py`, then generate a report with `coverage report -m`. Aim for 90%+ coverage and identify any untested lines.
- **PricingService Mocking** — In addition to mocking `InventoryService`, write a test class that injects a fully mocked `PricingService` into the cart. Verify that `ShoppingCart.checkout` calls `calculate_tax` and `apply_discount` with the correct arguments, without caring about the actual return values.
