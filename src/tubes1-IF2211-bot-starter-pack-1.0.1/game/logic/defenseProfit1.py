from typing import Tuple, Optional, List
from math import dist
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import *

#Defensive without clamp + most profitable(no enemy)
class DefensiveProfitLogic1(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        
    # Calculate next move based on the nearest diamond from bot
    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        props = board_bot.properties

        if props.diamonds >= 5: 
            # Move to base if inventory full
            base = board_bot.properties.base
            self.goal_position = base
        else:
            # Detect a list of diamond in board
            diamonds = board.diamonds

            # Aim for the most profitable diamond
            target = self.getMostProfitable(board_bot, diamonds)
            # target = getMostProfitable(bot,diamonds,enemies)
            self.goal_position = target.position
        
        current_position = board_bot.position
        enemies_coordinate = [bot.position for bot in board.bots if bot.properties.name != board_bot.properties.name]
        self.dangerous_coordinate = []

        for i in range(-2, 3):
            for j in range(-2, 3):
                if abs(i)+abs(j) <= 2 and (i != 0 or j != 0) and (0 <= current_position.x+i < board.width) and (0 <= current_position.y+j < board.height):
                    self.dangerous_coordinate.append(Position(current_position.y+j,current_position.x+i))
                else:
                    continue
        
        threat = list(filter(lambda x: x in enemies_coordinate, self.dangerous_coordinate))

        if len(threat) != 0:
            
            move_direction = [1, 1, 1, 1] # right, left, up, down
            for i in range(len(threat)):
                
                if threat[i].x > current_position.x or current_position.x == board.width-1:
                    move_direction[0] = 0
                elif threat[i].x < current_position.x or current_position.x == 0:
                    move_direction[1] = 0
                if threat[i].y > current_position.y or current_position.y == board.height-1:
                    move_direction[2] = 0
                elif threat[i].y < current_position.y or current_position.y == 0:
                    move_direction[3] = 0
                
            if 1 in move_direction:
                goal_direction = [0, 0, 0, 0] # right, left, up, down
                if self.goal_position.x > current_position.x or current_position.x < board.width-1:
                    goal_direction[0] = 1
                elif self.goal_position.x < current_position.x or current_position.x > 0:
                    goal_direction[1] = 1
                if self.goal_position.y > current_position.y or current_position.y < board.height-1:
                    goal_direction[2] = 1
                elif self.goal_position.y < current_position.y or current_position.y > 0:
                    goal_direction[3] = 1
                
                result = [i for i, (x, y) in enumerate(zip(move_direction, goal_direction)) if x == y == 1]

                if len(result) != 0:
                    move = result[0]
                else:
                    move = move_direction.index(1)

                if move == 0:
                    delta_x, delta_y = 1, 0
                elif move == 1:
                    delta_x, delta_y = -1, 0
                elif move == 2:
                    delta_x, delta_y = 0, 1
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
        return selectedDiamond