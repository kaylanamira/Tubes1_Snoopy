import math
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import *

def distance(object1position, object2position) :
    distance = math.sqrt(math.pow(abs(object1position.x - object2position.x), 2) + math.pow(abs(object1position.y - object2position.y), 2))
    return distance

class NearestBaseDefLogic(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None # position defaultnya adalah None jika bot belum mengetahui position bot
        # jika sudah ada update pergerakan, value atributnya terunion dengan current position bot

    def next_move(self, board_bot: GameObject, board: Board): # akan mengembalikan data ke mana bot akan bergerak
        props = board_bot.properties
        base = board_bot.properties.base
        # Analyze new state
        
        diamond_base_distances = []
        diamond_list = board.diamonds
        for diamond in diamond_list :
            diamond_base_distances.append(distance(diamond.position, base))
        
        min_distance = diamond_base_distances[0]
        min_distance_index = 0
        for i, distance_info in enumerate(diamond_base_distances) :
            if distance_info <= min_distance :
                min_distance = distance_info
                min_distance_index = i

        current_position = board_bot.position

        # Proses menentukan goal position
        if props.diamonds == 5 :
            # Move to base
            self.goal_position = base # ketika diamond sudah full, ubah value goal_position menjadi menuju base
        elif props.diamonds < 5 :
            if props.diamonds == 0 : 
                self.goal_position = diamond_list[min_distance_index].position # else masih ngumpulin diamond

            else : 
                if distance(diamond_list[min_distance_index].position, base) >= 1.75 * distance(current_position, base) :
                    # Bergerak ke base jika jarak diamond ke base >= 1.75 * jarak bot ke base
                    self.goal_position = base
                else : 
                    # Bergerak ke diamond terdekat jika jarak diamond ke base < 1.75 * jarak bot ke base
                    self.goal_position = diamond_list[min_distance_index].position
        else :
            self.goal_position = base
        
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
            
            print("Threat detected")
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
                print("Moving to safety")
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
                    print("Intersection detected")
                    move = result[0]
                else:
                    # No intersection between goal_position and move_direction
                    print("No intersection detected")
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
                # if the bot is surrounded by enemies ; move_direction = [0, 0, 0, 0]
                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    self.goal_position.x,
                    self.goal_position.y,
                )
        else:
            # No threat detected; move to targeted diamond
            print("No threat detected")
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )

        return delta_x, delta_y