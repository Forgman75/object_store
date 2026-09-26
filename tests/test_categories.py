import pytest
from src.products import Product, Smartphone, LawnGrass
from src.categories import Category, CategoryIterator, Order
from src.base_info import BaseInfo
from src.base_product import ProductZeroQuantityError


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
    # 5 (Iphone) + 3 (Samsung) + 1 (MacBook) = 9
    assert str(sample2_category) == "Электроника, количество продуктов: 9 шт."


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


def test_add_valid_products(
    sample3_category, sample_smartphone, sample_lawn_grass
):
    """Проверка успешного добавления допустимых объектов
    (Product и его наследников)"""
    base_product = Product("Базовый товар", "Описание", 100.0, 1)

    sample3_category.add_product(sample_smartphone)
    sample3_category.add_product(sample_lawn_grass)
    sample3_category.add_product(base_product)

    # Проверяем, что все 3 объекта добавлены
    assert len(sample3_category.product_list) == 3
    assert sample_smartphone in sample3_category.product_list
    assert sample_lawn_grass in sample3_category.product_list
    assert base_product in sample3_category.product_list


def test_add_invalid_products(sample3_category):
    """Проверка, что метод выбрасывает TypeError при добавлении
    недопустимых типов"""
    invalid_items = ["Строка", 123, {"name": "Словарь"}, None, [1, 2, 3]]

    for item in invalid_items:
        with pytest.raises(
            TypeError,
            match=(
                "Можно добавлять только объекты классов Product "
                "или его наследников"
            ),
        ):
            sample3_category.add_product(item)


def test_cannot_instantiate_base_info_directly():
    """BaseInfo — абстрактный, создать его напрямую нельзя."""
    with pytest.raises(TypeError):
        BaseInfo("name", "description")


def test_category_is_subclass_of_base_info():
    """Category наследуется от BaseInfo."""
    assert issubclass(Category, BaseInfo)


def test_order_is_subclass_of_base_info():
    """Order наследуется от BaseInfo."""
    assert issubclass(Order, BaseInfo)


def test_category_has_name_and_description():
    """У Category есть атрибуты name и description из BaseInfo."""
    cat = Category("Электроника", "Техника")
    assert cat.name == "Электроника"
    assert cat.description == "Техника"


def test_order_has_name_and_description(sample_smartphone):
    """У Order есть атрибуты name и description из BaseInfo."""
    order = Order(sample_smartphone, 2)
    assert hasattr(order, "name")
    assert hasattr(order, "description")


def test_order_creation_with_auto_name(sample2_smartphone):
    """Если name/description не переданы, они формируются автоматически."""
    order = Order(sample2_smartphone, 2)

    assert "iPhone 15" in order.name
    assert (
        "2" in order.description
        or sample2_smartphone.name in order.description
    )


def test_order_creation_with_custom_name(sample_smartphone):
    """Можно передать свои name и description."""
    order = Order(
        sample_smartphone, 3, name="Заказ №42", description="Подарок другу"
    )
    assert order.name == "Заказ №42"
    assert order.description == "Подарок другу"


def test_order_total_amount(sample2_smartphone):
    """Итоговая стоимость = цена × количество."""
    order = Order(sample2_smartphone, 3)
    assert order.total_amount == 100000.0 * 3


def test_order_total_amount_recalculated_on_price_change(sample2_smartphone):
    """При изменении цены товара total_amount пересчитывается."""
    order = Order(sample2_smartphone, 2)
    assert order.total_amount == 200000.0

    sample2_smartphone.price = 120000.0
    assert order.total_amount == 240000.0  # Автоматический пересчёт


def test_order_with_lawn_grass(sample_grass):
    """Заказ можно создать и для LawnGrass."""
    order = Order(sample_grass, 10)
    assert order.total_amount == 500.0 * 10


def test_order_rejects_non_product():
    """Нельзя создать заказ с объектом, не являющимся Product."""
    with pytest.raises(TypeError):
        Order("не товар", 5)

    with pytest.raises(TypeError):
        Order(12345, 1)


def test_order_rejects_zero_quantity(sample_smartphone):
    """Нельзя создать заказ с количеством 0."""
    with pytest.raises(ValueError):
        Order(sample_smartphone, 0)


def test_create_order_with_zero_quantity_product_raises(
    empty_category, zero_quantity_lawn_grass_data
):
    """Создание заказа на товар с quantity=0 вызывает ProductZeroQuantityError."""
    with pytest.raises(ProductZeroQuantityError):
        product = LawnGrass(**zero_quantity_lawn_grass_data)
        Order(product, quantity=3)


def test_order_error_is_value_error(zero_quantity_lawn_grass_data):
    """ProductZeroQuantityError перехватывается как ValueError."""
    with pytest.raises(ValueError):
        product = LawnGrass(**zero_quantity_lawn_grass_data)
        Order(product, quantity=3)


def test_order_rejects_negative_quantity(sample_smartphone):
    """Нельзя создать заказ с отрицательным количеством."""
    with pytest.raises(ValueError):
        Order(sample_smartphone, -5)


def test_order_str_representation(sample2_smartphone):
    """Проверяем строковое представление заказа."""
    order = Order(sample2_smartphone, 2, name="Заказ №1")
    result = str(order)

    assert "Заказ №1" in result
    assert "iPhone 15" in result
    assert "2 шт." in result
    assert "200000.0 руб." in result


def test_order_contains_only_one_product(sample_smartphone):
    """В заказе может быть только один товар — проверяем, что нет списка."""
    order = Order(sample_smartphone, 1)
    # product — это одиночный объект, а не список
    assert not isinstance(order.product, list)
    assert order.product is sample_smartphone


def test_both_have_same_base_attributes(sample_smartphone):
    """У Order и Category есть одинаковые атрибуты name и description."""
    cat = Category("Техника", "Описание категории")
    order = Order(
        sample_smartphone, 1, name="Заказ", description="Описание заказа"
    )

    assert hasattr(cat, "name") and hasattr(order, "name")
    assert hasattr(cat, "description") and hasattr(order, "description")

    assert cat.name == "Техника"
    assert order.name == "Заказ"


def test_both_share_abc_ancestor():
    """Оба класса имеют общего предка BaseInfo."""
    assert BaseInfo in Category.__mro__
    assert BaseInfo in Order.__mro__


def test_average_price_with_products(category_with_products):
    """Средний ценник для категории с товарами."""
    # (100000 + 500) / 2 = 50250.0
    assert category_with_products.middle_price() == 50250.0


def test_average_price_empty_category(empty_category):
    """Средний ценник пустой категории — 0."""
    assert empty_category.middle_price() == 0


def test_try_except_else_finally_success(capsys):
    """Проверяем работу try/except/else/finally при успехе."""
    category = Category("Тест", "Описание")
    try:
        product = Smartphone(
            "iPhone", "Чёрный", 100000.0, 5, "Высокая", "15", 128, "Чёрный"
        )
        category.add_product(product)
    except ProductZeroQuantityError:
        print("Ошибка")
    else:
        print("Товар добавлен")
    finally:
        print("Обработка завершена")

    captured = capsys.readouterr()
    assert "Товар добавлен" in captured.out
    assert "Обработка завершена" in captured.out
    assert "Ошибка" not in captured.out


def test_try_except_else_finally_failure(capsys):
    """Проверяем работу try/except/else/finally при ошибке."""
    category = Category("Тест", "Описание")
    try:
        product = Smartphone(
            "iPhone", "Чёрный", 100000.0, 0, "Высокая", "15", 128, "Чёрный"
        )
        category.add_product(product)
    except ProductZeroQuantityError:
        print("Ошибка")
    else:
        print("Товар добавлен")
    finally:
        print("Обработка завершена")

    captured = capsys.readouterr()
    assert "Ошибка" in captured.out
    assert "Обработка завершена" in captured.out
    assert "Товар добавлен" not in captured.out


@pytest.mark.parametrize("quantity", [0])
def test_parametrized_zero_quantity(quantity):
    """Параметризованный тест для нулевого количества."""
    with pytest.raises(ProductZeroQuantityError):
        LawnGrass("Трава", "Описание", 100.0, quantity, "Россия", 5, "Зелёный")


def test_category_not_modified_on_error(
    empty_category, zero_quantity_smartphone_data
):
    """При ошибке создания товара категория НЕ должна измениться."""
    initial_count = len(empty_category._Category__products)
    with pytest.raises(ProductZeroQuantityError):
        product = Smartphone(**zero_quantity_smartphone_data)
        empty_category.add_product(product)
    assert len(empty_category._Category__products) == initial_count
