import pytest
from src.products import Product, Smartphone, LawnGrass
from src.categories import Category


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
