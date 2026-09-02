class Product:
    """Класс, представляющий товар."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @classmethod
    def new_product(
        cls, product_data: dict, existing_products: list = None
    ) -> "Product":
        """
        Создает новый продукт или обновляет существующий.

        :param product_data: Словарь с данными товара
        :param existing_products: Список существующих товаров
        для проверки дубликатов
        :return: Объект Product
        """

        name = product_data.get("name")
        description = product_data.get("description")
        price = product_data.get("price")
        quantity = product_data.get("quantity")

        # Если передан список товаров, проверяем наличие дубликата
        if existing_products:
            for product in existing_products:
                if product.name == name:
                    # Товар найден - обновляем количество и цену
                    product.quantity += quantity
                    if price > product.price:
                        product.price = price
                    return product

        # Если дубликат не найден - создаем новый товар
        return cls(name, description, price, quantity)

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    def __repr__(self):
        return (
            f"Product("
            f"name={self.name!r}, "
            f"description={self.description!r}, "
            f"__price={self.__price}, "
            f"quantity={self.quantity})"
        )

    def __str__(self):
        """Строковое отображение продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

