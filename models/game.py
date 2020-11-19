from typing import List
from services.utils import DIRECTIONS, DIRECTION_BASED_INDEX, MOVING_VECTOR, create_new_board

import pprint
import random
import logging

logger = logging.getLogger(__name__)


class Board:

    """ Initialize the size of the game board and the number of roles in each camp. """

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
        """
        Set the position of dinosaurs
        :param row: the row coordinate of the position
        :param column: the column coordinate of the position
        :return: the list of dinosaurs' positions
        """
        # Check the total number of occupied in the grid
        if self._dinosaurs_count + self._robots_count >= self.dim * self.dim:
            logger.error("No vacancy for new roles on the game board")
            raise Exception(
                "All positions in the grid have been occupied or you set too many robots/dinosaurs in the grid"
            )

        # Create dinosaurs by random selection if the position not specified or specified wrong
        if row is None or column is None:
            row = random.randint(0, self.dim-1)
            column = random.randint(0, self.dim-1)

        position = (row, column)
        if not self.is_in_grid(position):
            logger.error(f"The position {position} is out of grid")
            raise Exception("The dinosaurs placement is out of grid scope")

        # Re-run a selection if the position is occupied
        if position in self.dinosaurs_position or position in self.robots_position:
            logger.info(f"The position {position} is occupied, re-run selection")
            return self.set_dinosaurs()

        # Record the position of a new role
        logger.info(f"Set a dinosaur at {position}")
        self.dinosaurs_position.append(position)

    def set_robots(self, row: int = None, column: int = None, direction: str = "E"):
        """
        Set the position of robots
        :param row: the row coordinate of the position
        :param column: the column coordinate of the position
        :param direction: the facing direction of the robot, the default is east (->)
        :return: the list of robots' positions, the dictionary of robots' detailed position
        """
        # Check the total number of occupied in the grid
        if self._dinosaurs_count + self._robots_count >= self.dim * self.dim:
            logger.error("No vacancy for new roles on the game board")
            raise Exception(
                "All positions in the grid have been occupied or you set too many robots/dinosaurs in the grid"
            )

        # Create robots
        # Define a random id for robot
        robot_id = str(random.getrandbits(16))

        # Create robots by random selection if the position not specified or specified wrong
        if row is None or column is None:
            row = random.randint(0, self.dim-1)
            column = random.randint(0, self.dim-1)

        position = (row, column)
        if not self.is_in_grid(position):
            logger.error(f"The position {position} is out of grid")
            raise Exception("The robots placement is out of grid scope")

        # Re-run a selection if the position is occupied
        if position in self.dinosaurs_position or position in self.robots_position:
            logger.info(f"The position {position} is occupied, re-run selection")
            return self.set_robots()

        # Record the position of a new role
        logger.info(f"Set a robot at {position}, facing {direction}")
        self.robots_position.append(position)
        self.robots.update(**{robot_id: {"coordinate": position, "direction": direction}})

    def validate_move(self, position: (int, int)):
        # Check the next move is an empty space
        if self._board[position] != 0:
            return False
        return True

    def is_in_grid(self, position: (int, int)):
        # Check the next move is within boundaries
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

    """ Inherit the Board instance and begin a game"""

    def __init__(self, dim):
        super().__init__(dim)
        self.game_id = random.randint(1, 9999)

        # The total number of move in a game
        self._moves = 0

        # Indicate each dinosaur has 1 life point
        self._dinosaur_life = 1

        # Indicate each robot has 1 attack power
        self._robot_power = -1

    def initial_placement(self):
        # Place all roles to the board
        for dinosaur in self.dinosaurs_position:
            self._board[dinosaur] = self._dinosaur_life

        for robot in self.robots_position:
            self._board[robot] = self._robot_power

        self.print_board()

    def set_random_game(self, robots_count: int = 1, dinosaurs_count: int = 1):
        """
        Set a random-placement game, define the number of roles in each camp
        :param robots_count: the total number of robots, the default is 1
        :param dinosaurs_count: the total number of dinosaurs, the default is 1
        """
        # The default is an 1 vs 1 game
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
        """
        Move a specified robot forward
        :param robot_id: the robot id
        """
        # Retrieve robot's detailed placement
        position = self.robots[robot_id]["coordinate"]
        direction = self.robots[robot_id]["direction"]

        # Convert position tuple to a list in order to update coordinate
        assert isinstance(position[0], int), "position must be a tuple of 2 integers"
        assert isinstance(position[1], int), "position must be a tuple of 2 integers"
        assert isinstance(direction, str), "direction must be a string of 'E', 'S', 'W', 'N'"
        position_to_list = list(position)

        # heading east or west -> move between columns, index 1
        # heading north or south -> move between rows, index 0
        position_to_list[DIRECTION_BASED_INDEX[direction]] += MOVING_VECTOR[direction]

        # Convert new position back to a tuple in order to update
        new_position = tuple(position_to_list)

        if not self.is_in_grid(new_position):
            logger.error(f"The new position {new_position} is out of grid")
            raise Exception("The move is invalid, the robot has reached the grid edge")

        if not self.validate_move(new_position):
            logger.error(f"The new position {new_position} is occupied")
            raise Exception("The new position has been occupied")

        logger.info(f"The robot moves forward from {position} to {new_position}, facing {direction} ")
        self.robots[robot_id].update({"coordinate": new_position})

        # Remove origin record on the board
        self._board[position] = 0

        # Set robot in the new position
        self._board[new_position] = self._robot_power
        self._moves += 1
        self.print_board()

    def move_robot_backward(self, robot_id: str):
        """
        Move a specified robot backward
        :param robot_id: the robot id
        """
        # Retrieve robot's detailed placement
        position = self.robots[robot_id]["coordinate"]
        direction = self.robots[robot_id]["direction"]

        # Convert position tuple to a list in order to update coordinate
        assert isinstance(position[0], int), "position must be a tuple of 2 integers"
        assert isinstance(position[1], int), "position must be a tuple of 2 integers"
        assert isinstance(direction, str), "direction must be a string of 'E', 'S', 'W', 'N'"
        position_to_list = list(position)

        # heading east or west -> move between columns, index 1
        # heading north or south -> move between rows, index 0
        position_to_list[DIRECTION_BASED_INDEX[direction]] -= MOVING_VECTOR[direction]

        # Convert new position back to a tuple in order to update
        new_position = tuple(position_to_list)

        if not self.is_in_grid(new_position):
            logger.error(f"The new position {new_position} is out of grid")
            raise Exception("The move is invalid, the robot has reached the grid edge")

        if not self.validate_move(new_position):
            logger.error(f"The new position {new_position} is occupied")
            raise Exception("The new position has been occupied")

        logger.info(f"The robot moves backward from {position} to {new_position}, facing {direction}")
        self.robots[robot_id].update({"coordinate": new_position})

        # Remove origin record on the board
        self._board[position] = 0

        # Set robot in the new position
        self._board[new_position] = self._robot_power
        self._moves += 1
        self.print_board()

    def turn_robot_right(self, robot_id: str):
        """
        Turn a specified robot right
        :param robot_id: the robot id
        """
        # Retrieve robot's direction
        direction = self.robots[robot_id]["direction"]

        # Directions order is clockwise, i.e. DIRECTION = ["E", "S", "W", "N"]
        new_direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % len(DIRECTIONS)]

        # Update new direction
        logger.info(f"The robot turns right from facing {direction} to {new_direction}")
        self.robots[robot_id].update({"direction": new_direction})
        self._moves += 1
        self.print_board()

    def turn_robot_left(self, robot_id: str):
        """
        Turn a specified robot left
        :param robot_id: the robot id
        """
        # Retrieve robot's direction
        direction = self.robots[robot_id]["direction"]

        # Directions order is clockwise, i.e. DIRECTION = ["E", "S", "W", "N"]
        new_direction = DIRECTIONS[(DIRECTIONS.index(direction) - 1) % len(DIRECTIONS)]

        # Update new direction
        logger.info(f"The robot turns left from facing {direction} to {new_direction}")
        self.robots[robot_id].update({"direction": new_direction})
        self._moves += 1
        self.print_board()

    def attack(self, robot_id: str):
        """
        Attack opponents in four directions around the robot
        :param robot_id: the robot id
        """
        # Retrieve robot's coordinate
        position = self.robots[robot_id]["coordinate"]

        # The list of positions that can be attacked
        opponents: List[(int, int)] = [
            (position[0]+1, position[1]),
            (position[0]-1, position[1]),
            (position[0], position[1]+1),
            (position[0], position[1]-1)
        ]
        _defeated = 0
        for opponent in opponents:
            # Pass the location which is out of grid
            if not self.is_in_grid(opponent):
                continue

            # Attack if the position in opponents list is occupied by dinosaurs
            if self._board[opponent] not in (0, -1):
                self._board[opponent] = self._board[opponent] + self._board[position]
                self.dinosaurs_position.remove(opponent)
                _defeated += 1

        logger.info(f"{_defeated} opponents were defeated")
        self._moves += 1
        self.print_board()

    def get_number_of_moves(self):
        return self._moves
