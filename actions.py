import tcod
from entity import Entity

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


class MovementAction(Action):
    def __init__(self, dx: int, dy: int): 
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine, entity: Entity, context) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.is_in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.

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