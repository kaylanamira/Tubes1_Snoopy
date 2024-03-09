import math
from typing import Optional
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

def distance(object1position, object2position) :
    distance = math.sqrt(math.pow(abs(object1position.x - object2position.x), 2) + math.pow(abs(object1position.y - object2position.y), 2))
    return distance

class NearestBaseLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)] # valid position
        self.goal_position: Optional[Position] = None # position ini defaultnya adalah None jika bot belum mengetahui position si bot, value atribut ini None,
                                                      # tapi kalau sudah ada update pergerakan, value atributnya terunion dengan current position bot
        self.current_direction = 0                                                                                                                                    

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
            # base = board_bot.properties.base # base = rumah tempat bot nge-store hasil diamond ambilannya
            self.goal_position = base # ketika diamond sudah full, dia akan mengubah value goal_position menjadi menuju base
        elif props.diamonds < 5 :
            if props.diamonds == 0 : 
                self.goal_position = diamond_list[min_distance_index].position # else masih ngumpulin diamond

            else : 
                if distance(diamond_list[min_distance_index].position, base) >= 1.75 * distance(current_position, base) :
                    self.goal_position = base
                else : 
                    self.goal_position = diamond_list[min_distance_index].position
        else :
            self.goal_position = base
        
        # if self.goal_position: # Ketika punya goal position, bot akan menerima tujuan pergerakan dari get_direction
        #     # We are aiming for a specific position, calculate delta

        delta_x, delta_y = get_direction(
        current_position.x,
        current_position.y,
        self.goal_position.x,
        self.goal_position.y,
        )

        return delta_x, delta_y