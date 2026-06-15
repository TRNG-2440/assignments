"""
inventory.py

Inventory service for the e-commerce shopping cart application.

This module is provided as part of the application under test for the
Shopping Cart Unit Testing activity. Do not modify this file.

Contains:
  - InventoryService : Simulates a database-backed stock level service
"""

from cart_exceptions import ItemNotFoundError, InvalidQuantityError


class InventoryService:
    """
    Simulates a database-backed inventory service.

    In production this class would open a connection to an inventory
    database and query live stock levels. For this module the
    'database call' is simulated internally.
    """

    # Simulated inventory levels (backing 'database')
    _INVENTORY_DB = {
        "SKU-001": 50,
        "SKU-002": 12,
        "SKU-003": 0,
        "SKU-004": 30,
        "SKU-005": 100,
        "SKU-006": 8,
        "SKU-007": 5,
        "SKU-008": 25,
    }

    def _query_inventory_db(self, sku: str) -> int:
        """
        Simulates a network/database call to fetch current stock level.

        Returns:
            int: current stock level for the given SKU.

        Raises:
            ItemNotFoundError: if the SKU does not exist in the inventory DB.
        """
        if sku not in self._INVENTORY_DB:
            raise ItemNotFoundError(sku)
        return self._INVENTORY_DB[sku]

    def get_stock(self, sku: str) -> int:
        """
        Returns the current stock level for a SKU.

        Raises:
            ItemNotFoundError: if the SKU is not recognised.
        """
        return self._query_inventory_db(sku)

    def is_available(self, sku: str, quantity: int) -> bool:
        """
        Returns True if at least `quantity` units are available for the SKU.

        Raises:
            ItemNotFoundError: if the SKU is not recognised.
            InvalidQuantityError: if quantity is not a positive integer.
        """
        if quantity <= 0:
            raise InvalidQuantityError(quantity)
        return self._query_inventory_db(sku) >= quantity
