import random
from typing import Tuple, Optional, List
from math import dist,inf
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import *

class DiamondFromBotLogic(BaseLogic):
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

            # Detect other bots in board
            enemies = [bot for bot in board.bots if bot.properties.name != board_bot.properties.name]

            # Aim for the nearest diamond
            target = self.getMostProfitable(board_bot, diamonds, enemies)
            # target = getMostProfitable(bot,diamonds,enemies)
            self.goal_position = target.position

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
        
            self.current_direction = (self.current_direction + 1) % len(
                self.directions)
                
        return delta_x, delta_y
    
    
    def calculateDistance(self, position1: Position, position2: Position):
        # Calculate distance between 2 Position
        return dist([position2.x, position2.y],[position1.x,position1.y])
    
    def getMostProfitable(self, bot: GameObject, diamonds: List[GameObject], bots: List[GameObject]) -> GameObject:
        # Find the nearest diamond with most profit
        maxProfit = 0
        for diamond in diamonds:
            nearestEnemy = min(bots, key=lambda x: self.calculateDistance(x.position,diamond.position)) # nearest enemy from diamond, x = enemy
            distToBot = self.calculateDistance(bot.position,diamond.position)
            distToBase = self.calculateDistance(bot.properties.base,diamond.position)
            distToEnemy = self.calculateDistance(nearestEnemy.position,diamond.position)
            profit = (diamond.properties.points)/(distToBot + (distToBase))

            print(profit)
            print()
            
            if (profit >= maxProfit):
                selectedDiamond = diamond
                maxProfit = profit
        return selectedDiamond

    def getNearestDiamond(self, bot: GameObject, diamonds: List[GameObject]) -> GameObject:
        # Find the nearest diamond with biggest point
        minDistance = inf #infinity
        redDiamondExist = False
        minRedDistance = inf
        for diamond in diamonds:
            if (redDiamondExist and diamond.properties.points == 1):
                # Prioritize choosing the red diamond 
                continue
            distToBot = self.calculateDistance(bot.position,diamond.position)
            if (diamond.properties.points == 2 and not redDiamondExist):  #indicates the finding of first diamond
                # First red diamond found
                redDiamondExist = True
                minRedDistance = distToBot
            if (distToBot <= minDistance or (redDiamondExist and distToBot <= minRedDistance)):
                minDistance = distToBot
                nearestDiamond = diamond
        return nearestDiamond