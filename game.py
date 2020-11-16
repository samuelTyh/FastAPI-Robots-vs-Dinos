from utils import DIRECTIONS, DIRECTION_BASED_INDEX, MOVING_STEP, create_new_board

import pprint
import uuid
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
        if not row or not column:
            row = random.randint(0, self.dim-1)
            column = random.randint(0, self.dim-1)
        if row >= self.dim or column >= self.dim:
            raise ValueError("The dinosaurs placement is out of grid scope.")
        if (row, column) in self.dinosaurs_position:
            return self.set_dinosaurs()

        self.dinosaurs_position.append((row, column))

    def set_robots(self, row: int = None, column: int = None, direction: str = "E"):
        # create robots
        # define robot uuid
        robot_id = str(uuid.uuid4())
        if not row or not column:
            row = random.randint(0, self.dim-1)
            column = random.randint(0, self.dim-1)
        if row >= self.dim or column >= self.dim:
            raise ValueError("The robots placement is out of grid scope.")
        if (row, column) in self.dinosaurs_position or (row, column) in self.robots_position:
            return self.set_robots()
        self.robots_position.append((row, column))
        self.robots.update(**{robot_id: {"coordinate": (row, column), "direction": direction}})

    def initial_placement(self):
        # update all pieces to the board
        for piece in self.dinosaurs_position:
            self._board[piece] = -1

        for piece in self.robots_position:
            self._board[piece] = 1

        self.print_board()

    def validate_placement(self, position):
        # make sure every new piece to place in the valid placement
        if self._board[position] != 0:
            return False
        return True

    def is_in_bounds(self, position):
        if 0 <= position[0] < self.dim and 0 <= position[1] < self.dim:
            return True
        return False


class Game(Board):

    def move_robot_forward(self, robot_id: str):
        position = self.robots[robot_id]["coordinate"]
        direction = self.robots[robot_id]["direction"]
        new_position = list(position)
        new_position[DIRECTION_BASED_INDEX[direction]] += MOVING_STEP[direction]
        new_position = tuple(new_position)

        if not self.is_in_bounds(new_position):
            raise Exception("The move is invalid")

        if not self.validate_placement(new_position):
            raise Exception("The new position has been occupied")

        self.robots[robot_id].update({"coordinate": new_position})
        self._board[position] = 0
        self._board[new_position] = 1
        self.print_board()

    def move_robot_backward(self, robot_id: str):
        position = self.robots[robot_id]["coordinate"]
        direction = self.robots[robot_id]["direction"]
        new_position = list(position)
        new_position[DIRECTION_BASED_INDEX[direction]] -= MOVING_STEP[direction]
        new_position = tuple(new_position)

        if not self.is_in_bounds(new_position):
            raise Exception("The move is invalid")

        if not self.validate_placement(new_position):
            raise Exception("The new position has been occupied")

        self.robots[robot_id].update({"coordinate": new_position})
        self._board[position] = 0
        self._board[new_position] = 1
        self.print_board()

    def turn_robot_right(self, robot_id: str):
        direction = self.robots[robot_id]["direction"]
        new_direction = DIRECTIONS[DIRECTIONS.index(direction) + 1]
        self.robots[robot_id].update({"direction": new_direction})

    def turn_robot_left(self, robot_id: str):
        direction = self.robots[robot_id]["direction"]
        new_direction = DIRECTIONS[DIRECTIONS.index(direction) - 1]
        self.robots[robot_id].update({"direction": new_direction})

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
            if self._board[opponent] == -1:
                self._board[opponent] = 0
                self.dinosaurs_position.remove(opponent)

        self.print_board()
