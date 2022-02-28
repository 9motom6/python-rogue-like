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

    def chebyshev_distance(self, target):
        dx = target.x - self.x
        dy = target.y - self.y

        return max(abs(dx), abs(dy))
