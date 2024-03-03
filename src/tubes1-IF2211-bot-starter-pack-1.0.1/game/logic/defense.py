import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class defensiveBot(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            self.goal_position = None

        current_position = board_bot.position
        if self.goal_position:
            enemies_coordinate = [bot for bot in board.bots.position if bot.properties.name != board_bot.properties.name]

            self.dangerous_coordinate = []

            for i in range(-2, 3):
                for j in range(-2, 3):
                    if abs(i)+abs(j) <= 2 and i != 0 and j != 0:
                        self.dangerous_coordinate.append(Position(current_position.x+i, current_position.y+j))
                    else:
                        continue

            threat = list(filter(lambda x: x in enemies_coordinate, self.immideate_threats))
            if len(threat) != 0:
                move_direction = [True, True, True, True] # right, up, left, down
                for i in range(len(threat)):
                    if threat[i].x > current_position.x:
                        move_direction[0] = False
                    elif threat[i].x < current_position.x:
                        move_direction[2] = False
                    if threat[i].y > current_position.y:
                        move_direction[1] = False
                    elif threat[i].y < current_position.y:
                        move_direction[3] = False
                
                if True in move_direction:
                    move = move_direction.index(True)
                    if move == 0:
                        delta_x, delta_y = 1, 0
                    elif move == 1:
                        delta_x, delta_y = 0, 1
                    elif move == 2:
                        delta_x, delta_y = -1, 0
                    elif move == 3:
                        delta_x, delta_y = 0, -1
                else:
                    delta_x, delta_y = get_direction(
                        current_position.x,
                        current_position.y,
                        self.goal_position.x,
                        self.goal_position.y,
                    )

            else:
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