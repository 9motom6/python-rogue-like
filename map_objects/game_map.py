from typing import TYPE_CHECKING, Iterable, Optional, Tuple
import numpy
from tcod import Console
from map_objects.coords import Coords

import map_objects.tile_types as tile_types


    
class GameMap:
    def __init__(self, engine, width: int, height: int, entities = ()):
        self.engine = engine
        self.width: int = width
        self.height: int = height
        self.entities = set(entities)
        self.tiles = self.initialize_tiles(width, height)

        self.visible = numpy.full((width, height), fill_value=False, order="F")  # Tiles the player can currently see
        self.explored = numpy.full((width, height), fill_value=False, order="F")  # Tiles the player has seen before

    def is_in_bounds(self, coords: Coords) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= coords.x < self.width and 0 <= coords.y < self.height

    def render(self, console: Console) -> None:
        """  
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        console.tiles_rgb[0:self.width, 0:self.height] = numpy.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )

        for entity in self.entities:
            # Only print entities that are in the FOV
            if self.visible[entity.location.x, entity.location.y]:
                console.print(x=entity.location.x, y=entity.location.y, string=entity.char, fg=entity.color)
        
    def initialize_tiles(self, width: int, height: int):
        return numpy.full((width, height), fill_value=tile_types.wall, order="F")

    def set_tiles_rect(self, rectangle: Tuple[slice, slice], tile_type):
        self.tiles[rectangle] = tile_type

    def get_blocking_entity_at_location(self, location: Coords):
        for entity in self.entities:
            if (entity.blocks_movement and entity.location == location):
                return entity

        return None

