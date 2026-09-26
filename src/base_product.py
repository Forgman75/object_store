from abc import ABC, abstractmethod


class ProductZeroQuantityError(ValueError):
    """Исключение, вызываемое при попытке добавить товар
    с нулевым количеством."""

    def __init__(
        self, message="Товар с нулевым количеством не может быть добавлен"
    ):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class BaseProduct(ABC):
    """
    Абстрактный базовый класс
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        color: str = "",
        *args,
        **kwargs,
    ):

        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.color = color

    @property
    @abstractmethod
    def price(self):
        pass

    @price.setter
    @abstractmethod
    def price(self, value):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass
