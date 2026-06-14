"""Defines `DigitalProduct`, a `Product` subclass for downloadable goods
that have no shipping cost and unlimited stock."""

from Product import Product

# Digital products never incur a shipping charge
SHIPPING_FEE = 0


class DigitalProduct(Product):
    """A downloadable product with no shipping cost and unlimited stock.

    Purchasing a digital product does not reduce its available stock,
    since digital goods can be duplicated/downloaded indefinitely.
    """

    def __init__(
        self,
        product_name: str,
        price: float,
        file_size_in_mb: float,
        download_url: str,
    ) -> None:
        """Initialize a digital product.

        Note that no `stock` argument is accepted; digital products use the
        base class's default stock value and never have it decremented.

        Args:
            product_name: The human-readable name of the product.
            price: The unit price of the product.
            file_size_in_mb: The size of the downloadable file, in megabytes.
            download_url: The URL from which the product can be downloaded.
        """
        super().__init__(product_name, price)
        self.file_size_in_mb: float = file_size_in_mb
        # Private since the download link should not be exposed/modified directly
        self.__download_url: str = download_url

    def _set_stock(self, value: int) -> None:
        """Override stock-setting to be a no-op.

        Digital products have unlimited stock, so any attempt to change
        stock (e.g. when an order is placed) is ignored by re-setting the
        stock to its current, unchanged value.

        Args:
            value: The requested new stock value (ignored).
        """
        return super()._set_stock(self._stock)

    def _get_shipping_cost(self) -> float:
        """Return the shipping cost for a digital product.

        Returns:
            Always 0, since digital products incur no shipping cost.
        """
        return SHIPPING_FEE

    def display_product_details(self) -> None:
        """Print common product details plus the digital-specific file size."""
        super().display_product_details()
        print(f"File size: {self.file_size_in_mb} MB")
        print("==============================")
