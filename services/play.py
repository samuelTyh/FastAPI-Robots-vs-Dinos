from typing import List, Dict
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


def create_game(dim: int, robots: List[Dict], dinosaurs: List[tuple]) -> Game:
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

    for content in robots:
        row, col = content["coordinate"][0], content["coordinate"][1]
        direction = content["direction"]
        game.set_robots(row=row, column=col, direction=direction)

    game.initial_placement()
    return game


async def move_robot(game: Game, robot_id: str, command: str) -> Game:
    """
    Operate a certain robot to move
    :param game: game instance
    :param robot_id: certain robot id
    :param command: the commands to move the robot
    :return: the game instance
    """

    if command == COMMANDS[0]:
        await game.move_robot_forward(robot_id)

    elif command == COMMANDS[1]:
        await game.move_robot_backward(robot_id)

    elif command == COMMANDS[2]:
        await game.turn_robot_right(robot_id)

    elif command == COMMANDS[3]:
        await game.turn_robot_left(robot_id)

    elif command == COMMANDS[4]:
        await game.attack(robot_id)

    else:
        raise Exception("Unsupported command")

    return game
