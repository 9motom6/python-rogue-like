from __future__ import annotations
import random

from typing import List, Optional, Tuple

import numpy as np  # type: ignore
import tcod
from actions import Action, BumpAction, MeleeAction, MovementAction, WaitAction

class BaseAI(Action):
    
    def perform(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest) -> List[Tuple[int, int]]:
        """Compute and return a path to the target position.

        If there is no valid path then returns an empty list.
        """
        # Copy the walkable array.
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            # Check that an enitiy blocks movement and the cost isn't zero (blocking.)
            if entity.blocks_movement and cost[entity.location.x, entity.location.y]:
                # Add to the cost of a blocked position.
                # A lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player.
                cost[entity.location.x, entity.location.y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.location.x, self.entity.location.y))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path: List[List[int]] = pathfinder.path_to((dest.x, dest.y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]

class HostileEnemy(BaseAI):
    def __init__(self, entity):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player

        dx = target.location.x - self.entity.location.x
        dy = target.location.y - self.entity.location.y
        
        distance = self.entity.location.chebyshev_distance(target.location)
        if self.engine.game_map.is_visible(self.entity.location):
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()

            self.path = self.get_path_to(target.location)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.location.x, dest_y - self.entity.location.y,
            ).perform()

        return WaitAction(self.entity).perform()

class ConfusedEnemy(BaseAI):
    """
    A confused enemy will stumble around aimlessly for a given number of turns, then revert back to its previous AI.
    If an actor occupies a tile it is randomly moving into, it will attack.
    """

    def __init__(
        self, entity, previous_ai: Optional[any], turns_remaining: int
    ):
        super().__init__(entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def perform(self) -> None:
        # Revert the AI back to the original state if the effect has run its course.
        if self.turns_remaining <= 0:
            self.engine.message_log.add_message(
                f"The {self.entity.name} is no longer confused."
            )
            self.entity.ai = self.previous_ai
        else:
            # Pick a random direction
            direction_x, direction_y = random.choice(
                [
                    (-1, -1),  # Northwest
                    (0, -1),  # North
                    (1, -1),  # Northeast
                    (-1, 0),  # West
                    (1, 0),  # East
                    (-1, 1),  # Southwest
                    (0, 1),  # South
                    (1, 1),  # Southeast
                ]
            )

            self.turns_remaining -= 1

            # The actor will either try to move or attack in the chosen random direction.
            # Its possible the actor will just bump into the wall, wasting a turn.
            return BumpAction(self.entity, direction_x, direction_y,).perform()