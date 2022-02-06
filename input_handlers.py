from typing import Optional
import tcod

from actions import Action, EscapeAction, FullscreenAction, MovementAction


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        key = event.sym
        mod = event.mod

        # Movement keys         
        if key == tcod.event.K_UP:
            return MovementAction(dx=0, dy=-1)
        if key == tcod.event.K_DOWN:
            return MovementAction(dx=0, dy=1)
        if key == tcod.event.K_LEFT:
            return MovementAction(dx=-1, dy=0)
        if key == tcod.event.K_RIGHT:
            return MovementAction(dx=1, dy=0)

        # Alt+Enter: toggle full screen
        if key == tcod.event.K_RETURN and mod.ALT:           
            return FullscreenAction()

        # Exit the game
        if key == tcod.event.K_ESCAPE:
           
            return EscapeAction()

        # No valid key was pressed
        return None

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()
