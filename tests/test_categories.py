import pytest
from src.products import Product
from src.categories import Category, CategoryIterator


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


def test_category_str_with_products(sample2_category):
    """Проверка строкового представления категории с товарами.
    Считается сумма quantity, а не количество наименований."""
    # 5 (Iphone) + 3 (Samsung) + 0 (MacBook) = 8
    assert str(sample2_category) == "Электроника, количество продуктов: 8 шт."


def test_category_str_empty():
    """Проверка строкового представления пустой категории."""
    empty_cat = Category("Пустая", "Без товаров", [])
    assert str(empty_cat) == "Пустая, количество продуктов: 0 шт."


def test_iterator_next_method(sample2_category, sample2_products):
    """Проверка работы метода __next__ и возврата товаров по одному."""
    p1, p2, p3 = sample2_products
    iterator = CategoryIterator(sample2_category)

    assert next(iterator) is p1
    assert next(iterator) is p2
    assert next(iterator) is p3


def test_iterator_stop_iteration(sample2_category):
    """Проверка, что после окончания товаров выбрасывается StopIteration."""
    iterator = CategoryIterator(sample2_category)

    # Пропускаем все 3 товара
    next(iterator)
    next(iterator)
    next(iterator)

    # На 4-й вызов должно упасть с StopIteration
    with pytest.raises(StopIteration):
        next(iterator)


def test_iterator_in_for_loop(sample2_category, sample2_products):
    """Проверка, что итератор корректно работает в цикле for."""
    p1, p2, p3 = sample2_products
    iterator = CategoryIterator(sample2_category)

    products_from_loop = [product for product in iterator]

    assert len(products_from_loop) == 3
    assert products_from_loop == [p1, p2, p3]


def test_iterator_empty_category():
    """Проверка итератора для пустой категории."""
    empty_cat = Category("Пустая", "Без товаров", [])
    iterator = CategoryIterator(empty_cat)

    with pytest.raises(StopIteration):
        next(iterator)
