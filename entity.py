from typing import Tuple

from map_objects.coords import Coords


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, location: Coords, char: str, color: Tuple[int, int, int]):
        self.location = location
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int) -> None:
        self.location.x += dx
        self.location.y += dy