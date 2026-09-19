from src.base_product import BaseProduct


class LogCreationMixin:
    """
    Миксин реализует конструктор и логирует создание объекта.
    """

    def __init__(self, *args, **kwargs):
        # Получаем имя именно того класса, объект которого создается
        class_name = self.__class__.__name__

        # Преобразуем аргументы в их строковое представление (repr)
        args_repr = [repr(arg) for arg in args]
        kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]

        # Собираем все параметры в одну строку через запятую
        params = ", ".join(args_repr + kwargs_repr)

        # Печатаем информацию в консоль
        print(f"{class_name}({params})")

        # Передаем управление и ВСЕ аргументы дальше по цепочке MRO
        #  (в BaseProduct)
        super().__init__(*args, **kwargs)


class Product(LogCreationMixin, BaseProduct):
    """Класс, представляющий товар."""

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
        price = product_data.get("price")
        quantity = product_data.get("quantity")

        # Если передан список товаров, проверяем наличие дубликата
        if existing_products:
            for product in existing_products:
                if product.name == name and type(product) is cls:
                    # Товар найден - обновляем количество и цену
                    product.quantity += quantity
                    if price > product.price:
                        product.price = price
                    return product

        # Если дубликат не найден - создаем новый товар
        return cls(**product_data)

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
            f"quantity={self.quantity}, "
            f"color={self.color!r})"
        )

    def __str__(self):
        """Строковое отображение продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Магический метод сложения. Возвращает сумму произведений цены
        на количество."""
        if type(self) is type(other):
            return (self.price * self.quantity) + (
                other.price * other.quantity
            )
        raise TypeError("Складывать можно только товары одного типа")


class Smartphone(Product):
    """Класс, представляющий смартфон."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: str,
        model: str,
        memory: int,
        color: str,
        **kwargs,
    ):
        super().__init__(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            efficiency=efficiency,
            model=model,
            memory=memory,
            color=color,
            **kwargs,
        )
        self.efficiency = efficiency
        self.model = model
        self.memory = memory

    def __repr__(self):
        return (
            f"Smartphone("
            f"name={self.name!r}, "
            f"description={self.description!r}, "
            f"price={self.price}, "
            f"quantity={self.quantity}, "
            f"color={self.color!r}, "
            f"efficiency={self.efficiency!r}, "
            f"model={self.model!r}, "
            f"memory={self.memory})"
        )

    def __str__(self):
        return (
            f"{self.name} ({self.model}), "
            f"{self.efficiency}, "
            f"{self.memory} ГБ, "
            f"{self.color}, "
            f"{self.price} руб. Остаток: {self.quantity} шт."
        )


class LawnGrass(Product):
    """Класс, представляющий газонную траву."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
        color: str,
        **kwargs,
    ):
        super().__init__(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            country=country,
            germination_period=germination_period,
            color=color,
            **kwargs,
        )
        self.country = country
        self.germination_period = germination_period

    def __repr__(self):
        return (
            f"LawnGrass("
            f"name={self.name!r}, "
            f"description={self.description!r}, "
            f"price={self.price}, "
            f"quantity={self.quantity}, "
            f"color={self.color!r}, "
            f"country={self.country!r}, "
            f"germination_period={self.germination_period})"
        )

    def __str__(self):
        return (
            f"{self.name}, "
            f"{self.country}, "
            f"прорастание {self.germination_period} дн., "
            f"{self.color}, "
            f"{self.price} руб. Остаток: {self.quantity} шт."
        )
