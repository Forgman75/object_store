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
        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только объекты классов Product или его наследников"
            )

        self.__products.append(product)
        Category.product_count += 1

    # Геттер списка товаров
    @property
    def products(self) -> str:
        """
        Возвращает строку со списком товаров в формате:
        'Название продукта, X руб. Остаток: X шт.\n'
        """
        return "\n".join(str(product) for product in self.__products)

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

    def __str__(self):
        """Строковое отображение категории. 
        Рассчитывает общее количество товаров на складе (сумма quantity)."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


class CategoryIterator:
    """Итератор для перебора товаров одной категории."""

    def __init__(self, category):
        """
        Принимает объект категории и инициализирует итератор.
        
        :param category: объект класса Category
        """
        self._category = category
        self._products = category.product_list  # список товаров категории
        self._index = 0                      # текущая позиция в списке

    def __iter__(self):
        """Возвращает сам объект итератора."""
        return self

    def __next__(self):
        """
        Возвращает очередной товар категории.
        Когда товары закончатся — возбуждает StopIteration.
        """
        if self._index < len(self._products):
            product = self._products[self._index]
            self._index += 1
            return product
        else:
            raise StopIteration
