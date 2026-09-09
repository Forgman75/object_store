# Object Store - Система управления товарами и категориями

Простая система для управления товарами и категориями с возможностью загрузки данных из JSON файлов.

## Описание

Проект реализует систему управления товарами с использованием принципов ООП:
- **`Product`** - товар с характеристиками (название, описание, цена, количество)
- **`Smartphone`** — специализированный класс для смартфонов с дополнительными атрибутами
- **`LawnGrass`** — специализированный класс для газонной травы
- **`Category`** - класс для группировки товаров с защитой от добавления некорректных объектов

Система автоматически подсчитывает общее количество категорий и товаров через атрибуты класса.

## Быстрый старт

### Установка зависимостей

```bash
# Если используете Poetry
poetry install
```
## Примеры использования

### Создание объектов Product

```
# Создание товара
product1 = Product(
    name="Samsung Galaxy S23 Ultra",
    description="256GB, Серый цвет, 200MP камера",
    price=180000.0,
    quantity=5
)

# Доступ к атрибутам товара
print(product1.name)         # Samsung Galaxy S23 Ultra
print(product1.description)  # 256GB, Серый цвет, 200MP камера
print(product1.price)        # 180000.0
print(product1.quantity)     # 5
```

### Создание объектов Smartphone и LawnGrass

```
# Создаём смартфон
iphone = Smartphone(
    name="iPhone 14 Pro",
    description="Флагманский смартфон Apple",
    price=99990.0,
    quantity=10,
    efficiency=97.5,       # эффективность (баллы)
    model="Pro",           # модель
    memory=256,            # объём встроенной памяти (ГБ)
    color="Deep Purple"    # цвет корпуса
)

# Создаём газонную траву
grass = LawnGrass(
    name="Трава газонная Премиум",
    description="Смесь для спортивного газона",
    price=750.0,
    quantity=50,
    country="Россия",      # страна-производитель
    germination_period="7 дней",  # срок прорастания
    color="Зелёный"        # цвет травы
)

print(iphone.name, iphone.model, iphone.memory)   # iPhone 14 Pro Pro 256
print(grass.name, grass.country)                  # Трава газонная Премиум Россия
```


### Создание объектов Category

```
# Сначала создаем товары
product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

# Создаем категорию со списком товаров
category1 = Category(
    name="Смартфоны",
    description="Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
    products=[product1, product2, product3]
)

# Доступ к атрибутам категории
print(category1.name)              # Смартфоны
print(category1.description)       # Смартфоны, как средство не только коммуникации...
print(len(category1.product_list))     # 3

# Проверка, что в списке хранятся объекты Product
print(type(category1.product_list[0])) # <class 'src.products.Product'>
```

### Добавление товаров в категорию через add_product

Метод add_product класса Category принимает только объекты класса Product или его наследников. При попытке добавить что-то другое будет выброшено исключение TypeError.

```
# Создаём категорию (передаём пустой список товаров)
electronics = Category("Электроника", "Техника для дома", [])

# Корректное добавление объектов
electronics.add_product(iphone)
electronics.add_product(Smartphone(
    "Samsung Galaxy S23", "Флагман Samsung", 89990.0, 5,
    95.0, "S23", 128, "White"
))

print(len(electronics.product_list))  # 2

# Попытка добавить недопустимый объект
electronics.add_product("Просто строка")
# TypeError: Можно добавлять только объекты классов Product или его наследников

electronics.add_product(1000)
# TypeError: Можно добавлять только объекты классов Product или его наследников
```
### Сложение товаров через метод __add__ класса Product

Магический метод __add__ позволяет складывать два товара одного типа и получать общую сумму их стоимости на складе (price * quantity).

```
# Создаём два смартфона одной модели
iphone_128 = Smartphone(
    "iPhone 14", "Описание", 79990.0, 5,
    95.0, "Base", 128, "Black"
)

iphone_256 = Smartphone(
    "iPhone 14", "Описание", 89990.0, 3,
    95.0, "Base", 256, "Black"
)

# Складываем товары — получаем общую стоимость на складе
total_value = iphone_128 + iphone_256
print(total_value)
# (79990 * 5) + (89990 * 3) = 399950 + 269970 = 669920.0

# То же самое для газонной травы
grass_1 = LawnGrass("Трава А", "Описание", 500.0, 20, "Россия", "7 дней", "Зелёный")
grass_2 = LawnGrass("Трава Б", "Описание", 800.0, 10, "Германия", "10 дней", "Светло-зелёный")

print(grass_1 + grass_2)
# (500 * 20) + (800 * 10) = 10000 + 8000 = 18000.0

# Нельзя сложить смартфон и траву
try:
    result = iphone + grass
except TypeError as e:
    print(e)
    # Ошибка: нельзя складывать товары разных типов

```

### Автоматический подсчет категорий и товаров

```
# Создаем первую категорию с 3 товарами
p1 = Product("Товар 1", "Описание", 100.0, 5)
p2 = Product("Товар 2", "Описание", 200.0, 10)
p3 = Product("Товар 3", "Описание", 300.0, 15)
cat1 = Category("Электроника", "Описание категории", [p1, p2, p3])

print(Category.category_count)  # 1
print(Category.product_count)   # 3

# Создаем вторую категорию с 2 товарами
p4 = Product("Товар 4", "Описание", 400.0, 20)
p5 = Product("Товар 5", "Описание", 500.0, 25)
cat2 = Category("Бытовая техника", "Описание категории", [p4, p5])

# Счетчики обновляются автоматически
print(Category.category_count)  # 2
print(Category.product_count)   # 5 (3 + 2)
```

### Загрузка данных из JSON файла

```
# Загружаем данные из JSON файла
categories = load_data_from_json("products.json")

# Проверяем результат
print(f"Загружено категорий: {len(categories)}")  # Загружено категорий: 2

# Перебираем все категории
for category in categories:
    print(f"\nКатегория: {category.name}")
    print(f"Описание: {category.description}")
    print(f"Количество товаров: {len(category.products)}")
    
    # Перебираем товары в категории
    for product in category.products:
        print(f"  - {product.name}: {product.price} руб. (остаток: {product.quantity})")

# Проверяем глобальные счетчики
print(f"\nВсего категорий: {Category.category_count}")  # Всего категорий: 2
print(f"Всего товаров: {Category.product_count}")      # Всего товаров: 4
```

## Запуск тестов

### Запуск всех тестов

```
poetry run pytest
```

### Запуск конкретного теста

```
pytest tests/test_store.py::test_product_initialization -v
```

### Запуск с отчетом о покрытии

```
# Терминальный отчет
pytest --cov=src --cov-report=term-missing

# HTML отчет (откроется в браузере)
pytest --cov=src --cov-report=html
# Затем откройте файл htmlcov/index.html
```


## Требования

* Python 3.12+
* pytest (для тестирования)
* pytest-cov (для отчетов о покрытии)
