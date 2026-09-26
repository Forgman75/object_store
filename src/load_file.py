import json
import logging
from src.categories import Category
from src.products import Product


def load_data_from_json(
    file_path: str = "data/products.json",
) -> list[Category]:
    """
    Читает данные из JSON файла и создает объекты классов Category и Product.

    :param file_path: Путь к файлу JSON
    :return: Список объектов Category
    """
    categories = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error(f"Файл {file_path} не найден.")
        return []
    except json.JSONDecodeError as e:
        logging.error(
            f"Ошибка: Некорректный формат JSON в файле {file_path}: {e}"
        )
        return []
    except Exception as e:
        logging.error(f"Произошла неожиданная ошибка: {e}")
        return []

    for category_data in data:
        # Создаем объекты Product для текущей категории
        products_list = []
        for product_data in category_data.get("products", []):
            product = Product(
                name=product_data["name"],
                description=product_data["description"],
                price=float(product_data["price"]),
                quantity=int(product_data["quantity"]),
            )
            products_list.append(product)

            # Создаем объект Category, передавая ему список объектов Product
            # Это автоматически увеличит Category.category_count и
            #  Category.product_count
        category = Category(
            name=category_data["name"],
            description=category_data["description"],
            products=products_list,
        )
        categories.append(category)

    return categories
