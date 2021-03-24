from products.models import Product


class ProductAssignment:
    def __init__(self, product: Product, count: int):
        self.product = product
        self.count = count

    def __dict__(self):
        return {
            "product": self.product,
            "count": self.count
        }

    def __eq__(self, other):
        return self.product == other.product
