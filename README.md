# Object Store - Система управления товарами и категориями

Простая система для управления товарами и категориями с возможностью загрузки данных из JSON файлов.

## Описание

Проект реализует две основные сущности:
- **Product** - товар с характеристиками (название, описание, цена, количество)
- **Category** - категория товаров, содержащая список объектов Product

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
print(len(category1.products))     # 3

# Проверка, что в списке хранятся объекты Product
print(type(category1.products[0])) # <class 'src.products.Product'>
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
