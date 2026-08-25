from src.products import Product


class Category:
    """Класс категорий."""

    category_count = 0
    product_count = 0

    def __init__(
        self, name: str, description: str, products: list[Product] | None
    ):

        self.name = name
        self.description = description
        self.products = products if products else []
        Category.category_count += 1
        Category.product_count += len(self.products)

    def __repr__(self):
        return f"Category({self.name}, {self.description}, {self.products})"
