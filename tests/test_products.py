import pytest
from src.products import Product


def test_price_getter():
    """Тест геттера price: возвращает корректное значение."""
    product = Product("iPhone 15", "512GB", 210000.0, 8)
    assert product.price == 210000.0


def test_price_getter_float():
    """Тест геттера price: возвращает float."""
    product = Product("Test", "Test", 99.99, 1)
    assert product.price == 99.99
    assert isinstance(product.price, float)


def test_price_setter_valid():
    """Тест сеттера price: установка корректной цены."""
    product = Product("iPhone 15", "512GB", 210000.0, 8)
    product.price = 180000.0
    assert product.price == 180000.0


def test_price_setter_negative(capsys):
    """Тест сеттера price: отрицательная цена отклоняется."""
    product = Product("iPhone 15", "512GB", 210000.0, 8)
    product.price = -100

    # Цена НЕ должна измениться
    assert product.price == 210000.0

    # Должно быть сообщение в stdout
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_price_setter_zero(capsys):
    """Тест сеттера price: нулевая цена отклоняется."""
    product = Product("iPhone 15", "512GB", 210000.0, 8)
    product.price = 0

    assert product.price == 210000.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_price_setter_positive():
    """Тест сеттера price: положительная цена устанавливается."""
    product = Product("iPhone 15", "512GB", 210000.0, 8)
    product.price = 800
    assert product.price == 800


def test_new_product_from_dict():
    """Тест new_product: создание объекта из словаря."""
    data = {
        "name": "Samsung Galaxy S23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5,
    }
    product = Product.new_product(data)

    assert isinstance(product, Product)
    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, Серый цвет, 200MP камера"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_new_product_creates_new_instance():
    """Тест new_product: каждый вызов создаёт новый объект."""
    data = {"name": "A", "description": "B", "price": 100.0, "quantity": 1}
    p1 = Product.new_product(data)
    p2 = Product.new_product(data)

    assert p1 is not p2  # Разные объекты
    assert p1.name == p2.name  # Но с одинаковыми данными


def test_new_product_with_different_values():
    """Тест new_product: разные значения корректно передаются."""
    data = {"name": "X", "description": "Y", "price": 1.5, "quantity": 100}
    product = Product.new_product(data)

    assert product.price == 1.5
    assert product.quantity == 100


def test_new_product_without_existing_list():
    """Тест: создание продукта без передачи списка существующих."""
    data = {"name": "A", "description": "B", "price": 100.0, "quantity": 1}
    product = Product.new_product(data)

    assert product.name == "A"
    assert product.quantity == 1


def test_new_product_with_empty_existing_list():
    """Тест: создание продукта при пустом списке existing_products."""
    data = {"name": "A", "description": "B", "price": 100.0, "quantity": 1}
    product = Product.new_product(data, existing_products=[])

    assert product.name == "A"
    assert product.quantity == 1


def test_new_product_with_none_existing_list():
    """Тест: создание продукта при existing_products=None."""
    data = {"name": "A", "description": "B", "price": 100.0, "quantity": 1}
    product = Product.new_product(data, existing_products=None)

    assert product.name == "A"


def test_new_product_updates_quantity_when_duplicate():
    """Тест: при дубликате количество увеличивается."""
    existing = [Product("iPhone", "Desc", 100000.0, 5)]
    data = {
        "name": "iPhone",
        "description": "New",
        "price": 100000.0,
        "quantity": 3,
    }

    result = Product.new_product(data, existing_products=existing)

    # Количество должно увеличиться: 5 + 3 = 8
    assert result.quantity == 8
    # И в исходном списке тоже обновилось (побочный эффект)
    assert existing[0].quantity == 8


def test_new_product_updates_price_when_new_is_higher():
    """Тест: при дубликате цена обновляется, если новая ВЫШЕ."""
    existing = [Product("iPhone", "Desc", 100000.0, 5)]
    data = {
        "name": "iPhone",
        "description": "New",
        "price": 150000.0,
        "quantity": 2,
    }

    result = Product.new_product(data, existing_products=existing)

    assert result.price == 150000.0  # Цена обновилась
    assert existing[0].price == 150000.0


def test_new_product_keeps_price_when_new_is_lower():
    """Тест: при дубликате цена НЕ обновляется, если новая НИЖЕ."""
    existing = [Product("iPhone", "Desc", 100000.0, 5)]
    data = {
        "name": "iPhone",
        "description": "New",
        "price": 50000.0,
        "quantity": 2,
    }

    result = Product.new_product(data, existing_products=existing)

    assert result.price == 100000.0  # Цена осталась старой
    assert existing[0].price == 100000.0


def test_new_product_creates_new_when_no_duplicate():
    """Тест: если дубликата нет в списке — создаётся новый продукт."""
    existing = [Product("iPhone", "Desc", 100000.0, 5)]
    data = {
        "name": "Samsung",
        "description": "Android",
        "price": 80000.0,
        "quantity": 3,
    }

    result = Product.new_product(data, existing_products=existing)

    # Должен создаться новый объект
    assert result is not existing[0]
    assert result.name == "Samsung"
    assert result.quantity == 3
    # Исходный список не изменился
    assert existing[0].name == "iPhone"
    assert existing[0].quantity == 5


def test_product_str_standard(sample2_products):
    """Проверка строкового представления обычного продукта."""
    p1, p2, _ = sample2_products
    assert str(p1) == "Iphone 15, 100000.0 руб. Остаток: 5 шт."
    assert str(p2) == "Samsung S24, 80000.0 руб. Остаток: 3 шт."


def test_product_str_zero_quantity(sample2_products):
    """Проверка строкового представления продукта с нулевым остатком."""
    _, _, p3 = sample2_products
    assert str(p3) == "MacBook Pro, 250000.0 руб. Остаток: 0 шт."


def test_add_two_products(sample2_products):
    """Проверка сложения двух продуктов (сумма их стоимости на складе)."""
    p1, p2, _ = sample2_products
    # p1: 100000.0 * 5 = 500000.0
    # p2: 80000.0 * 3 = 240000.0
    # Итого: 740000.0
    assert p1 + p2 == 740000.0


def test_add_product_and_integer_raises_error(sample_products):
    """Проверка, что сложение с числом вызывает TypeError."""
    p1, _ = sample_products
    with pytest.raises(
        TypeError, match="Складывать можно только объекты класса Product"
    ):
        p1 + 100


def test_add_product_and_string_raises_error(sample_products):
    """Проверка, что сложение со строкой вызывает TypeError."""
    p1, _ = sample_products
    with pytest.raises(
        TypeError, match="Складывать можно только объекты класса Product"
    ):
        p1 + "текст"


def test_add_product_and_none_raises_error(sample_products):
    """Проверка, что сложение с None вызывает TypeError."""
    p1, _ = sample_products
    with pytest.raises(
        TypeError, match="Складывать можно только объекты класса Product"
    ):
        p1 + None
