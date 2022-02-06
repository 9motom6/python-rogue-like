import tcod
from engine import Engine

from entity import Entity
from input_handlers import EventHandler
from map_objects import coords
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

    tileset = tcod.tileset.load_tilesheet(
        FONT_FILE, 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    
    event_handler = EventHandler()

    player: Entity = Entity(coords.Coords(int(screen_width / 2), int(screen_height / 2)), '@', (255, 255, 255))
    npc: Entity = Entity(coords.Coords(int(screen_width / 2) + 5, int(screen_height / 2)), '@', (255, 255, 0))

    entities: list[Entity] = [npc, player]
    game_map: GameMap =  generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player
    )

    engine = Engine(entities=entities, event_handler=event_handler, player=player, game_map=game_map)

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
            
            events = tcod.event.wait()
            
            engine.handle_events(events, context=context)

if __name__ == "__main__":
    main()
