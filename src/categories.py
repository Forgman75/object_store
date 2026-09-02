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
        self.__products = products if products else []
        Category.category_count += 1
        Category.product_count += len(self.__products)

    # Метод добавления продукта
    def add_product(self, product: Product) -> None:
        """Добавляет продукт в приватный список и увеличивает счётчик."""
        self.__products.append(product)
        Category.product_count += 1

    # Геттер списка товаров
    @property
    def products(self) -> str:
        """
        Возвращает строку со списком товаров в формате:
        'Название продукта, X руб. Остаток: X шт.\n'
        """
        result = ""
        for product in self.__products:
            result += (
                f"{product.name}, {product.price} руб. "
                f"Остаток: {product.quantity} шт.\n"
            )
        return result

    @property
    def product_list(self) -> list:
        """Возвращает список объектов товаров."""
        return self.__products

    @property
    def product_count_instance(self) -> int:
        """Количество товаров в данной категории."""
        return len(self.__products)

    def __repr__(self):
        return (
            f"Category("
            f"name={self.name!r}, "
            f"description={self.description!r}, "
            f"__products={self.products})"
        )
