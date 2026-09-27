from src.products import Product, Smartphone, LawnGrass
from src.categories import Category, CategoryIterator, Order
from src.base_info import BaseInfo
from src.base_product import ProductZeroQuantityError
from src.load_file import load_data_from_json


def safe_add_to_category(category: Category, product_class, **kwargs):
    """
    Безопасно добавляет товар в категорию.
    Обрабатывает ProductZeroQuantityError и выводит нужные сообщения.
    """
    try:
        product = product_class(**kwargs)
        category.add_product(product)
    except ProductZeroQuantityError as e:
        print(f"Ошибка: {e}")
    else:
        print("Товар добавлен")
    finally:
        print("Обработка добавления товара завершена\n")


def safe_add_to_order(
    product_class: Product, order_quantity: int, **kwargs
) -> Order | None:
    """
    Безопасно добавляет товар в заказ.
    """
    try:
        product = product_class(**kwargs)
        order = Order(product, order_quantity)
    except ProductZeroQuantityError as e:
        print(f"Ошибка: {e}")
        return None
    except ValueError as e:
        print(f"Ошибка при создании заказа: {e}")
        return None
    else:
        print("Товар добавлен")
        return order

    finally:
        print("Обработка добавления товара завершена\n")


if __name__ == "__main__":
    product1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # noqa: W504
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, "
        + "но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(category1.products)
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры", "Современные телевизоры с поддержкой 4K", []
    )

    category2.add_product(product4)
    print(category2.products)
    print(category2.product_count)

    new_product = Product.new_product(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5,
        }
    )
    print(new_product.name)
    print(new_product.description)
    print(new_product.price)
    print(new_product.quantity)

    new_product.price = 800
    print(new_product.price)

    new_product.price = -100
    print(new_product.price)
    new_product.price = 0
    print(new_product.price)

    # Загружаем данные из JSON файла
    loaded_categories = load_data_from_json()

    # Проверяем результат
    print(f"Загружено категорий: {len(loaded_categories)}")

    # Перебираем все категории
    for category in loaded_categories:
        print(f"\nКатегория: {category.name}")
        print(f"Описание: {category.description}")
        print(f"Количество товаров: {category.product_count_instance}")
        print(f"Товары: {category.products}")

    # Проверяем глобальные счетчики
    print(f"\nВсего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    print(str(product1))
    print(str(product2))
    print(str(product3))

    print(str(category1))

    print(category1.products)

    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)

    iterator = CategoryIterator(category1)

    for product in iterator:
        print(product)

    print("\n--- Ручной вызов next() ---")
    it = CategoryIterator(category1)
    print(next(it))
    print(next(it))
    print(next(it))

    smartphone1 = Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
        95.5,
        "S23 Ultra",
        256,
        "Серый",
    )
    smartphone2 = Smartphone(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8,
        98.2,
        "15",
        512,
        "Gray space",
    )
    smartphone3 = Smartphone(
        "Xiaomi Redmi Note 11",
        "1024GB, Синий",
        31000.0,
        14,
        90.3,
        "Note 11",
        1024,
        "Синий",
    )

    print(smartphone1.name)
    print(smartphone1.description)
    print(smartphone1.price)
    print(smartphone1.quantity)
    print(smartphone1.efficiency)
    print(smartphone1.model)
    print(smartphone1.memory)
    print(smartphone1.color)

    print(smartphone2.name)
    print(smartphone2.description)
    print(smartphone2.price)
    print(smartphone2.quantity)
    print(smartphone2.efficiency)
    print(smartphone2.model)
    print(smartphone2.memory)
    print(smartphone2.color)

    print(smartphone3.name)
    print(smartphone3.description)
    print(smartphone3.price)
    print(smartphone3.quantity)
    print(smartphone3.efficiency)
    print(smartphone3.model)
    print(smartphone3.memory)
    print(smartphone3.color)

    grass1 = LawnGrass(
        "Газонная трава",
        "Элитная трава для газона",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый",
    )
    grass2 = LawnGrass(
        "Газонная трава 2",
        "Выносливая трава",
        450.0,
        15,
        "США",
        "5 дней",
        "Темно-зеленый",
    )

    print(grass1.name)
    print(grass1.description)
    print(grass1.price)
    print(grass1.quantity)
    print(grass1.country)
    print(grass1.germination_period)
    print(grass1.color)

    print(grass2.name)
    print(grass2.description)
    print(grass2.price)
    print(grass2.quantity)
    print(grass2.country)
    print(grass2.germination_period)
    print(grass2.color)

    smartphone_sum = smartphone1 + smartphone2
    print(smartphone_sum)

    grass_sum = grass1 + grass2
    print(grass_sum)

    try:
        invalid_sum = smartphone1 + grass1
    except TypeError:
        print("Возникла ошибка TypeError при попытке сложения")
    else:
        print("Не возникла ошибка TypeError при попытке сложения")

    category_smartphones = Category(
        "Смартфоны",
        "Высокотехнологичные смартфоны",
        [smartphone1, smartphone2],
    )
    category_grass = Category(
        "Газонная трава", "Различные виды газонной травы", [grass1, grass2]
    )

    category_smartphones.add_product(smartphone3)

    print(category_smartphones.products)

    print(Category.product_count)

    try:
        category_smartphones.add_product("Not a product")
    except TypeError:
        print("Возникла ошибка TypeError при добавлении не продукта")
    else:
        print("Не возникла ошибка TypeError при добавлении не продукта")

    print("--- Создаем объекты ---")
    # Сработает миксин, выведет все параметры в стиле __repr__
    phone1 = Smartphone(
        "iPhone 15", "Черный", 100000.0, 5, "Высокая", "15 Pro", 256, "Черный"
    )
    grass1 = LawnGrass(
        "Газонная трава",
        "Зеленая",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Темно-зеленый",
    )

    print("\n--- Проверка функциональности ---")
    print(phone1)
    print(grass1)

    print("\n--- Создаём категорию ---")
    electronics = Category("Электроника", "Техника для дома")
    electronics.add_product(phone1)
    print(electronics)
    print(electronics.product_list)

    print("\n--- Создаём заказы ---")
    order1 = Order(phone1, 2)
    order2 = Order(grass1, 10, name="Заказ №1", description="Для дачи")

    print(order1)
    print(order2)

    print("\n--- Проверка общих свойств ---")
    print(
        f"Категория: name='{electronics.name}',"
        f" description='{electronics.description}'"
    )
    print(
        f"Заказ:     name='{order1.name}', description='{order1.description}'"
    )

    print("\n--- Проверка наследования от BaseInfo ---")
    print(f"Category наследует BaseInfo: {issubclass(Category, BaseInfo)}")
    print(f"Order наследует BaseInfo:    {issubclass(Order, BaseInfo)}")

    try:
        product_invalid = Product(
            "Бракованный товар", "Неверное количество", 1000.0, 0
        )
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы "
            "при попытке добавить продукт с нулевым количеством"
        )
    else:
        print(
            "Не возникла ошибка ValueError при попытке добавить продукт "
            "с нулевым количеством"
        )

    product1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны", "Категория смартфонов", [product1, product2, product3]
    )

    print(category1.middle_price())

    category_empty = Category(
        "Пустая категория", "Категория без продуктов", []
    )
    print(category_empty.middle_price())

    phones_category = Category("Смартфоны", "Мобильные устройства")
    # Создаём товар
    grass = LawnGrass(
        "Газонная трава", "Зелёная", 500.0, 20, "Россия", 7, "Тёмно-зелёный"
    )
    # Создаём заказ на этот товар
    my_order = Order(grass, quantity=3)

    print("Успешное добавление в Category")
    safe_add_to_category(
        phones_category,
        Smartphone,
        name="iPhone 15",
        description="Чёрный",
        price=100000.0,
        quantity=5,
        efficiency="Высокая",
        model="15 Pro",
        memory=256,
        color="Чёрный",
    )

    print("Товар с quantity=0 в Category")
    safe_add_to_category(
        phones_category,
        Smartphone,
        name="iPhone 15 Mini",
        description="Белый",
        price=50000.0,
        quantity=0,
        efficiency="Средняя",
        model="15 Mini",
        memory=128,
        color="Белый",
    )

    print("Успешное добавление в Order")
    order1 = safe_add_to_order(
        LawnGrass,
        order_quantity=3,
        name="Газонная трава",
        description="Зелёная",
        price=500.0,
        quantity=20,
        country="Россия",
        germination_period=7,
        color="Тёмно-зелёный",
    )

    print("Товар с quantity=0 в Order")
    order2 = safe_add_to_order(
        LawnGrass,
        order_quantity=3,
        name="Плохая трава",
        description="Описание",
        price=100.0,
        quantity=0,
        country="Россия",
        germination_period=5,
        color="Зелёный",
    )

    print("Заказ с order_quantity=0")
    order3 = safe_add_to_order(
        LawnGrass,
        order_quantity=0,
        name="Хорошая трава",
        description="Описание",
        price=100.0,
        quantity=10,
        country="Россия",
        germination_period=5,
        color="Зелёный",
    )

    print("Категория:")
    print(phones_category)
    print("\nЗаказ:")
    print(my_order, order1, order2, order3)
