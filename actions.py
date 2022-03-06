
from typing import Optional, Tuple
from map_objects.coords import Coords
import color
import exceptions

class Action: 

    def __init__(self, entity) -> None:
        # super().__init__()
        self.entity = entity

    @property
    def engine(self):
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.        
        `self.engine` is the scope this action is being performed in.
        `self.entity` is the object performing the action.
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

class ActionWithDirection(Action):
    def __init__(self, entity, dx: int, dy: int):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Coords:
        """Returns this actions destination."""
        return Coords(self.entity.location.x + self.dx, self.entity.location.y + self.dy)

    @property
    def blocking_entity(self):
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(self.dest_xy)

    @property
    def target_actor(self):
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(self.dest_xy)

    def perform(self) -> None:
        return super().perform()

class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"

        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} for {damage} hit points.", attack_color
            )
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(
                f"{attack_desc} but does no damage.", attack_color
            )

class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor is not None and self.target_actor.blocks_movement:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()

class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        if not self.engine.game_map.is_in_bounds(self.dest_xy):            
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.game_map.tiles["walkable"][self.dest_xy.x, self.dest_xy.y]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at_location(self.dest_xy):
            # Destination is blocked by an entity.
            raise exceptions.Impossible("That way is blocked.")
            
        self.entity.move(self.dx, self.dy)

class ItemAction(Action):
    def __init__(
        self, entity, item, target_xy: Optional[Tuple[int, int]] = None
    ):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.location.x, entity.location.y
        self.target_xy = target_xy

    @property
    def target_actor(self):
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(Coords(*self.target_xy))

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        self.item.consumable.activate(self)
        
class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity):
        super().__init__(entity)

    def perform(self) -> None:
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if self.entity.location == item.location:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")

                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"You picked up the {item.name}!")
                return

        raise exceptions.Impossible("There is nothing here to pick up.")

class DropItem(ItemAction):
    def perform(self) -> None:
        self.entity.inventory.drop(self.item)

class WaitAction(Action):
    def perform(self) -> None:
        pass

# class FullscreenAction(Action):
#     def perform(self) -> None:      
#         """Toggle a context window between fullscreen and windowed modes."""
#         if not context.sdl_window_p:
#             return
#         fullscreen = tcod.lib.SDL_GetWindowFlags(context.sdl_window_p) & (
#             tcod.lib.SDL_WINDOW_FULLSCREEN | tcod.lib.SDL_WINDOW_FULLSCREEN_DESKTOP
#         )
#         tcod.lib.SDL_SetWindowFullscreen(
#             context.sdl_window_p,
#             0 if fullscreen else tcod.lib.SDL_WINDOW_FULLSCREEN_DESKTOP,
#         )