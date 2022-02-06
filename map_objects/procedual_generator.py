import random
from typing import Iterator, List, Tuple
from typing_extensions import Self

import tcod
from entity import Entity
from map_objects.coords import Coords

from map_objects.game_map import GameMap
import map_objects.tile_types as tile_types

class RectangularRoom:
    def __init__(self, top_left: Coords, width: int, height: int) -> None:
        self.top_left = top_left
        self.bottom_right = Coords(top_left.x + width, top_left.y + height)

    @property
    def center(self) -> Coords:
        center_x = int((self.top_left.x + self.bottom_right.x) / 2)
        center_y = int((self.top_left.y + self.bottom_right.y) / 2)

        return Coords(center_x, center_y)

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.top_left.x + 1, self.bottom_right.x), slice(self.top_left.y + 1, self.bottom_right.y)

    def intersects(self, other: Self) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.top_left.x <= other.bottom_right.x
            and self.bottom_right.x >= other.top_left.x
            and self.top_left.y <= other.bottom_right.y
            and self.bottom_right.y >= other.top_left.y
        )


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    player: Entity,
) -> GameMap:
    """Generate a new dungeon map."""
    dungeon = GameMap(map_width, map_height)

    rooms: List[RectangularRoom] = []

    for _ in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        room_coords = Coords(
            random.randint(0, dungeon.width - room_width - 1),
            random.randint(0, dungeon.height - room_height - 1))

        new_room = RectangularRoom(room_coords, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        dungeon.set_tiles_rect(new_room.inner, tile_types.floor)

        if len(rooms) == 0:
            # The first room, where the player starts.
            player.location = new_room.center
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        # Finally, append the new room to the list.
        rooms.append(new_room)

    return dungeon

    
def tunnel_between(start: Coords, end: Coords) -> Iterator[Coords]:
    """Return an L-shaped tunnel between these two points.""" 
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = end.x, start.y
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = start.x, end.y

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((start.x, start.y), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (end.x, end.y)).tolist():
        yield x, y
