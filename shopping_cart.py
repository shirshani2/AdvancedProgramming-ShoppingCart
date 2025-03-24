import item
from errors import ItemAlreadyExistsError, ItemNotExistError
from item import Item


class ShoppingCart:
    def __init__(self):
        self.items = []
    def add_item(self, item: Item):

        if any(i.name == item.name for i in self.items) :
            raise ItemAlreadyExistsError()
        else:
            self.items.append(item)



    def remove_item(self, item_name: str):

        if not any(item.name == item_name for item in self.items):
            raise ItemNotExistError()
        else:
            self.items.remove(next(item for item in self.items if item.name == item_name))


    def get_subtotal(self) -> int:
        return sum(item.price for item in self.items)
