import copy
from typing import Optional, Tuple, TypeVar

from map_objects.coords import Coords
from map_objects.game_map import GameMap

T = TypeVar("T", bound="Entity")

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    
    gamemap: GameMap

    def __init__(
        self, 
        gamemap: Optional[GameMap] = None,
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
        if gamemap:
            # If gamemap isn't provided now then it will be set later.
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def spawn(self: T, gamemap: GameMap, spawn_location: Coords) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.location = spawn_location
        clone.gamemap = gamemap
        gamemap.entities.add(clone)

        return clone   
        
    def move(self, dx: int, dy: int) -> None:
        self.location.x += dx
        self.location.y += dy

    def place(self, location: Coords,  gamemap: Optional[GameMap] = None) -> None:
        """Place this entity at a new location.  Handles moving across GameMaps."""
        self.location = location
        
        if gamemap:
            if hasattr(self, "gamemap"):  # Possibly uninitialized.
                self.gamemap.entities.remove(self)
            self.gamemap = gamemap
            gamemap.entities.add(self)