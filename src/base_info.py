from abc import ABC, abstractmethod


class BaseInfo(ABC):
    """
    Общий абстрактный класс, содержащий свойства, 
    общие для категорий и заказов.
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def __str__(self):
        pass
