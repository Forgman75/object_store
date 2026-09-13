import pytest
from src.products import Product, Smartphone, LawnGrass
from src.categories import Category
from src.base_product import BaseProduct


@pytest.fixture(autouse=True)
def reset_counters():
    """Сбрасывает счётчики перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0
    yield
    # После теста счётчики тоже можно сбросить
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_products():
    """Фикстура с набором товаров."""
    return [
        Product("iPhone 15", "512GB", 210000.0, 8),
        Product("Samsung S23", "256GB", 180000.0, 5),
    ]


@pytest.fixture
def sample_category(sample_products):
    """Фикстура с категорией, содержащей товары."""
    return Category("Смартфоны", "Описание смартфонов", sample_products)


@pytest.fixture
def sample2_products():
    """Создает набор тестовых продуктов."""
    p1 = Product("Iphone 15", "Смартфон", 100000.0, 5)
    p2 = Product("Samsung S24", "Смартфон", 80000.0, 3)
    p3 = Product("MacBook Pro", "Ноутбук", 250000.0, 0)
    return p1, p2, p3


@pytest.fixture
def sample2_category(sample2_products):
    """Создает тестовую категорию с продуктами."""
    p1, p2, p3 = sample2_products
    return Category("Электроника", "Техника Apple и Samsung", [p1, p2, p3])


@pytest.fixture
def sample_smartphone():
    return Smartphone(
        "iPhone 14", "Описание", 80000.0, 5, 95.5, "Pro", 256, "Black"
    )


@pytest.fixture
def sample_lawn_grass():
    return LawnGrass(
        "Трава", "Описание", 500.0, 10, "Россия", "7 дней", "Зеленый"
    )


@pytest.fixture
def sample3_category():
    return Category("Электроника", "Описание категории", [])


@pytest.fixture
def sample2_smartphone():
    """Смартфон для тестов."""
    return Smartphone(
        name="iPhone 15",
        description="Чёрный",
        price=100000.0,
        quantity=5,
        efficiency="Высокая",
        model="15 Pro",
        memory=256,
        color="Чёрный",
    )


@pytest.fixture
def sample_grass():
    """Газонная трава для тестов."""
    return LawnGrass(
        name="Газонная трава",
        description="Зелёная",
        price=500.0,
        quantity=20,
        country="Россия",
        germination_period=7,
        color="Тёмно-зелёный",
    )


class ConcreteProduct(BaseProduct):
    """Конкретная реализация BaseProduct для тестирования."""

    def __init__(self, name, description, price, quantity, **kwargs):
        super().__init__(name, description, price, quantity, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price


    def __add__(self, other):
        """Магический метод сложения. Возвращает сумму произведений цены на количество."""
        if type(self) is type(other):
            return (self.price * self.quantity) + (other.price * other.quantity)
        raise TypeError("Складывать можно только товары одного типа")


class AnotherProduct(BaseProduct):
    """Другая реализация для проверки __add__ с разными типами."""

    def __init__(self, name, description, price, quantity, **kwargs):
        super().__init__(name, description, price, quantity, **kwargs)

    def __str__(self):
        return f"Another: {self.name}"

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price


    def __add__(self, other):
        """Магический метод сложения. Возвращает сумму произведений цены на количество."""
        if type(self) is type(other):
            return (self.price * self.quantity) + (other.price * other.quantity)
        raise TypeError("Складывать можно только товары одного типа")





@pytest.fixture
def concrete_product():
    """Образец продукта для тестов."""
    return ConcreteProduct("Товар1", "Описание", 1000.0, 5)


@pytest.fixture
def another_product():
    """Другой продукт для тестов."""
    return AnotherProduct("Товар2", "Другое описание", 500.0, 10)


