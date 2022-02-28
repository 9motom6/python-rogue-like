import tcod

from actions import EscapeAction, BumpAction

class EventHandler(tcod.event.EventDispatch[any]):
    def __init__(self, engine):
        self.engine = engine

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()  # Update the FOV before the players next action.

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym
        mod = event.mod

        player = self.engine.player
        # Movement keys         
        if key == tcod.event.K_UP:
            return BumpAction(player, dx=0, dy=-1)
        if key == tcod.event.K_DOWN:
            return BumpAction(player, dx=0, dy=1)
        if key == tcod.event.K_LEFT:
            return BumpAction(player, dx=-1, dy=0)
        if key == tcod.event.K_RIGHT:
            return BumpAction(player, dx=1, dy=0)

        # Alt+Enter: toggle full screen
        if key == tcod.event.K_RETURN and mod.ALT:           
            pass
            # return FullscreenAction()

        # Exit the game
        if key == tcod.event.K_ESCAPE:           
            return EscapeAction(player)

        # No valid key was pressed 
        return None

    def ev_quit(self, event: tcod.event.Quit):
        raise SystemExit()
