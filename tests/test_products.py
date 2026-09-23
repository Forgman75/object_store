import pytest
import re
from src.products import Product, Smartphone, LawnGrass


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
        TypeError, match="Складывать можно только товары одного типа"
    ):
        p1 + 100


def test_add_product_and_string_raises_error(sample_products):
    """Проверка, что сложение со строкой вызывает TypeError."""
    p1, _ = sample_products
    with pytest.raises(
        TypeError, match="Складывать можно только товары одного типа"
    ):
        p1 + "текст"


def test_add_product_and_none_raises_error(sample_products):
    """Проверка, что сложение с None вызывает TypeError."""
    p1, _ = sample_products
    with pytest.raises(
        TypeError, match="Складывать можно только товары одного типа"
    ):
        p1 + None


def test_smartphone_initialization():
    """Проверка создания экземпляра Smartphone и его атрибутов"""
    phone = Smartphone(
        "iPhone 14", "Описание", 80000.0, 5, 95.5, "Pro", 256, "Black"
    )

    assert phone.name == "iPhone 14"
    assert phone.price == 80000.0
    assert phone.quantity == 5
    # Проверка специфичных атрибутов
    assert phone.efficiency == 95.5
    assert phone.model == "Pro"
    assert phone.memory == 256
    assert phone.color == "Black"
    # Проверка наследования
    assert isinstance(phone, Product)


def test_lawn_grass_initialization():
    """Проверка создания экземпляра LawnGrass и его атрибутов"""
    grass = LawnGrass(
        "Трава", "Описание", 500.0, 10, "Россия", "7 дней", "Зеленый"
    )

    assert grass.name == "Трава"
    assert grass.price == 500.0
    assert grass.quantity == 10
    # Проверка специфичных атрибутов
    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"
    assert grass.color == "Зеленый"
    # Проверка наследования
    assert isinstance(grass, Product)


def test_smartphone_creation_logs_to_console(capsys):
    """При создании Smartphone в консоль выводится строка с параметрами."""
    Smartphone(
        "iPhone 15", "Чёрный", 100000.0, 5, "Высокая", "15 Pro", 256, "Чёрный"
    )
    captured = capsys.readouterr()

    # Проверяем, что выведено имя класса
    assert captured.out.startswith("Smartphone(")
    # Проверяем, что строки обёрнуты в кавычки (как в __repr__)
    assert "'iPhone 15'" in captured.out
    assert "'Чёрный'" in captured.out
    # Проверяем, что числа идут без кавычек
    assert "100000.0" in captured.out
    assert "256" in captured.out


def test_lawn_grass_creation_logs_to_console(capsys):
    """При создании LawnGrass в консоль выводится строка с параметрами."""
    LawnGrass("Газон", "Зелёная", 500.0, 20, "Россия", 7, "Тёмно-зелёный")
    captured = capsys.readouterr()

    assert captured.out.startswith("LawnGrass(")
    assert "'Газон'" in captured.out
    assert "500.0" in captured.out


def test_add_different_types_raises(sample_smartphone, sample_lawn_grass):
    """Сложение товаров разных типов вызывает TypeError."""
    with pytest.raises(TypeError):
        _ = sample_smartphone + sample_lawn_grass


def test_mixin_uses_repr_for_strings(capsys):
    """Строковые параметры должны быть обёрнуты в одинарные кавычки."""
    Smartphone("Test", "Desc", 1.0, 1, "E", "M", 1, "C")
    captured = capsys.readouterr()

    # Ищем паттерн: 'Test' (строка в кавычках)
    assert re.search(r"'Test'", captured.out)
    # И что число 1.0 идёт без кавычек
    assert re.search(r"[^']1\.0[^']", captured.out)


def test_mixin_logs_kwargs(capsys):
    """Если параметры переданы как kwargs, они тоже логируются."""
    Smartphone(
        name="Phone",
        description="D",
        price=100.0,
        quantity=1,
        efficiency="E",
        model="M",
        memory=64,
        color="Black",
    )
    captured = capsys.readouterr()
    # В выводе должны быть именованные параметры
    assert "name=" in captured.out
    assert "price=" in captured.out


def test_mixin_does_not_break_initialization():
    """Миксин не должен мешать инициализации атрибутов."""
    phone = Smartphone("iPhone", "D", 100.0, 2, "High", "Pro", 128, "White")
    assert phone.name == "iPhone"
    assert phone.price == 100.0
    assert phone.model == "Pro"
