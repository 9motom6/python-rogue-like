import tcod as libtcod
from map_objects.coords import Coords

from map_objects.entity import Entity
from map_objects.game_map import GameMap
import color

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
                libtcod.console_set_char_background(
                    console, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(
                    console, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    for entity in entities:
        draw_entity(console, entity)

    libtcod.console_blit(console, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(console: libtcod.Console, entities: list[Entity]):
    for entity in entities:
        clear_entity(console, entity)


def draw_entity(console: libtcod.Console, entity: Entity) -> None:
    libtcod.console_set_default_foreground(console, entity.color)
    console.print(entity.x, entity.y, entity.char, fg=entity.color)


def clear_entity(console: libtcod.Console, entity: Entity):
    console.print(entity.x, entity.y, ' ')


def render_bar(console: libtcod.Console, current_value: int, maximum_value: int, total_width: int) -> None:
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=0, y=45, width=total_width,
                      height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(
        x=1, y=45, string=f"HP: {current_value}/{maximum_value}", fg=color.bar_text
    )

def get_names_at_location(x: int, y: int, game_map) -> str:
    if not game_map.is_in_bounds(Coords(x, y)) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.location.x == x and entity.location.y == y
    )

    return names.capitalize()
    
def render_names_at_mouse_location(
    console: libtcod.Console, x: int, y: int, engine
) -> None:
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )

    console.print(x=x, y=y, string=names_at_mouse_location)