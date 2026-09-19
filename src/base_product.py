from abc import ABC, abstractmethod


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
