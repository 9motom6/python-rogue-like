from typing import Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import EventHandler

from map_objects.entity import Entity
from map_objects.game_map import GameMap


class Engine:
    def __init__(self, event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map
        self.update_fov()

    def handle_events(self, events: Iterable[Any], context) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
            action.perform(self, self.player, context)

            self.handle_enemy_turns()
            
            self.update_fov()

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        context.present(console)

        console.clear()

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.location.x, self.player.location.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            print(f'The {entity.name} wonders when it will get to take a real turn.')