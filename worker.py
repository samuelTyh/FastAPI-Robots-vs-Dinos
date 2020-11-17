from fastapi import FastAPI
from fastapi.responses import JSONResponse


from utils import COMMANDS
from items import GameInfo, ErrorMessage, RobotInfo
from play import create_game, move_robot


# Caching the games by id
GAMES = {}

app = FastAPI(
    title="Robots vs Dinosaurs",
    description="A service that provides a REST API to support simulating an army \
                of remote-controlled robots to fight the dinosaurs",
    version="0.0.1"
)


@app.get("/")
def read_root():
    res = {"app_name": "Robots vs Dinosaurs", "version": app.version}
    return JSONResponse(res)


@app.post("/games/start", responses={400: {"model": ErrorMessage}})
def start_game(item: GameInfo):
    dim, robots, dinosaurs = item.grid_dim, item.robots, item.dinosaurs
    if dim <= 2:
        return JSONResponse(
            status_code=400,
            content={"status": False, "detail": "You must create a bigger grid"}
        )

    match = create_game(dim, robots_count=robots, dinosaurs_count=dinosaurs)
    GAMES[str(match.id)] = match

    res = {
        "game_id": match.id,
        "grid": f"{match.dim}*{match.dim}",
        "dinosaurs": len(match.dinosaurs_position),
        "dinosaurs_position": match.dinosaurs_position,
        "robots": len(match.robots_position),
        "robots_position": match.robots_position,
    }
    return JSONResponse(res)


@app.put("/games/play/{game_id}", responses={400: {"model": ErrorMessage}})
def play_robots(game_id: str, item: RobotInfo):
    game = GAMES[game_id]
    robot_id_list = list(game.robots.keys())
    chose_robot = robot_id_list[item.robot_id % len(robot_id_list)]
    command = COMMANDS[item.command % len(COMMANDS)]

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
        chose_robot = robot_id_list[0]

    try:
        move_robot(game, chose_robot, command)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"status": False, "detail": str(e)}
        )
    res = {
        "robot_id": chose_robot,
        "command": command,
        "new_position": game.robots[chose_robot],
        "dinosaurs": len(game.dinosaurs_position),
        "dinosaurs_position": game.dinosaurs_position,
        "all_dinosaurs_has_been_terminated": not bool(game.dinosaurs_position),
    }
    return JSONResponse(res)
