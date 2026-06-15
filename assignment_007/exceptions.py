class InventoryError(Exception):
    pass


class ProductNotFoundError(InventoryError):
    pass


class OutOfStockError(InventoryError):
    pass


class ExpiredProductError(InventoryError):
    pass