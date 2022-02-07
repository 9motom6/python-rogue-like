import tcod
from map_objects.entity import Entity
from map_objects.coords import Coords

class Action: 
    def perform(self, engine, entity: Entity, context) -> None:
        """Perform this action with the objects needed to determine its scope.        
        `engine` is the scope this action is being performed in.
        `entity` is the object performing the action.
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self, engine, entity: Entity, context) -> None:
        raise SystemExit()

class ActionWithDirection(Action):
    def __init__(self, dx, dy) -> None:
        super().__init__()
        self.dx = dx
        self.dy = dy

    def perform(self, engine, entity: Entity, context) -> None:
        return super().perform(engine, entity, context)

class MeleeAction(ActionWithDirection):
    def perform(self, engine, entity: Entity, context) -> None:
        dest = Coords(entity.location.x + self.dx, entity.location.y + self.dy)
        target = engine.game_map.get_blocking_entity_at_location(dest)
        if not target:
            return  # No entity to attack.

        print(f"You kick the {target.name}, much to its annoyance!")

class BumpAction(ActionWithDirection):
    def perform(self, engine, entity: Entity, context) -> None:
        dest = Coords(entity.location.x + self.dx, entity.location.y + self.dy)

        if engine.game_map.get_blocking_entity_at_location(dest):
            return MeleeAction(self.dx, self.dy).perform(engine, entity, context)

        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity, context)

class MovementAction(ActionWithDirection):
    def perform(self, engine, entity: Entity, context) -> None:
        dest = Coords(x= entity.location.x + self.dx, y=entity.location.y + self.dy)
        if not engine.game_map.is_in_bounds(Coords(x= entity.location.x + self.dx, y=entity.location.y + self.dy)):
            return  # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest.x, dest.y]:
            return  # Destination is blocked by a tile.
        if engine.game_map.get_blocking_entity_at_location(dest):
            return  # Destination is blocked by an entity.

        entity.move(self.dx, self.dy)

class FullscreenAction(Action):
    def perform(self, engine, entity: Entity, context) -> None:        
        """Toggle a context window between fullscreen and windowed modes."""
        if not context.sdl_window_p:
            return
        fullscreen = tcod.lib.SDL_GetWindowFlags(context.sdl_window_p) & (
            tcod.lib.SDL_WINDOW_FULLSCREEN | tcod.lib.SDL_WINDOW_FULLSCREEN_DESKTOP
        )
        tcod.lib.SDL_SetWindowFullscreen(
            context.sdl_window_p,
            0 if fullscreen else tcod.lib.SDL_WINDOW_FULLSCREEN_DESKTOP,
        )