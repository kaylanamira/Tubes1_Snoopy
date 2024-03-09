from typing import Tuple, Optional, List
from math import dist
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import *
from ..util import clamp

# Defensive clamp + most profitable(no enemy)
class DefensiveProfitLogic2(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None
        
    # Calculate next move based on the nearest diamond from bot
    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        props = board_bot.properties
        current_position = board_bot.position

        if (props.diamonds == 5 or (props.diamonds == 4 and self.diamondtargetpoint == 2)) and current_position != board_bot.properties.base: 
            # Move to base if inventory is full or inventory is 4 and the target diamond is 2 points and not already in base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            # Detect a list of diamond in board
            diamonds = board.diamonds

            # Aim for the most profitable diamond
            target = self.getMostProfitable(board_bot, diamonds)
            # target = getMostProfitable(bot,diamonds,enemies)
            self.goal_position = target.position
        
        enemies_coordinate = [bot.position for bot in board.bots if bot.properties.name != board_bot.properties.name]
        
        # Plotting dangerous coordinate
        dangerous_coordinate = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0 or j != 0) and (0 <= current_position.x+i < board.width) and (0 <= current_position.y+j < board.height):
                    dangerous_coordinate.append(Position(current_position.y+j,current_position.x+i))
                else:
                    continue
        
        # Find the intersection between dangerous coordinate and enemies coordinate
        threat = list(filter(lambda x: x in enemies_coordinate, dangerous_coordinate))
        
        if len(threat) != 0:
            directions = [(1,0), (-1,0), (0,1), (0,-1)]
            enemy_direction = []
            for coordinate in threat:
                x = clamp(coordinate.x-current_position.x, -1, 1)
                if x != 0 and (x, 0) not in enemy_direction:
                    enemy_direction.append((x, 0))
                y = clamp(coordinate.y-current_position.y, -1, 1)
                if y != 0 and (0, y) not in enemy_direction:
                    enemy_direction.append((0, y))
                
            # List all potential direction to move
            directions = list(filter(lambda x: x not in enemy_direction, directions))
            
            # handling edge----------------------------------------
            if current_position.x == 0: 
                directions.remove((-1,0))
            elif current_position.x == board.width-1:
                directions.remove((1,0))
            if current_position.y == 0:
                directions.remove((0,-1))
            elif current_position.y == board.height-1:
                directions.remove((0,1))

            if len(directions) == 0:
                # No safe direction to move, just move to the nearest diamond
                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    self.goal_position.x,
                    self.goal_position.y,
                )
            
            else:
                # move to the nearest safe direction
                x = clamp(self.goal_position.x-current_position.x, -1, 1)
                y = clamp(self.goal_position.y-current_position.y, -1, 1)
                if (x,0) in directions:
                    delta_x = x
                    delta_y = 0
                elif (0,y) in directions:
                    delta_x = 0
                    delta_y = y
                else:
                    delta_x, delta_y = directions[0][0], directions[0][1]

        else:
            # Move safely to the nearest diamond
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )

        return delta_x, delta_y
    
    def calculateDistance(self, position1: Position, position2: Position):
        # Calculate distance between 2 Position
        return dist([position2.x, position2.y],[position1.x,position1.y])
    
    def getMostProfitable(self, bot: GameObject, diamonds: List[GameObject]) -> GameObject:
        # Find the nearest diamond with most profit
        maxProfit = 0
        for diamond in diamonds:
            distToBot = self.calculateDistance(bot.position,diamond.position)
            distToBase = self.calculateDistance(bot.properties.base,diamond.position)
            profit = (diamond.properties.points)/(distToBot + distToBase)
            
            if (profit >= maxProfit):
                selectedDiamond = diamond
                maxProfit = profit
                self.diamondtargetpoint = diamond.properties.points
        return selectedDiamond