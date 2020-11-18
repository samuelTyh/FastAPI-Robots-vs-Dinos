from typing import Optional, List, Dict
from pydantic import BaseModel


class GamePayload(BaseModel):
    grid_dim: int = 50
    robots_count: Optional[int] = None
    robots: Optional[List[tuple]] = []
    dinosaurs_count: Optional[int] = None
    dinosaurs: Optional[List[tuple]] = []


class RobotPayload(BaseModel):
    robot_id: Optional[int] = 0
    command: int


class StartResponse(BaseModel):
    game_id: str
    grid: str
    dinosaurs: int
    dinosaurs_position: List[tuple]
    robots: int
    robots_position: List[tuple]


class PlayResponse(BaseModel):
    game_id: str
    robot_id: str
    command: int
    new_position: Dict[tuple, str]
    dinosaurs: int
    dinosaurs_position: List[tuple]
    number_of_moves: int
    all_dinosaurs_has_been_terminated: bool


class ErrorMessage(BaseModel):
    status: bool
    detail: str
