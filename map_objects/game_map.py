from typing import Tuple
import numpy
from tcod import Console
from map_objects.coords import Coords

import map_objects.tile_types as tile_types

class GameMap:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.tiles = self.initialize_tiles(width, height)


    def is_in_bounds(self, coords: Coords) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= coords.x < self.width and 0 <= coords.y < self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
        
    def initialize_tiles(self, width: int, height: int):
        return numpy.full((width, height), fill_value=tile_types.wall, order="F")

    def set_tiles_rect(self, rectangle: Tuple[slice, slice], tile_type):
        self.tiles[rectangle] = tile_type
