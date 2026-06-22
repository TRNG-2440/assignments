"""
catalogue.py

Static data store for the e-commerce shopping cart application.

This module is provided as part of the application under test for the
Shopping Cart Unit Testing activity. Do not modify this file.

Contains:
  - PRODUCT_CATALOGUE    : All available products keyed by SKU
  - DISCOUNT_CODES       : Valid and expired discount code definitions
  - CATEGORY_TAX_RATES   : Tax rates applied per product category
"""

from datetime import date


# ---------------------------------------------------------------------------
# Product Catalogue
# In production this would be sourced from a database or external API.
# ---------------------------------------------------------------------------

PRODUCT_CATALOGUE = {
    "SKU-001": {"name": "Wireless Keyboard",    "price": 49.99,  "category": "Electronics"},
    "SKU-002": {"name": "USB-C Hub",            "price": 34.99,  "category": "Electronics"},
    "SKU-003": {"name": "Ergonomic Mouse",      "price": 39.99,  "category": "Electronics"},
    "SKU-004": {"name": "Desk Lamp",            "price": 24.99,  "category": "Home Office"},
    "SKU-005": {"name": "Notebook (Pack of 3)", "price": 12.99,  "category": "Stationery"},
    "SKU-006": {"name": "Standing Desk Mat",    "price": 59.99,  "category": "Home Office"},
    "SKU-007": {"name": "Monitor Stand",        "price": 44.99,  "category": "Electronics"},
    "SKU-008": {"name": "Cable Management Kit", "price": 18.99,  "category": "Home Office"},
}


# ---------------------------------------------------------------------------
# Discount Codes
# Each entry defines a type ('percent' or 'flat'), a value, and an expiry date.
# ---------------------------------------------------------------------------

DISCOUNT_CODES = {
    "SAVE10":    {"type": "percent", "value": 10,    "expires": date(2099, 12, 31)},
    "SAVE20":    {"type": "percent", "value": 20,    "expires": date(2099, 12, 31)},
    "FLAT5":     {"type": "flat",    "value": 5.00,  "expires": date(2099, 12, 31)},
    "FLAT15":    {"type": "flat",    "value": 15.00, "expires": date(2099, 12, 31)},
    "EXPIRED50": {"type": "percent", "value": 50,    "expires": date(2000, 1, 1)},
}


# ---------------------------------------------------------------------------
# Tax Rates
# Applied per product category at the point of tax calculation.
# ---------------------------------------------------------------------------

CATEGORY_TAX_RATES = {
    "Electronics": 0.08,
    "Home Office":  0.06,
    "Stationery":   0.05,
}
