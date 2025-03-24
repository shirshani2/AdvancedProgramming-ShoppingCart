from itertools import count

import yaml

from errors import ItemAlreadyExistsError, ItemNotExistError, TooManyMatchesError
from item import Item
from shopping_cart import ShoppingCart

class Store:
    def __init__(self, path):
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart()

    @staticmethod
    def _convert_to_item_objects(items_raw):
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        return self._items

    def search_by_name(self, item_name: str) -> list:
        Tags = [tag for item in self._shopping_cart.items for tag in item.hashtags]
        answer = [item for item in self._items if item_name in item.name and item not in self._shopping_cart.items]
        answer.sort(key=lambda item: (-sum(Tags.count(tag) for tag in item.hashtags), item.name))


        return answer

    def search_by_hashtag(self, hashtag: str) -> list:
        Tags = [tag for item in self._shopping_cart.items for tag in item.hashtags]
        answer = [item for item in self._items if hashtag in item.hashtags and item not in self._shopping_cart.items]
        answer.sort(key=lambda item: (-sum(Tags.count(tag) for tag in item.hashtags), item.name))
        return answer

    def add_item(self, item_name: str):
        items = [item for item in self._items if item_name.lower() in item.name.lower()]
        if not items:
            raise ItemNotExistError()
        if len(items) > 1:
            raise TooManyMatchesError()
        the_item = items[0]
        exist = [item for item in self._shopping_cart.items if item_name in item.name]
        if exist:
            raise ItemAlreadyExistsError()
        else:
            self._shopping_cart.add_item(the_item)


    def remove_item(self, item_name: str):
        items = [item for item in self._items if item_name.lower() in item.name.lower()]
        if not items:
            raise ItemNotExistError()
        if len(items) > 1:
            raise TooManyMatchesError()
        else:
            the_item = items[0]
            self._shopping_cart.remove_item(the_item.name)

    def checkout(self) -> int:
        return sum(item.price for item in self._shopping_cart.items)





