from typing import Tuple, Optional, List
from math import dist,inf

# --------------------------------------UNCOMMENT IF NOT TESTING ------------------------------------------
# from game.logic.base import BaseLogic
# from game.models import GameObject, Board, Position, Properties
# from ..util import *

# --------------------------------------TESTING PURPOSES------------------------------------------
from abc import ABC
from dataclasses import dataclass
from typing import List, Optional, Union
from colorama import Fore, Style

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

def get_direction(current_x, current_y, dest_x, dest_y):
    delta_x = clamp(dest_x - current_x, -1, 1)
    delta_y = clamp(dest_y - current_y, -1, 1)
    if delta_x != 0:
        delta_y = 0
    return (delta_x, delta_y)


@dataclass
class Bot:
    name: str
    email: str
    id: str


@dataclass
class Position:
    y: int
    x: int


@dataclass
class Base(Position): ...


@dataclass
class Properties:
    points: Optional[int] = None
    pair_id: Optional[str] = None
    diamonds: Optional[int] = None
    score: Optional[int] = None
    name: Optional[str] = None
    inventory_size: Optional[int] = None
    can_tackle: Optional[bool] = None
    milliseconds_left: Optional[int] = None
    time_joined: Optional[str] = None
    base: Optional[Base] = None


@dataclass
class GameObject:
    id: int
    position: Position
    type: str
    properties: Optional[Properties] = None


@dataclass
class Config:
    generation_ratio: Optional[float] = None
    min_ratio_for_generation: Optional[float] = None
    red_ratio: Optional[float] = None
    seconds: Optional[int] = None
    pairs: Optional[int] = None
    inventory_size: Optional[int] = None
    can_tackle: Optional[bool] = None


@dataclass
class Feature:
    name: str
    config: Optional[Config] = None


@dataclass
class Board:
    id: int
    width: int
    height: int
    features: List[Feature]
    minimum_delay_between_moves: int
    game_objects: Optional[List[GameObject]]

    @property
    def bots(self) -> List[GameObject]:
        return [d for d in self.game_objects if d.type == "BotGameObject"]

    @property
    def diamonds(self) -> List[GameObject]:
        return [d for d in self.game_objects if d.type == "DiamondGameObject"]

    def get_bot(self, bot: Bot) -> Optional[GameObject]:
        for b in self.bots:
            if b.properties.name == bot.name:
                return b
        return None

    def is_valid_move(
        self, current_position: Position, delta_x: int, delta_y: int
    ) -> bool:
        if not (-1 <= delta_x <= 1) or not (-1 <= delta_y <= 1):
            print(
                Fore.RED + Style.BRIGHT + "Invalid move:" + Style.RESET_ALL,
                "Delta values must be between -1 and 1 inclusive",
            )
            return False

        if delta_x == delta_y:
            print(
                Fore.RED + Style.BRIGHT + "Invalid move:" + Style.RESET_ALL,
                "Delta_x and delta_y cannot be equal",
            )
            return False

        if not (0 <= current_position.x + delta_x < self.width):
            print(
                Fore.RED + Style.BRIGHT + "Invalid move:" + Style.RESET_ALL,
                "X-coordinate out of bounds",
            )
            return False

        if not (0 <= current_position.y + delta_y < self.height):
            print(
                Fore.RED + Style.BRIGHT + "Invalid move:" + Style.RESET_ALL,
                "Y-coordinate out of bounds",
            )
            return False

        return True


class BaseLogic(ABC):
    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        raise NotImplementedError()

# --------------------------------------TESTING PURPOSES------------------------------------------

class DiamondFromBotLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        
    # Calculate next move based on the nearest diamond from bot
    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        props = board_bot.properties

        if props.diamonds == 5: 
            # Move to base if inventory full
            base = board_bot.properties.base
            self.goal_position = base
        else:
            # Detect a list of diamond in board
            diamonds = board.diamonds

            # Detect other bots in board
            enemies = [bot for bot in board.bots if bot.properties.name != board_bot.properties.name]

            # Aim for the nearest diamond
            target = self.getNearestDiamond(board_bot, diamonds)
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
            nearestEnemy = min(bots, key=lambda x: self.calculateDistance(x.position,diamond.position)) # nearest enemy from diamond
            distToBot = self.calculateDistance(bot.position,diamond.position)
            distToBase = self.calculateDistance(bot.properties.base,diamond.position)
            distToEnemy = self.calculateDistance(nearestEnemy.position,diamond.position)
            profit = (distToEnemy + diamond.properties.points)/(distToBot + distToBase)

            print(profit)
            print()
            
            if (profit >= maxProfit):
                selectedDiamond = diamond
                maxProfit = profit
        return selectedDiamond

    def getNearestDiamond(self, bot: GameObject, diamonds: List[GameObject]) -> GameObject:
        # Find the nearest diamond with biggest point
        minDistance = inf
        redDiamondExist = False
        minRedDistance = inf
        for diamond in diamonds:
            if (redDiamondExist and diamond.properties.points == 1):
                # Prioritize choosing the red diamond 
                continue
            distToBot = self.calculateDistance(bot.position,diamond.position)
            if (diamond.properties.points == 2 and not redDiamondExist):
                # First red diamond found
                redDiamondExist = True
                minRedDistance = distToBot
            if (distToBot <= minDistance or (redDiamondExist and distToBot <= minRedDistance)):
                minDistance = distToBot
                nearestDiamond = diamond
        return nearestDiamond
    
    
    
# --------------------------------------TESTING PURPOSES------------------------------------------
def main():
    botposition = Position(0,0)
    props = Properties(diamonds=5,base=Base(0,0))
    bot = GameObject(1,botposition,"bot",props)
    otherbots = [GameObject(7,Position(9,4),"bot",props),GameObject(8,Position(2,2),"bot",props)]

    diamonds = [GameObject(2,Position(4,3),"diamond",Properties(points=1)), GameObject(3,Position(2,2),"diamond",Properties(points=1)), GameObject(4,Position(7,7),"diamond",Properties(points=2)), GameObject(5,Position(3,3),"diamond",Properties(points=2)), GameObject(6,Position(10,5),"diamond",Properties(points=2))]
    # board = Board(1,15,15)
    logic = DiamondFromBotLogic()
    # nearest = logic.getNearestDiamond(bot,diamonds)
    mostprofitable = logic.getMostProfitable(bot,diamonds,otherbots)
    # print(nearest)
    print(mostprofitable)
    # deltax, deltay = logic.next_move(bot,board)
main()