from items import Item, ItemPatch
from pydantic import BaseModel

import random

items = { 1: Item( id=1, name="Banana", price=12.3, is_offer=False ) }

class ItemService(BaseModel):


    def query_items(name: str = None, lower_price: float = None, max_price: float = None):
        itemlist = list(items.values())
        filteredlist = filter(lambda x:
                    (name is None or x.name.lower() == name.lower()) and
                    (lower_price is None or x.price >= lower_price) and
                    (max_price is None or x.price <= max_price),
                 itemlist)
        return filteredlist

    def read_item(item_id: int):
        item = items.get(item_id)
        if item is not None:
            item.id = item_id;
        return item

    def add_item(item: Item) -> Item:
        item_id = random.randint(2,99999)
        item.id = item_id
        items[item_id] = item
        return item

    def update_item(item: Item) -> Item:
        # Ideally would lock a mutex or start a transaction to guarantee no concurrent operations
        items[item.id] = item
        return item
    
    def patch_item(item_id: int, itempatch: ItemPatch) -> Item:
        # Ideally would lock a mutex or start a transaction to guarantee no concurrent operations
        item = items[item_id]
        if itempatch.price is not None:
            item.price = itempatch.price
        if itempatch.is_available is not None: 
            item.is_available = itempatch.is_available
        if itempatch.is_offer is not None:
            item.is_offer = itempatch.is_offer
        return item
    
    def delete_item(item_id: int) -> bool:
        exists = items.pop(item_id, None)
        return exists != None