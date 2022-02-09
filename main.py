import copy

import tcod

from engine import Engine
from input_handlers import EventHandler
from map_objects import entity_factories
from map_objects.entity import Entity
from map_objects.game_map import GameMap
from map_objects.procedual_generator import generate_dungeon

FONT_FILE = "arial10x10.png"

def main() -> bool:
    screen_width = 80
    screen_height = 50
    
    map_width: int = 80
    map_height: int = 45
    
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room=2

    tileset = tcod.tileset.load_tilesheet(
        FONT_FILE, 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    
    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_map =  generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        engine=engine,
    )

    engine.update_fov()

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Roguelike",
        vsync=True,
    ) as context:
        root_console: tcod.Console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)
            
            engine.event_handler.handle_events()

if __name__ == "__main__":
    main()
