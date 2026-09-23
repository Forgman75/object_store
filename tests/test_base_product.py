import pytest
from src.base_product import BaseProduct, ProductZeroQuantityError
from tests.conftest import ConcreteProduct, AnotherProduct


def test_cannot_instantiate_base_product_directly():
    """BaseProduct — абстрактный, создать его напрямую нельзя."""
    with pytest.raises(TypeError):
        BaseProduct("name", "description", 100.0, 5)


def test_concrete_product_initialization(concrete_product):
    """Конкретный наследник корректно инициализируется."""
    assert concrete_product.name == "Товар1"
    assert concrete_product.description == "Описание"
    assert concrete_product.price == 1000.0
    assert concrete_product.quantity == 5


def test_extra_args_kwargs_are_accepted():
    """BaseProduct принимает *args и **kwargs без ошибок."""
    product = ConcreteProduct(
        "Test", "Desc", 100.0, 1, extra_arg="value", another=42
    )
    assert product.name == "Test"
    assert product.price == 100.0


def test_concrete_product_is_subclass():
    """ConcreteProduct наследуется от BaseProduct."""
    assert issubclass(ConcreteProduct, BaseProduct)


def test_another_product_is_subclass():
    """AnotherProduct наследуется от BaseProduct."""
    assert issubclass(AnotherProduct, BaseProduct)


def test_base_product_is_abc():
    """BaseProduct является абстрактным классом."""
    from abc import ABC

    assert issubclass(BaseProduct, ABC)


def test_instance_check(concrete_product):
    """Экземпляр ConcreteProduct является экземпляром BaseProduct."""
    assert isinstance(concrete_product, BaseProduct)


def test_price_getter(concrete_product):
    """Геттер price возвращает корректное значение."""
    assert concrete_product.price == 1000.0


def test_price_setter_valid_value(concrete_product):
    """Сеттер принимает положительную цену."""
    concrete_product.price = 2000.0
    assert concrete_product.price == 2000.0


def test_price_setter_zero_value(concrete_product, capsys):
    """Сеттер отклоняет нулевую цену."""
    concrete_product.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert concrete_product.price == 1000.0  # Цена не изменилась


def test_price_setter_negative_value(concrete_product, capsys):
    """Сеттер отклоняет отрицательную цену."""
    concrete_product.price = -500.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert concrete_product.price == 1000.0  # Цена не изменилась


def test_price_is_private(concrete_product):
    """Цена хранится в приватном атрибуте __price."""
    # Проверяем, что прямой атрибут __price недоступен извне
    with pytest.raises(AttributeError):
        _ = concrete_product.__price


def test_add_same_type_products(concrete_product, another_product):
    """Сложение товаров одного типа возвращает сумму произведений цены
    на количество."""
    result = concrete_product + another_product
    expected = (1000.0 * 5) + (500.0 * 10)  # 5000 + 5000 = 10000
    assert result == expected


def test_add_different_type_products_raises_error(concrete_product):
    """Сложение товаров разных типов выбрасывает TypeError."""
    another = AnotherProduct("Other", "Desc", 200.0, 3)
    with pytest.raises(
        TypeError, match="Складывать можно только товары одного типа"
    ):
        _ = concrete_product + another


def test_add_with_non_product_raises_error(concrete_product):
    """Сложение с объектом не-Product выбрасывает TypeError."""
    with pytest.raises(TypeError):
        _ = concrete_product + "строка"

    with pytest.raises(TypeError):
        _ = concrete_product + 123


def test_add_commutative(concrete_product, another_product):
    """Сложение коммутативно: a + b == b + a."""
    result1 = concrete_product + another_product
    result2 = another_product + concrete_product
    assert result1 == result2


def test_str_method_implemented_in_concrete_class(concrete_product):
    """Конкретный класс реализует __str__."""
    result = str(concrete_product)
    assert "Товар1" in result
    assert "1000.0" in result
    assert "5" in result


def test_str_method_returns_string(concrete_product):
    """__str__ возвращает строку."""
    result = str(concrete_product)
    assert isinstance(result, str)


def test_is_exception_subclass():
    """Исключение наследуется от Exception."""
    assert issubclass(ProductZeroQuantityError, Exception)


def test_default_message():
    """Сообщение по умолчанию корректное."""
    error = ProductZeroQuantityError()
    assert str(error) == "Товар с нулевым количеством не может быть добавлен"


def test_custom_message():
    """Можно передать своё сообщение."""
    error = ProductZeroQuantityError("Моё сообщение")
    assert str(error) == "Моё сообщение"


def test_can_be_raised_and_caught():
    """Исключение можно выбросить и перехватить."""
    with pytest.raises(ProductZeroQuantityError) as exc_info:
        raise ProductZeroQuantityError()
    assert "нулевым количеством" in str(exc_info.value)
