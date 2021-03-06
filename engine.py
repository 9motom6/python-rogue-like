from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import EventHandler, MainGameEventHandler
from render_functions import render_bar, render_names_at_mouse_location
from message_log import MessageLog
import exceptions

class Engine:

    game_map = None

    def __init__(self, player):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.player = player
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_names_at_mouse_location(console=console, x=21, y=44, engine=self)
        
    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible_array[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.location.x, self.player.location.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible_array

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI