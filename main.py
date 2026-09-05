from src.products import Product
from src.categories import Category, CategoryIterator
from src.load_file import load_data_from_json

if __name__ == "__main__":
    product1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
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
