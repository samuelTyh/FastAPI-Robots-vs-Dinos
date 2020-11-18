from typing import List
from models.game import Game
from services.utils import COMMANDS


def create_random_game(dim: int, **kargs) -> Game:
    """
    Create a random game instance
    :param dim: grid dimension
    :param kargs: robots_count, dinosaurs_count
    :return: the game instance
    """
    if not dim:
        raise TypeError("Dimension is necessary")
    game = Game(dim)
    game.set_random_game(**kargs)
    return game


def create_game(dim: int, robots: List[tuple], dinosaurs: List[tuple]) -> Game:
    """
    Create a game instance and set certain positions for robots and dinosaurs
    :param dim: grid dimension
    :param robots: set of robots' coordinate (row, column)
    :param dinosaurs:set of dinosaurs' coordinate (row, column)
    :return: the game instance
    """
    if not dim or not robots or not dinosaurs:
        raise TypeError("All variables are necessary")
    game = Game(dim)
    for row, col in dinosaurs:
        game.set_dinosaurs(row=row, column=col)

    for row, col in robots:
        game.set_robots(row=row, column=col)

    game.initial_placement()
    return game


def move_robot(game: Game, robot_id: str, command: str) -> Game:
    """
    Operate a certain robot to move
    :param game: game instance
    :param robot_id: certain robot id
    :param command: the commands to move the robot
    :return: the game instance
    """

    if command == COMMANDS[0]:
        game.move_robot_forward(robot_id)

    elif command == COMMANDS[1]:
        game.move_robot_backward(robot_id)

    elif command == COMMANDS[2]:
        game.turn_robot_right(robot_id)

    elif command == COMMANDS[3]:
        game.turn_robot_left(robot_id)

    elif command == COMMANDS[4]:
        game.attack(robot_id)

    else:
        raise Exception("Unsupported command")

    return game
