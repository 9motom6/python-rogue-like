from typing import List

from components.base_component import BaseComponent



class Inventory(BaseComponent):
    parent: any

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[any] = []

    def drop(self, item) -> None:
        """
        Removes an item from the inventory and restores it to the game map, at the player's current location.
        """
        self.items.remove(item)
        item.place(self.parent.x, self.parent.y, self.gamemap)

        self.engine.message_log.add_message(f"You dropped the {item.name}.")