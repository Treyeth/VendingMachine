class Item:
    def __init__(self, name: str, price: float, quantity: int = 0):
        self._name = name
        self._price = price
        self._quantity = quantity

    def __repr__(self):
        return "Item()"

    def __str__(self):
        return f"Item name: {self._name} \n" \
               f"Item price: {self._price}\n" \
               f"Item quantity: {self._quantity}"

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, new_price: float):
        self._price = new_price

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, new_quantity: int):
        self._quantity = new_quantity
