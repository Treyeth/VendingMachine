from .item import Item
import warnings

class Inventory:
    def __init__(self):
        self._item_inventory = []

    def __repr__(self):
        return('Inventory()')

    # def __str__(self):
    #     return("Papuci")

    @property
    def item_inventory(self):
        return self._item_inventory

    def add_new_product(self, name: str, price: float, quantity: int):
        for item in self._item_inventory:
            item_name = item.name
            if name == item_name:
                warnings.warn('Item already exists in the list.')
                return
        new_item = Item(name, price, quantity)
        self._item_inventory.append(new_item)

    def delete_product_by_name(self, name: str) -> None:
        """

        Args:
            name:

        Returns:

        """
        for index, item in enumerate(self._item_inventory):
            if item.name == name:
                del self._item_inventory[index]
                print(f'{item.name} successfully deleted.')
                return
        warnings.warn(f'{name} has not been found in the inventory.')

    def has_item(self, name: str) -> bool:
        for item in self._item_inventory:
            if item.name == name:
                return True
        return False

    def return_item_by_name(self, name: str) -> [Item, warnings.warn]:
        for item in self._item_inventory:
            if item.name == name:
                return item
        warnings.warn('Product not found')

    def modify_item_quantity(self, name: str, quantity: int) -> None:
        for index, item in enumerate(self._item_inventory):
            if item.name == name:
                print(f"{item.name} has {item.quantity} at the moment")
                item.quantity += quantity
                if item.quantity < 0:
                    self.delete_product_by_name(name)
                else:
                    print(f"{item.name} has {item.quantity} now.")
                return
        warnings.warn(f'{name} has not been found in the items.')

