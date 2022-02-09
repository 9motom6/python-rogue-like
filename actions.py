from typing import Optional, Tuple, TYPE_CHECKING

import tcod
from map_objects.entity import Entity
from map_objects.coords import Coords


class Action: 

    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self):
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.        
        `self.engine` is the scope this action is being performed in.
        `self.entity` is the object performing the action.
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()

class ActionWithDirection(Action):
    def __init__(self, entity: Entity, dx: int, dy: int):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Coords:
        """Returns this actions destination."""
        return Coords(self.entity.location.x + self.dx, self.entity.location.y + self.dy)

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(self.dest_xy)

    def perform(self) -> None:
        return super().perform()

class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.blocking_entity
        if not target:
            return  # No entity to attack.

        print(f"You kick the {target.name}, much to its annoyance!")

class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.blocking_entity:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()

class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        if not self.engine.game_map.is_in_bounds(self.dest_xy):
            return  # Destination is out of bounds.
        if not self.engine.game_map.tiles["walkable"][self.dest_xy.x, self.dest_xy.y]:
            return  # Destination is blocked by a tile.
        if self.engine.game_map.get_blocking_entity_at_location(self.dest_xy):
            return  # Destination is blocked by an entity.

        self.entity.move(self.dx, self.dy)

# class FullscreenAction(Action):
#     def perform(self) -> None:      
#         """Toggle a context window between fullscreen and windowed modes."""
#         if not context.sdl_window_p:
#             return
#         fullscreen = tcod.lib.SDL_GetWindowFlags(context.sdl_window_p) & (
#             tcod.lib.SDL_WINDOW_FULLSCREEN | tcod.lib.SDL_WINDOW_FULLSCREEN_DESKTOP
#         )
#         tcod.lib.SDL_SetWindowFullscreen(
#             context.sdl_window_p,
#             0 if fullscreen else tcod.lib.SDL_WINDOW_FULLSCREEN_DESKTOP,
#         )