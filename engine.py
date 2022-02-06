import tcod
from actions import EscapeAction, FullscreenAction, MovementAction

from input_handlers import EventHandler
from entity import Entity
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all

FONT_FILE = "arial10x10.png"

def main() -> bool:
    screen_width = 80
    screen_height = 50
    map_width: int = 80
    map_height: int = 45

    tileset = tcod.tileset.load_tilesheet(
        FONT_FILE, 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    colors: dict[str, tcod.Color] = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150)
    }
    
    event_handler = EventHandler()

    player: Entity = Entity(int(screen_width / 2), int(screen_height / 2), '@', tcod.white)
    npc: Entity = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', tcod.yellow)

    entities: list[Entity] = [npc, player]

    game_map: GameMap = GameMap(map_width, map_height)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Roguelike",
        vsync=True,
    ) as context:
        root_console: tcod.Console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            render_all(root_console, entities, game_map, screen_width, screen_height, colors)
            
            context.present(root_console)
            
            root_console.clear()

            for event in tcod.event.wait():
                action = event_handler.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, MovementAction):
                    if not game_map.is_blocked(player.x + action.dx, player.y + action.dy):
                        player.move(dx = action.dx, dy = action.dy)

                elif isinstance(action, FullscreenAction):
                    toggle_fullscreen(context)

                elif isinstance(action, EscapeAction):
                    raise SystemExit()

def toggle_fullscreen(context: tcod.context.Context) -> None:
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

if __name__ == "__main__":
    main()
