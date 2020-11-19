from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
import logging

from services.utils import COMMANDS, create_html
from models.items import GamePayload, RobotPayload, StartResponse, ErrorMessage
from models.setting import get_app_settings
from services.play import create_random_game, create_game, move_robot
from models.game import Game

# Setting logging
logging.basicConfig(filename='record.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Caching the games by id
GAMES = {}

app_settings = get_app_settings()

app = FastAPI(
    title=app_settings.title,
    description=app_settings.description,
    version=app_settings.version,
    debug=app_settings.debug,
)


@app.get("/")
def read_root() -> RedirectResponse:

    """ The root route, redirect to API document """

    return RedirectResponse("/docs")
    
    
@app.post("/games/start", responses={200: {"model": StartResponse}, 400: {"model": ErrorMessage}})
def start_game(item: GamePayload) -> JSONResponse:
    """
    Start a game
    :param item: parameters to initialize a game instance
    :return: the game information
    """
    try:
        dim, robots, robots_count, dinosaurs, dinosaurs_count = \
            item.grid_dim, item.robots, item.robots_count, item.dinosaurs, item.dinosaurs_count
        if dim <= 2:
            logger.debug(f"The dimension is not big enough: {dim}")
            return JSONResponse(
                status_code=400,
                content={"status": False, "detail": "You must create a bigger grid"}
            )

        if robots and dinosaurs:
            match: Game = create_game(dim, robots=robots, dinosaurs=dinosaurs)
        else:
            match: Game = create_random_game(dim, robots_count=robots_count, dinosaurs_count=dinosaurs_count)

        GAMES[str(match.game_id)] = match
        logger.info(f">>>>>     Game {match.game_id} started     <<<<<<")

        res = {
            "game_id": str(match.game_id),
            "grid": f"{match.dim}*{match.dim}",
            "dinosaurs": len(match.dinosaurs_position),
            "dinosaurs_position": match.dinosaurs_position,
            "robots": len(match.robots_position),
            "robots_position": list(match.robots.values()),
        }

        logger.info(f"{res}")
        return JSONResponse(status_code=200, content=res)

    except Exception as e:  # TODO: http error handler
        logger.error(f"Exception: {e}")
        return JSONResponse(
            status_code=400,
            content={"status": False, "detail": str(e)}
        )


@app.get("/games/{game_id}", responses={400: {"model": ErrorMessage}, 404: {"model": ErrorMessage}})
def display_game(game_id: str) -> HTMLResponse:
    """
    Display the game board in html
    :param game_id: a specified game id
    :return: html page
    """
    try:
        if game_id not in GAMES:
            logger.error(f"Game ID '{game_id}' does not exist")
            return JSONResponse(
                status_code=404,
                content={"status": False, "detail": f"Game ID '{game_id}' does not exist"}
            )
        game = GAMES[game_id]
        html = create_html(game_id, game.get_board(), game.dim)
        return HTMLResponse(content=html, status_code=200)

    except Exception as e:  # TODO: http error handler
        logger.error(f"Exception: {e}")
        return JSONResponse(
            status_code=400,
            content={"status": False, "detail": str(e)}
        )


@app.put("/games/{game_id}",
         responses={200: {"model": StartResponse}, 400: {"model": ErrorMessage}, 404: {"model": ErrorMessage}})
def play_robots(game_id: str, item: RobotPayload) -> JSONResponse:
    """
    Operate specified robot to move forward and backward, turn right and left, and attack
    :param game_id: a specified game id
    :param item: parameters to operate the robot
    :return: the state of current game
    """
    try:
        if game_id not in GAMES:
            logger.error(f"Game ID '{game_id}' does not exist")
            return JSONResponse(
                status_code=404,
                content={"status": False, "detail": f"Game ID '{game_id}' does not exist"}
            )

        game: Game = GAMES[game_id]
        robots_list = list(game.robots.keys())
        chose_robot = str(item.robot_id)
        if chose_robot not in robots_list:
            chose_robot = list(game.robots.keys())[0]
            logger.info(f"Moved robot id: {chose_robot}")
        
        if item.command not in range(5):
            logger.error(f"Invalid command: {item.command}")
            return JSONResponse(
                status_code=400,
                content={
                    "status": False,
                    "detail": "You must insert the correct instructions as following \
                    0 -> forward, 1 -> backward, 2 -> right, 3 -> left, 4 -> attack"
                }
            )

        command = COMMANDS[item.command]
        game = move_robot(game, chose_robot, command)
        res = {
            "game_id": game_id,
            "robot_id": chose_robot,
            "command": command,
            "new_position": game.robots[chose_robot],
            "dinosaurs": len(game.dinosaurs_position),
            "dinosaurs_position": game.dinosaurs_position,
            "number_of_moves": game.get_number_of_moves(),
            "all_dinosaurs_has_been_terminated": not bool(game.dinosaurs_position),
        }
        logger.info(f"{res}")
        if res["all_dinosaurs_has_been_terminated"]:
            logger.info(f">>>>>     Game {game_id} completed     <<<<<<")
        return JSONResponse(status_code=200, content=res)

    except Exception as e:  # TODO: http error handler
        logger.error(f"Exception: {e}")
        return JSONResponse(
            status_code=400,
            content={"status": False, "detail": str(e)}
        )


@app.delete("/games/{game_id}", responses={400: {"model": ErrorMessage}, 404: {"model": ErrorMessage}})
def remove_game(game_id: str) -> JSONResponse:
    """
    Remove a specified game instance in the cache
    :param game_id: a specified game id
    :return: the state of remove
    """
    try:
        if game_id not in GAMES:
            logger.error(f"Game ID '{game_id}' does not exist")
            return JSONResponse(
                status_code=404,
                content={"status": False, "detail": f"Game ID '{game_id}' does not exist"}
            )
        GAMES.pop(game_id)
        res = {
            "game_id": game_id,
            "is_deleted": game_id not in GAMES,
        }
        logger.info(f"{res}")
        return JSONResponse(status_code=204, content={})

    except Exception as e:  # TODO: http error handler
        logger.error(f"Exception: {e}")
        return JSONResponse(
            status_code=400,
            content={"status": False, "detail": str(e)}
        )


@app.delete("/games")
def remove_games() -> JSONResponse:

    """ Remove all games instances in the cache """

    logger.info("Delete all games")
    try:
        [GAMES.pop(game) for game in GAMES.copy()]
        logger.info("all games deleted")
        return JSONResponse(status_code=204, content={})

    except Exception as e:  # TODO: http error handler
        logger.error(f"Exception: {e}")
        return JSONResponse(
            status_code=400,
            content={"status": False, "detail": str(e)}
        )
