import tcod as libtcod

from map_objects.entity import Entity
from map_objects.game_map import GameMap

def render_all(console: libtcod.Console, 
    entities: list[Entity], 
    game_map: GameMap,
    screen_width: int,
    screen_height: int,
    colors: dict[str, libtcod.Color]
) -> None:
# Draw all the tiles in the game map
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            if wall:
                libtcod.console_set_char_background(console, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(console, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    for entity in entities:
        draw_entity(console, entity)

    libtcod.console_blit(console, 0, 0, screen_width, screen_height, 0, 0, 0)

def clear_all(console: libtcod.Console, entities: list[Entity]):
    for entity in entities:
        clear_entity(console, entity)

def draw_entity(console: libtcod.Console, entity: Entity) -> None:
    libtcod.console_set_default_foreground(console, entity.color)
    console.print(entity.x, entity.y, entity.char, fg = entity.color)

def clear_entity(console: libtcod.Console, entity: Entity):
    console.print(entity.x, entity.y, ' ')
