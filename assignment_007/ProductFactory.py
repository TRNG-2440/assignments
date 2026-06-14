"""Defines `ProductFactory`, a factory for constructing concrete `Product`
subclass instances based on a `ProductType`."""

from typing import Dict, Type, Any

from Product import Product, ProductType
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from PerishableProduct import PerishableProduct


class ProductFactory:
    """Factory class that creates `Product` instances from a `ProductType`."""

    # Map each product type enum value directly to its concrete implementation class
    _registry: Dict[ProductType, Type[Product]] = {
        ProductType.PHYSICAL: PhysicalProduct,
        ProductType.DIGITAL: DigitalProduct,
        ProductType.PERISHABLE: PerishableProduct,
    }

    @classmethod
    def create_product(cls, product_type: ProductType, **kwargs: Any) -> Product:
        """Instantiates and returns a concrete Product subclass safely based on Type.

        Args:
            product_type: The `ProductType` indicating which subclass to construct.
            **kwargs: Keyword arguments forwarded to the chosen subclass's
                constructor (e.g. `product_name`, `price`, `stock`, etc.).

        Returns:
            A newly constructed `Product` subclass instance.

        Raises:
            ValueError: If `product_type` is not a recognized/registered type.
            TypeError: If `kwargs` does not match the constructor signature
                of the resolved product class.
        """
        # Look up the concrete class registered for this product type
        product_class = cls._registry.get(product_type)

        if not product_class:
            raise ValueError(f"Unsupported product type provided: {product_type}")

        try:
            return product_class(**kwargs)
        except TypeError as e:
            # Re-raise with a clearer message indicating which class/kwargs failed
            raise TypeError(
                f"Missing or invalid keyword arguments for {product_class.__name__}: {e}"
            )
