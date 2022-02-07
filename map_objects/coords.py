from typing import Tuple


class Coords:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    

    @classmethod
    def from_tuple(cls, coords: Tuple[int, int]) -> None:
        return cls(x = coords[0], y = coords[1])
