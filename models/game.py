from typing import List, Any, Tuple
from services.utils import DIRECTIONS, DIRECTION_BASED_INDEX, MOVING_VECTOR, create_new_board

import pprint
import random


class Board:

    def __init__(self, dim: int):
        self.dim = dim
        self._board = []
        self._robots_count = 0
        self._dinosaurs_count = 0
        self._create_new_board()

    def _create_new_board(self):
        self._board = create_new_board(self.dim)
        self.dinosaurs_position = []
        self.robots_position = []
        self.robots = {}

    def set_dinosaurs(self, row: int = None, column: int = None):
        # Check the total number of occupations in the grid
        if self._dinosaurs_count + self._robots_count >= self.dim * self.dim:
            raise Exception(
                "All positions in the grid have been occupied or you set too many robots/dinosaurs in the grid"
            )

        # create dinosaurs
        if row is None or column is None:
            row = random.randint(0, self.dim-1)
            column = random.randint(0, self.dim-2)

        position = (row, column)
        if not self.is_in_bounds(position):
            raise Exception("The dinosaurs placement is out of grid scope.")
        if position in self.dinosaurs_position or position in self.robots_position:
            return self.set_dinosaurs()

        self.dinosaurs_position.append(position)

    def set_robots(self, row: int = None, column: int = None, direction: str = "E"):
        # Check the total number of occupations in the grid
        if self._dinosaurs_count + self._robots_count >= self.dim * self.dim:
            raise Exception(
                "All positions in the grid have been occupied or you set too many robots/dinosaurs in the grid"
            )

        # create robots
        # define robot random id
        robot_id = str(random.getrandbits(16))

        if row is None or column is None:
            row = random.randint(0, self.dim-1)
            column = random.randint(0, self.dim-1)

        position = (row, column)
        if not self.is_in_bounds(position):
            raise Exception("The robots placement is out of grid scope.")
        if position in self.dinosaurs_position or position in self.robots_position:
            return self.set_robots()
        self.robots_position.append(position)
        self.robots.update(**{robot_id: {"coordinate": position, "direction": direction}})

    def validate_move(self, position):
        # make sure every new piece to place in the valid placement
        if self._board[position] != 0:
            return False
        return True

    def is_in_bounds(self, position):
        if 0 <= position[0] < self.dim and 0 <= position[1] < self.dim:
            return True
        return False

    def get_board(self):
        return self._board

    def delete_board(self):
        self._board = []

    def print_board(self):
        pprint.pprint(self._board)


class Game(Board):

    def __init__(self, dim):
        super().__init__(dim)
        self.game_id = random.randint(1, 9999)
        self._moves = 0
        # indicate each dinosaur has 1 life point
        self._dinosaur_life = 1
        # indicate each robot has 1 attack power
        self._robot_power = -1

    def initial_placement(self):
        # update all pieces to the board
        for piece in self.dinosaurs_position:
            self._board[piece] = self._dinosaur_life

        for piece in self.robots_position:
            self._board[piece] = self._robot_power

        self.print_board()

    def set_random_game(self, robots_count: int = 1, dinosaurs_count: int = 1):
        # default 1 vs 1 game
        if not robots_count:
            robots_count = 1
        if not dinosaurs_count:
            dinosaurs_count = 1

        dinosaurs = 0
        while dinosaurs != dinosaurs_count:
            self.set_dinosaurs()
            dinosaurs += 1

        robots = 0
        while robots != robots_count:
            self.set_robots()
            robots += 1

        self.initial_placement()

    def move_robot_forward(self, robot_id: str):
        position = self.robots[robot_id]["coordinate"]
        direction = self.robots[robot_id]["direction"]
        position_to_list = list(position)

        # head east and west -> move between columns
        # head north and south -> move between rows
        position_to_list[DIRECTION_BASED_INDEX[direction]] += MOVING_VECTOR[direction]
        new_position: Tuple[Any, ...] = tuple(position_to_list)

        if not self.is_in_bounds(new_position):
            raise Exception("The move is invalid, the robot has reached the grid edge")

        if not self.validate_move(new_position):
            raise Exception("The new position has been occupied")

        self.robots[robot_id].update({"coordinate": new_position})
        self._board[position] = 0
        self._board[new_position] = self._robot_power
        self._moves += 1
        self.print_board()

    def move_robot_backward(self, robot_id: str):
        position = self.robots[robot_id]["coordinate"]
        direction = self.robots[robot_id]["direction"]
        position_to_list = list(position)
        position_to_list[DIRECTION_BASED_INDEX[direction]] -= MOVING_VECTOR[direction]
        new_position = tuple(position_to_list)

        if not self.is_in_bounds(new_position):
            raise Exception("The move is invalid, the robot has reached the grid edge")

        if not self.validate_move(new_position):
            raise Exception("The new position has been occupied")

        self.robots[robot_id].update({"coordinate": new_position})
        self._board[position] = 0
        self._board[new_position] = self._robot_power
        self._moves += 1
        self.print_board()

    def turn_robot_right(self, robot_id: str):
        direction = self.robots[robot_id]["direction"]
        new_direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % len(DIRECTIONS)]
        self.robots[robot_id].update({"direction": new_direction})
        self._moves += 1
        self.print_board()

    def turn_robot_left(self, robot_id: str):
        direction = self.robots[robot_id]["direction"]
        new_direction = DIRECTIONS[(DIRECTIONS.index(direction) - 1) % len(DIRECTIONS)]
        self.robots[robot_id].update({"direction": new_direction})
        self._moves += 1
        self.print_board()

    def attack(self, robot_id: str):
        position = self.robots[robot_id]["coordinate"]
        opponents: List[tuple, ...] = [
            (position[0]+1, position[1]),
            (position[0]-1, position[1]),
            (position[0], position[1]+1),
            (position[0], position[1]-1)
        ]

        for opponent in opponents:
            if not self.is_in_bounds(opponent):
                continue
            if self._board[opponent] not in (0, -1):
                self._board[opponent] = self._board[opponent] + self._board[position]
                self.dinosaurs_position.remove(opponent)

        self._moves += 1
        self.print_board()

    def get_number_of_moves(self):
        return self._moves
