from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
import logging

from services.utils import COMMANDS, create_html
from models.items import GameInfo, ErrorMessage, RobotInfo
from models.setting import get_app_settings
from services.play import create_game, move_robot
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
    return RedirectResponse("/docs")


@app.post("/games/start", responses={400: {"model": ErrorMessage}})
def start_game(item: GameInfo) -> JSONResponse:
    dim, robots, dinosaurs = item.grid_dim, item.robots, item.dinosaurs
    if dim <= 2:
        return JSONResponse(
            status_code=400,
            content={"status": False, "detail": "You must create a bigger grid"}
        )

    match: Game = create_game(dim, robots_count=robots, dinosaurs_count=dinosaurs)
    GAMES[str(match.game_id)] = match

    logger.info("The Game has begun")

    res = {
        "game_id": match.game_id,
        "grid": f"{match.dim}*{match.dim}",
        "dinosaurs": len(match.dinosaurs_position),
        "dinosaurs_position": match.dinosaurs_position,
        "robots": len(match.robots_position),
        "robots_position": match.robots_position,
    }

    logger.info(f"{res}")
    return JSONResponse(res)


@app.get("/games/display/{game_id}")
def display_game(game_id: str) -> HTMLResponse:
    game = GAMES[game_id]
    html = create_html(game_id, game.get_board(), game.dim)
    return HTMLResponse(content=html, status_code=200)


@app.put("/games/play/{game_id}", responses={400: {"model": ErrorMessage}})
async def play_robots(game_id: str, item: RobotInfo) -> JSONResponse:
    try:
        game: Game = GAMES[game_id]
        chose_robot = str(item.robot_id)
        command = COMMANDS[item.command % len(COMMANDS)]
    except ZeroDivisionError:
        return JSONResponse(
            status_code=400,
            content={"status": False, "detail": "Invalid game id, you must correct id or create a new game"}
        )

    if item.command not in range(5):
        return JSONResponse(
            status_code=400,
            content={
                "status": False,
                "detail": "You must insert the correct instructions as following \
                0 -> forward, 1 -> backward, 2 -> right, 3 -> left, 4 -> attack"
            }
        )

    if not chose_robot:
        chose_robot = list(game.robots.keys())[0]

    try:
        await move_robot(game, chose_robot, command)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"status": False, "detail": str(e)}
        )
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
    return JSONResponse(res)


@app.delete("/games/delete/{game_id}")
def remove_game(game_id: str) -> JSONResponse:
    try:
        game: Game = GAMES[game_id]
        game.delete_game()
    except ZeroDivisionError:
        return JSONResponse(
            status_code=400,
            content={"status": False, "detail": "Invalid game id, you must correct id or create a new game"}
        )

    res = {
        "game_id": game_id,
        "is_deleted": not bool(game.get_board())
    }
    logger.info(f"{res}")
    return JSONResponse(res)
