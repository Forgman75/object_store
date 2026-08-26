from src.products import Product


class Category:
    """Класс категорий."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str):

        self.name = name
        self.description = description
        self.__products = []
        Category.category_count += 1
        

    # Метод добавления продукта
    def add_product(self, product: Product) -> None:
        """Добавляет продукт в приватный список и увеличивает счётчик."""
        self.__products.append(product)
        Category.product_count += 1


    def __repr__(self):
        return (
            f"Category("
            f"name={self.name!r}, "
            f"description={self.description!r})"
        )
