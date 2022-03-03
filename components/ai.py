from __future__ import annotations

from typing import List, Tuple

import numpy as np  # type: ignore
import tcod
from actions import Action, MeleeAction, MovementAction, WaitAction

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
        if self.engine.game_map.visible[self.entity.location.x, self.entity.location.y]:
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()

            self.path = self.get_path_to(target.location)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.location.x, dest_y - self.entity.location.y,
            ).perform()

        return WaitAction(self.entity).perform()