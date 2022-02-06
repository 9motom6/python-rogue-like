import numpy
from tcod import Console

import map_objects.tile_types as tile_types

class GameMap:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.tiles = self.initialize_tiles(width, height)


    def is_in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
        
    def initialize_tiles(self, width: int, height: int):
        tiles = numpy.full((width, height), fill_value=tile_types.floor, order="F")

        tiles[30:33, 22] = tile_types.wall

        return tiles
