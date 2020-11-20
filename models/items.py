from typing import Optional, List, Dict
from pydantic import BaseModel


class GamePayload(BaseModel):

    """ The data model for starting games """

    grid_dim: int = 50
    robots_count: Optional[int] = None
    robots: List[Dict] = []
    dinosaurs_count: Optional[int] = None
    dinosaurs: Optional[List[tuple]] = []


class RobotPayload(BaseModel):

    """ The data model for operating robots """

    robot_id: Optional[int] = 0
    command: int


class StartResponse(BaseModel):

    """ The response model of starting games """

    game_id: str
    grid: str
    dinosaurs: int
    dinosaurs_position: List[tuple]
    robots: int
    robots_position: List[Dict]


class PlayResponse(BaseModel):

    """ The response model of operating robots """

    game_id: str
    robot_id: int
    command: int
    new_position: Dict[tuple, str]
    dinosaurs: int
    dinosaurs_position: List[tuple]
    number_of_moves: int
    all_dinosaurs_has_been_terminated: bool


class ErrorMessage(BaseModel):

    """ The response model of error """

    status: bool
    detail: str


class DeletionMessage(BaseModel):

    """ The response model of deletion """

    game_id: str
    is_deleted: bool
