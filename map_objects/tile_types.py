from typing import Tuple
import numpy

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = numpy.dtype(
    [
        ("ch", numpy.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = numpy.dtype(
    [
        ("walkable", numpy.bool),  # True if this tile can be walked over.
        ("transparent", numpy.bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when the tile is in FOV.
    ]
)


# SHROUD represents unexplored, unseen tiles
SHROUD = numpy.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> numpy.ndarray:
    """Helper function for defining individual tile types """
    return numpy.array((walkable, transparent, dark, light), dtype=tile_dt)


floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (130, 110, 50)),
)