class Product:
    """Класс, представляющий товар."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return (f"Product({self.name}, {self.description},"
                f"{self.price}, {self.quantity},)"
                )
