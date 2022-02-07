import copy
from typing import Tuple, TypeVar

from map_objects.coords import Coords
from map_objects.game_map import GameMap

T = TypeVar("T", bound="Entity")

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(
        self, 
        location: Coords = Coords(0, 0), 
        char: str = "?", 
        color: Tuple[int, int, int] = (255, 255, 255),    
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
    ):
        self.location = location
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement

    def spawn(self: T, gamemap: GameMap, spawn_location: Coords) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.location = spawn_location
        gamemap.entities.add(clone)

        return clone   
        
    def move(self, dx: int, dy: int) -> None:
        self.location.x += dx
        self.location.y += dy