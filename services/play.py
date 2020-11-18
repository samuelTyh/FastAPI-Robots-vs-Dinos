from models.game import Game
from services.utils import COMMANDS


def create_game(dim: int, **kargs) -> Game:
    """
    Create a game instance
    :param dim: grid dimension
    :param kargs: robots_count, dinosaurs_count
    :return: the game instance
    """
    game = Game(dim)
    game.set_random_game(**kargs)
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
