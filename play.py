from game import Game
from utils import COMMANDS


def create_game(dim, **kargs):
    game = Game(dim)
    game.set_random_game(**kargs)
    return game


def move_robot(game: object, robot_id: str, command: str):

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
