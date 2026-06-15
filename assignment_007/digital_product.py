from product import Product


class DigitalProduct(Product):

    def __init__(
        self,
        name,
        price,
        file_size,
        download_url
    ):
        super().__init__(name, price, 999999)

        self.file_size = file_size
        self.download_url = download_url

    def calculate_total(self, quantity):
        return self.price * quantity

    def get_details(self):

        return (
            f"{self.product_id} | "
            f"{self.name} | "
            f"${self.price:.2f} | "
            f"Digital | "
            f"{self.file_size} MB"
        )