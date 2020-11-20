import numpy as np
import pandas as pd

# The directions set, clockwise order
DIRECTIONS = ["E", "S", "W", "N"]

# Heading east and west -> move between columns
# Heading north and south -> move between rows
DIRECTION_BASED_INDEX = {"E": 1, "S": 0, "W": 1, "N": 0}

# Identity vector of each direction
MOVING_VECTOR = {"E": 1, "S": 1, "W": -1, "N": -1}

# The commands set
COMMANDS = ["move forward", "move backward", "turn right", "turn left", "attack"]


def create_new_board(dim: int) -> np.ndarray:
    """
    :param dim: dimension of the grid
    :return: a zero-matrix composed by numpy 2d array
    """
    # create a clear board
    if not dim:
        raise TypeError("Dimension is necessary")
    board = np.zeros((dim, dim), dtype=int)
    return board


def select_empty_position(board):
    """
    Select an empty postion to put entity on
    :param board: board instance
    :return: list of available choices
    """
    result = np.where(board == 0)
    list_of_coordinate = list(zip(result[0], result[1]))
    numpyint64_to_int = [(row.item(), col.item()) for row, col in list_of_coordinate]
    return numpyint64_to_int


def create_html(game_id: str, board: np.ndarray, dim: int):
    """
    Display game board in HTML format via pandas
    :param game_id: a specified game id
    :param board: the game board presented by numpy 2d array
    :param dim: dimension of the grid
    :return: html
    """
    # create simple table in html format
    columns = [f"{n}" for n in range(dim)]
    df = pd.DataFrame(board, columns=columns)
    df = df.replace(0, " ")
    html = df.to_html(
        table_id=game_id,
        col_space=30,
        border=1,
        justify="center",
        show_dimensions=True,
        classes="table table-striped"
    )
    return html
