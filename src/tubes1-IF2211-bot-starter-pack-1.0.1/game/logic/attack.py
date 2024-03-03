import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class AggresiveBot(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        enemies_coordinate = [bot for bot in board.bots.position if bot.properties.name != board_bot.properties.name]
        self.attack_coordinate = []

        for i in range(-1, 2):
                for j in range(-1, 2):
                    if i != 0 and j != 0:
                        self.attack_coordinate.append(Position(current_position.x+i, current_position.y+j))
                    else:
                        continue
        
        enemy = list(filter(lambda x: x in enemies_coordinate, self.attack_coordinate))

        if len(enemy) != 0:
            self.goal_position = enemy[0]
        else:
            self.goal_position = None

        current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )

        else:
            # Roam around
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )
        
        return delta_x, delta_y