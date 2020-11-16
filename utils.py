import numpy as np

DIRECTIONS = ["E", "S", "W", "N"]
DIRECTION_BASED_INDEX = {"E": 1, "S": 0, "W": 1, "N": 0}
MOVING_STEP = {"E": 1, "S": 1, "W": -1, "N": -1}
COMMANDS = ["move forward", "move backward", "turn right", "turn left", "attack"]


def create_new_board(dim):
    # create a clear board
    board = np.zeros((dim, dim), dtype=int)
    return board