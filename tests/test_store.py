import json
import pytest
from src.products import Product
from src.categories import Category
from src.load_file import load_data_from_json


@pytest.fixture(autouse=True)
def reset_class_attributes():
    """
    Фикстура, которая автоматически выполняется перед каждым тестом.
    Сбрасывает атрибуты класса в ноль, чтобы тесты были изолированы
    и не влияли друг на друга.
    """
    Category.category_count = 0
    Category.product_count = 0
    yield


def test_product_initialization():
    """Проверка корректности инициализации объекта Product."""
    product = Product("Nokia 3310", "Легендарная надежность", 2500.0, 100)

    assert product.name == "Nokia 3310"
    assert product.description == "Легендарная надежность"
    assert product.price == 2500.0
    assert product.quantity == 100
    assert isinstance(product.price, float)
    assert isinstance(product.quantity, int)


def test_category_initialization():
    """Проверка корректности инициализации объекта Category."""
    p1 = Product("Товар 1", "Описание 1", 100.0, 5)
    p2 = Product("Товар 2", "Описание 2", 200.0, 10)

    category = Category("Электроника", "Гаджеты и устройства", [p1, p2])

    assert category.name == "Электроника"
    assert category.description == "Гаджеты и устройства"
    assert len(category.products) == 2
    # Проверяем, что в списке лежат именно объекты Product, а не словари
    assert isinstance(category.products[0], Product)
    assert category.products[0] is p1  # Проверка на идентичность объектов


def test_category_and_product_counts():
    """Проверка автоматического подсчета количества категорий и товаров."""
    # Изначально (благодаря фикстуре) счетчики равны 0
    assert Category.category_count == 0
    assert Category.product_count == 0

    # Создаем первую категорию с 2 товарами
    p1, p2 = Product("P1", "D", 10.0, 1), Product("P2", "D", 20.0, 2)
    cat1 = Category("Категория 1", "Desc", [p1, p2])

    assert Category.category_count == 1
    assert Category.product_count == 2

    # Создаем вторую категорию с 3 товарами
    p3, p4, p5 = (
        Product("P3", "D", 30.0, 3),
        Product("P4", "D", 40.0, 4),
        Product("P5", "D", 50.0, 5),
    )
    cat2 = Category("Категория 2", "Desc", [p3, p4, p5])

    # Счетчики должны просуммироваться
    assert Category.category_count == 2
    assert Category.product_count == 5


def test_load_data_from_json(tmp_path):
    """
    Проверка правильности работы функции load_data_from_json.
    Фикстура tmp_path предоставляет временную директорию, которая
    автоматически очищается после завершения тестов.
    """
    # 1. Подготовка тестовых данных
    json_data = [
        {
            "name": "Смартфоны",
            "description": "Мобильные устройства",
            "products": [
                {
                    "name": "iPhone",
                    "description": "Apple",
                    "price": 100000.0,
                    "quantity": 5,
                },
                {
                    "name": "Samsung",
                    "description": "Android",
                    "price": 80000.0,
                    "quantity": 10,
                },
            ],
        },
        {
            "name": "Телевизоры",
            "description": "Для кино",
            "products": [
                {
                    "name": "LG OLED",
                    "description": "4K",
                    "price": 150000.0,
                    "quantity": 2,
                }
            ],
        },
    ]

    # Создаем временный файл
    file_path = tmp_path / "test_data.json"
    file_path.write_text(json.dumps(json_data), encoding="utf-8")

    # Вызов тестируемой функции
    categories = load_data_from_json(str(file_path))

    # Проверка результатов
    assert isinstance(categories, list)
    assert len(categories) == 2

    # Проверка первой категории
    assert categories[0].name == "Смартфоны"
    assert len(categories[0].products) == 2
    assert isinstance(categories[0].products[0], Product)
    assert categories[0].products[0].name == "iPhone"
    assert categories[0].products[0].price == 100000.0

    # Проверка второй категории
    assert categories[1].name == "Телевизоры"
    assert len(categories[1].products) == 1

    # Проверка глобальных счетчиков (2 категории, 2 + 1 = 3 товара)
    assert Category.category_count == 2
    assert Category.product_count == 3


def test_load_data_from_json_empty_products(tmp_path):
    """Проверка граничного случая: категория без товаров."""
    json_data = [
        {
            "name": "Пустая категория",
            "description": "Здесь пока ничего нет",
            "products": [],
        }
    ]
    file_path = tmp_path / "empty.json"
    file_path.write_text(json.dumps(json_data), encoding="utf-8")

    categories = load_data_from_json(str(file_path))

    assert len(categories) == 1
    assert len(categories[0].products) == 0
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_load_data_from_json_file_not_found():
    """
    Тест на случай, если файл не существует.
    Покрывает блок except FileNotFoundError (если он есть в коде).
    """
    # Если ваш код возвращает пустой список при ошибке
    categories = load_data_from_json("non_existent_file.json")
    assert categories == []

    # ИЛИ, если ваш код выбрасывает исключение, проверьте это:
    # with pytest.raises(FileNotFoundError):
    #     load_data_from_json("non_existent_file.json")


def test_load_data_from_json_invalid_json(tmp_path):
    """
    Тест на случай некорректного JSON.
    Покрывает блок except json.JSONDecodeError (если он есть в коде).
    """
    file_path = tmp_path / "invalid.json"
    file_path.write_text("this is not a valid json", encoding="utf-8")

    # Если ваш код возвращает пустой список при ошибке парсинга
    categories = load_data_from_json(str(file_path))
    assert categories == []


def test_load_data_from_json_empty_categories_list(tmp_path):
    """
    Тест на случай, когда в JSON пустой массив категорий.
    Покрывает строки внутри цикла for category_data in data:,
    если цикл не выполняется ни разу.
    """
    file_path = tmp_path / "empty_categories.json"
    file_path.write_text("[]", encoding="utf-8")

    categories = load_data_from_json(str(file_path))
    assert categories == []
    assert Category.category_count == 0
    assert Category.product_count == 0


def test_load_data_from_json_missing_products_key(tmp_path):
    """
    Тест на случай, когда у категории нет ключа "products".
    Покрывает ветку else или .get("products", []) в коде.
    """
    json_data = [
        {
            "name": "Категория без товаров",
            "description": "Описание",
            # Ключ "products" отсутствует
        }
    ]
    file_path = tmp_path / "missing_key.json"
    file_path.write_text(json.dumps(json_data), encoding="utf-8")

    categories = load_data_from_json(str(file_path))
    assert len(categories) == 1
    assert categories[0].name == "Категория без товаров"
    assert categories[0].products == []


def test_product_str_or_repr():
    """
    Покрывает метод __repr__ класса Product.
    """
    product = Product("Test Product", "Description", 100.0, 5)
    repr(product)


def test_category_str_or_repr():
    """
    Покрывает метод __repr__ класса Category.
    """
    product = Product("P", "D", 10.0, 1)
    category = Category("Test Category", "Description", [product])
    repr(category)
