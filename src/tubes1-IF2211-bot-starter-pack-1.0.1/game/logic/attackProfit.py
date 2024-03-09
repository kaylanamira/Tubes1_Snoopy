from typing import Tuple, Optional, List
from math import dist, inf
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import *

class AttackProfitLogic(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None
        self.aim_for_teleporter = False
        self.diamondtargetpoint: Optional[int] = None
        
    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        props = board_bot.properties
        current_position = board_bot.position

        direction = [(1,0), (-1,0), (0,1), (0,-1)]
        # handling edge
        if current_position.x == 0: 
            direction.remove((-1,0))
        elif current_position.x == board.width-1:
            direction.remove((1,0))
        if current_position.y == 0:
            direction.remove((0,-1))
        elif current_position.y == board.height-1:
            direction.remove((0,1))
        
        diamonds = []
        teleporters = {}
        for object in board.game_objects:
            if object.type == "DiamondGameObject":
                diamonds.append(object)
            elif object.type == "TeleportGameObject":
                if object.properties.pair_id not in teleporters:
                    teleporters[object.properties.pair_id] = []
                teleporters[object.properties.pair_id].append(object)

        nearestTeleporter = None
        minDist = inf
        for key in teleporters:
            for teleporter in teleporters[key]:
                distTeleporterToBot = self.calculateDistance(board_bot.position,teleporter.position)
                if (distTeleporterToBot < minDist):
                    nearestTeleporter = teleporter
                    minDist = distTeleporterToBot
        nearestTeleporterIdx = teleporters[nearestTeleporter.properties.pair_id].index(nearestTeleporter) 

        if (props.diamonds == 5 or (props.diamonds == 4 and self.diamondtargetpoint == 2)) and current_position != board_bot.properties.base: 
            base = board_bot.properties.base
            self.goal_position = base

        else:
            if (nearestTeleporterIdx == 0): 
                nearestTeleporterPair = teleporters[nearestTeleporter.properties.pair_id][1]
            else:       
                nearestTeleporterPair = teleporters[nearestTeleporter.properties.pair_id][0]

            target = self.getMostProfitable(board_bot, diamonds, nearestTeleporter, nearestTeleporterPair)
            self.goal_position = target.position if not self.aim_for_teleporter else nearestTeleporter.position
        
        enemies_coordinate = [bot.position for bot in board.bots if bot.properties.name != board_bot.properties.name]

        if not self.aim_for_teleporter:
            if current_position.x+1 == nearestTeleporter.position.x and current_position.y == nearestTeleporter.position.y:
                direction.remove((1,0))
            elif current_position.x-1 == nearestTeleporter.position.x and current_position.y == nearestTeleporter.position.y:
                direction.remove((-1,0))
            if current_position.y+1 == nearestTeleporter.position.y and current_position.x == nearestTeleporter.position.x:
                direction.remove((0,1))
            elif current_position.y-1 == nearestTeleporter.position.y and current_position.x == nearestTeleporter.position.x:
                direction.remove((0,-1))
        
        for coord in enemies_coordinate:
            if dist([coord.x, coord.y], [current_position.x, current_position.y]) <= 1.5: # sqrt(2) = 1.414
                x = clamp(coord.x-current_position.x, -1, 1)
                if x != 0 and (x, 0) in direction:
                    return x,0
                y = clamp(coord.y-current_position.y, -1, 1)
                if y != 0 and (0, y) in direction:
                    return 0,y
        
        x = clamp(self.goal_position.x-current_position.x, -1, 1)
        y = clamp(self.goal_position.y-current_position.y, -1, 1)
        if (x,0) in direction:
            delta_x = x
            delta_y = 0
        elif (0,y) in direction:
            delta_x = 0
            delta_y = y
        else:
            delta_x, delta_y = direction[0]
        
        return delta_x, delta_y
    
    
    def calculateDistance(self, position1: Position, position2: Position):
        return dist([position2.x, position2.y],[position1.x,position1.y])
    
    def getMostProfitable(self, bot: GameObject, diamonds: List[GameObject], nearestTeleporter:GameObject, nearestTeleporterPair:GameObject) -> GameObject:
        maxProfit = 0

        for diamond in diamonds:
            realdistToBot = self.calculateDistance(bot.position,diamond.position)
            altDistToBot = self.calculateDistance(nearestTeleporter.position,bot.position) + self.calculateDistance(nearestTeleporterPair.position,diamond.position)
            if (realdistToBot > 1.5 * altDistToBot):
                self.aim_for_teleporter = True
                distToBot = altDistToBot
            else:
                self.aim_for_teleporter = False
                distToBot = realdistToBot
            distToBase = self.calculateDistance(bot.properties.base,diamond.position)
            profit = (diamond.properties.points)/(distToBot + distToBase)
            
            if (profit >= maxProfit):
                selectedDiamond = diamond
                maxProfit = profit
                self.diamondtargetpoint = diamond.properties.points
        return selectedDiamond