import pytest
from src.base_product import BaseProduct
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
    product = ConcreteProduct("Test", "Desc", 100.0, 1, extra_arg="value", another=42)
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


