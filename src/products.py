class Product:
    """Класс, представляющий товар."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity


    @classmethod
    def new_product(cls, product_data: dict) -> "Product":
        """
        Создаёт и возвращает объект Product на основе словаря с параметрами.
        Ожидается словарь вида:
        {"name": ..., "price": ..., "description": ..., "quantity": ...}
        """
        return cls(
            name=product_data["name"],
            price=product_data["price"],
            description=product_data["description"],
            quantity=product_data["quantity"],
        )


    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price


    def __repr__(self):
        return (
            f"Product("
            f"name={self.name!r}, "
            f"description={self.description!r}, "
            f"__price={self.__price}, "
            f"quantity={self.quantity})"
        )
