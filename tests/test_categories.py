import pytest
from src.products import Product
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


def test_category_initialization(sample_products):
    """Тест инициализации Category."""
    category = Category("Смартфоны", "Описание", sample_products)

    assert category.name == "Смартфоны"
    assert category.description == "Описание"
    assert Category.category_count == 1


def test_category_count_increments():
    """Тест счётчика категорий."""
    Category("A", "A", [])
    Category("B", "B", [])
    Category("C", "C", [])
    assert Category.category_count == 3


def test_product_count_with_initial_products(sample_products):
    """Тест product_count: учитывает товары при создании."""
    Category("Смартфоны", "Описание", sample_products)
    assert Category.product_count == 2


def test_product_count_with_multiple_categories(sample_products):
    """Тест product_count: суммирует товары из всех категорий."""
    Category("A", "A", sample_products)  # 2 товара
    Category("B", "B", [Product("X", "Y", 100.0, 1)])  # 1 товар
    assert Category.product_count == 3


def test_category_with_empty_products():
    """Тест создания категории без товаров."""
    category = Category("Пустая", "Описание", None)
    assert category.products == ""
    assert category.product_count_instance == 0


def test_category_with_none_products():
    """Тест создания категории с None вместо списка."""
    category = Category("Пустая", "Описание", None)
    assert Category.product_count == 0


def test_products_getter_returns_string(sample_category):
    """Тест геттера products: возвращает строку."""
    result = sample_category.products
    assert isinstance(result, str)


def test_products_getter_format(sample_category):
    """Тест геттера products: корректный формат строки."""
    result = sample_category.products

    # Проверяем, что в строке есть названия товаров
    assert "iPhone 15" in result
    assert "Samsung S23" in result

    # Проверяем наличие ключевых частей формата
    assert "руб." in result
    assert "Остаток:" in result
    assert "шт." in result


def test_products_getter_contains_price_and_quantity(sample_category):
    """Тест геттера products: содержит цену и количество."""
    result = sample_category.products
    assert "210000.0" in result
    assert "8" in result
    assert "180000.0" in result
    assert "5" in result


def test_products_getter_empty_category():
    """Тест геттера products: пустая категория."""
    category = Category("Пустая", "Описание", [])
    assert category.products == ""


def test_product_count_instance_initial(sample_category):
    """Тест product_count_instance: начальное значение."""
    assert sample_category.product_count_instance == 2


def test_product_count_instance_after_add(sample_category):
    """Тест product_count_instance: после добавления товара."""
    new_product = Product("Новый товар", "Описание", 1000.0, 10)
    sample_category.add_product(new_product)
    assert sample_category.product_count_instance == 3


def test_product_count_instance_empty():
    """Тест product_count_instance: пустая категория."""
    category = Category("Пустая", "Описание", [])
    assert category.product_count_instance == 0


def test_add_product(sample_category):
    """Тест add_product: товар добавляется в список."""
    new_product = Product("Новый товар", "Описание", 1000.0, 10)
    sample_category.add_product(new_product)

    # Проверяем через геттер products
    assert "Новый товар" in sample_category.products


def test_add_product_increments_global_counter(sample_category):
    """Тест add_product: увеличивает общий счётчик product_count."""
    initial_count = Category.product_count
    new_product = Product("Новый товар", "Описание", 1000.0, 10)
    sample_category.add_product(new_product)

    assert Category.product_count == initial_count + 1


def test_add_product_increments_instance_counter(sample_category):
    """Тест add_product: увеличивает счётчик конкретной категории."""
    initial_count = sample_category.product_count_instance
    new_product = Product("Новый товар", "Описание", 1000.0, 10)
    sample_category.add_product(new_product)

    assert sample_category.product_count_instance == initial_count + 1


def test_add_multiple_products():
    """Тест add_product: добавление нескольких товаров."""
    category = Category("Тест", "Тест", [])
    for i in range(5):
        category.add_product(Product(f"Товар {i}", "Описание", 100.0, 1))

    assert category.product_count_instance == 5
    assert Category.product_count == 5
