import copy
from typing import Optional, Tuple, Type, TypeVar
from components.ai import BaseAI
from components.fighter import Fighter

from map_objects.coords import Coords
from map_objects.game_map import GameMap
from map_objects.render_order import RenderOrder

T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    parent: GameMap

    def __init__(
        self,
        parent: Optional[GameMap] = None,
        location: Coords = Coords(0, 0),
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
    ):
        self.location = location
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent
            parent.entities.add(self)

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    def spawn(self: T, gamemap: GameMap, spawn_location: Coords) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.location = spawn_location
        clone.parent = gamemap
        gamemap.entities.add(clone)

        return clone

    def move(self, dx: int, dy: int) -> None:
        self.location.x += dx
        self.location.y += dy

    def place(self, location: Coords,  gamemap: Optional[GameMap] = None) -> None:
        """Place this entity at a new location.  Handles moving across GameMaps."""
        self.location = location

        if gamemap:
            if hasattr(self, "parent"):  # Possibly uninitialized.
                if self.parent is self.gamemap:
                    self.gamemap.entities.remove(self)
            self.parent = gamemap
            gamemap.entities.add(self)


class Actor(Entity):
    def __init__(self,
                 *,
                 location: Coords = Coords(0, 0),
                 char: str = "?",
                 color: Tuple[int, int, int] = (255, 255, 255),
                 name: str = "<Unnamed>",
                 ai_cls: Type[BaseAI],
                 fighter: Fighter):
        super().__init__(
            location=location,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,)

        self.ai: Optional[BaseAI] = ai_cls(self)

        self.fighter = fighter
        self.fighter.parent = self

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)
