from typing import Tuple


class Coords:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    @classmethod
    def from_tuple(cls, coords: Tuple[int, int]) -> None:
        return cls(x = coords[0], y = coords[1])