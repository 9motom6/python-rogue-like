from typing import Tuple
import math

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

    def distance(self, other):
        """
        Return the distance between the current entity and the given (x, y) coordinate.
        """
        return math.sqrt((other.x - self.x) ** 2 + (self.y - self.y) ** 2)