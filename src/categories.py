from src.products import Product
from src.base_info import BaseInfo
from typing import Optional


class Category(BaseInfo):
    """Класс категорий."""

    category_count = 0
    product_count = 0

    def __init__(
        self, name: str, description: str, products: Optional[list[Product]]=None
    ):

        super().__init__(name, description)
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


class Order(BaseInfo):
    """
    Класс, представляющий заказ.
    В заказе может быть указан только один товар.
    """

    def __init__(self, product: Product, quantity: int, name: str = "", description: str = ""):

        if not isinstance(product, Product):
            raise TypeError("В заказе может быть указан только товар класса Product или его наследников")
        if quantity <= 0:
            raise ValueError("Количество товара должно быть больше нуля")
        
        # Если имя/описание не переданы — формируем их автоматически
        if not name:
            name = f"Заказ на {product.name}"
        if not description:
            description = f"Покупка товара '{product.name}' в количестве {quantity} шт."

        super().__init__(name, description)
        
        self.product = product
        self.quantity = quantity

    @property
    def total_amount(self) -> float:
        """Итоговая стоимость заказа."""
        return self.product.price * self.quantity

    def __str__(self):
        return (
            f"{self.name}: {self.product.name} x {self.quantity} шт. "
            f"= {self.total_amount} руб."
        )

    def __repr__(self):
        return (
            f"Order(name={self.name!r}, product={self.product.name!r}, "
            f"quantity={self.quantity}, total_amount={self.total_amount})"
        )

