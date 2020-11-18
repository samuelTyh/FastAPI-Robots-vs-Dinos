import numpy as np
import pandas as pd

# directions set
DIRECTIONS = ["E", "S", "W", "N"]

# head east and west -> move between columns
# head north and south -> move between rows
DIRECTION_BASED_INDEX = {"E": 1, "S": 0, "W": 1, "N": 0}

# identity vector of each direction
MOVING_VECTOR = {"E": 1, "S": 1, "W": -1, "N": -1}

# commands set
COMMANDS = ["move forward", "move backward", "turn right", "turn left", "attack"]


def create_new_board(dim):
    # create a clear board
    board = np.zeros((dim, dim), dtype=int)
    return board


def create_html(game_id, board, dim):
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
