import tcod as libtcod

from input_handlers import handle_keys
from entity import Entity
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all

FONT_FILE = "arial10x10.png"

def main() -> bool:
    screen_width = 80
    screen_height = 50
    map_width: int = 80
    map_height: int = 45

    colors: dict[str, libtcod.Color] = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150)
    }

    player: Entity = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    npc: Entity = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)

    entities: list[Entity] = [npc, player]

    libtcod.console_set_custom_font(FONT_FILE, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, "Roguelike", False)

    console: libtcod.Console = libtcod.console.Console(screen_width, screen_height)
    
    game_map: GameMap = GameMap(map_width, map_height)
    
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        render_all(console, entities, game_map, screen_width, screen_height, colors)
        libtcod.console_flush()

        clear_all(console, entities)

        action = handle_keys(key)

        move_action = action.get("move")
        exit_action = action.get("exit")
        fullscreen = action.get("fullscreen")

        if move_action:
            dx, dy = move_action
            
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        if exit_action:
            return True

if __name__ == "__main__":
    main()
