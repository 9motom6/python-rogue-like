from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from entity import Entity
from input_handlers import EventHandler
from map_objects.game_map import GameMap


class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, player: Entity, game_map: GameMap):
        self.entities = entities
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map

    def handle_events(self, events: Iterable[Any], context) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
            action.perform(self, self.player, context)

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            console.print(entity.location.x, entity.location.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()

