
from map_objects.tile import Tile


class GameMap:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.tiles: list[list[Tile]] = self.initialize_tiles()

    def is_blocked(self, x: int , y: int) -> bool:
        return self.tiles[x][y].blocked
        
    def initialize_tiles(self) -> list[list[Tile]]:
        tiles: list[list[Tile]] = [[Tile(False) for y in range(self.height)] for x in range(self.width)]

        tiles[30][22].blocked = True
        tiles[30][22].block_sight = True
        tiles[31][22].blocked = True
        tiles[31][22].block_sight = True
        tiles[32][22].blocked = True
        tiles[32][22].block_sight = True

        return tiles
