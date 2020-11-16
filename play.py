import logging
from game import Game


def start_game():
    game = Game(50)
    game.set_random_game()
    return game


def move_robot(game, command: str):
    robot_id = list(game.robots.keys())[0]
    if command == "move forward":
        game.move_robot_forward(robot_id)

    elif command == "move backward":
        game.move_robot_backward(robot_id)

    elif command == "turn right":
        game.turn_robot_right(robot_id)

    elif command == "turn left":
        game.turn_robot_left(robot_id)

    elif command == "attack":
        game.attack(robot_id)

    else:
        logging.error("Unsupported command")

    return game
