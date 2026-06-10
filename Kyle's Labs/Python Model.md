# Model Builder

## Objective
Practice building a Python class with an initializer, properties, setters, and a string representation.

## Setup
Create a new file called `model_builder.py`.

## Instructions
Build an `Account` class to hold the following data:

| Field      | Type  | Example    |
|------------|-------|------------|
| id         | int   | 1042       |
| first_name | str   | "Alice"    |
| last_name  | str   | "Smith"    |
| balance    | float | 1250.75    |

Your class should include:
1. An `__init__` method that accepts all four fields
2. A `@property` getter and `@<field>.setter` for each field
3. Store the backing values with a leading underscore (e.g., `self._first_name`)
4. A read-only `@property` called `full_name` that returns `"first_name last_name"` (no setter needed)
5. A `__str__` method that returns a readable string like:
   ```
   Account(1042, Alice Smith, 1250.75)
   ```

## Test It
Paste this at the bottom of your file and confirm it works:

```python
acct = Account(1042, "Alice", "Smith", 1250.75)
print(acct)
print(acct.full_name)
acct.first_name = "Bob"
print(acct.full_name)
print(acct)
```

Expected output:
```
Account(1042, Alice Smith, 1250.75)
Alice Smith
Bob Smith
Account(1042, Bob Smith, 1250.75)
```