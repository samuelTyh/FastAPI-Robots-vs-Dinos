from typing import Any, Tuple

from utils import DIRECTIONS, DIRECTION_BASED_INDEX, MOVING_STEP, create_new_board

import pprint
import random


class Board:
    def __init__(self, dim: int):
        self.dim = dim
        self._board = []
        self._create_new_board()

    def _create_new_board(self):
        self._board = create_new_board(self.dim)
        self.dinosaurs_position = []
        self.robots_position = []
        self.robots = {}

    def print_board(self):
        pprint.pprint(self._board)

    def set_random_game(self, robots_count: int = 1, dinosaurs_count: int = 1):

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

    def set_dinosaurs(self, row: int = None, column: int = None):
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
        # create robots
        # define robot uuid
        robot_id = str(random.randint(1, 9999))

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

    def initial_placement(self):
        # update all pieces to the board
        # indicate each dinosaur has 1 life point
        for piece in self.dinosaurs_position:
            self._board[piece] = 1

        # indicate each robot has 1 attack power
        for piece in self.robots_position:
            self._board[piece] = -1

        self.print_board()

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


class Game(Board):

    def __init__(self, dim):
        super().__init__(dim)
        self.id = self.id = random.randint(1, 9999)
        self._moves = 0

    def move_robot_forward(self, robot_id: str):
        position = self.robots[robot_id]["coordinate"]
        direction = self.robots[robot_id]["direction"]
        position_to_list = list(position)
        position_to_list[DIRECTION_BASED_INDEX[direction]] += MOVING_STEP[direction]
        new_position: Tuple[Any, ...] = tuple(position_to_list)

        if not self.is_in_bounds(new_position):
            raise Exception("The move is invalid, the robot has reached the grid edge")

        if not self.validate_move(new_position):
            raise Exception("The new position has been occupied")

        self.robots[robot_id].update({"coordinate": new_position})
        self._board[position] = 0
        self._board[new_position] = -1
        self._moves += 1
        self.print_board()

    def move_robot_backward(self, robot_id: str):
        position = self.robots[robot_id]["coordinate"]
        direction = self.robots[robot_id]["direction"]
        position_to_list = list(position)
        position_to_list[DIRECTION_BASED_INDEX[direction]] -= MOVING_STEP[direction]
        new_position = tuple(position_to_list)

        if not self.is_in_bounds(new_position):
            raise Exception("The move is invalid, the robot has reached the grid edge")

        if not self.validate_move(new_position):
            raise Exception("The new position has been occupied")

        self.robots[robot_id].update({"coordinate": new_position})
        self._board[position] = 0
        self._board[new_position] = -1
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
        opponents = [
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
