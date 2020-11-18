from typing import Optional
from pydantic import BaseModel


class GameInfo(BaseModel):
    grid_dim: int = 50
    robots: Optional[int] = None
    dinosaurs: Optional[int] = None


class ErrorMessage(BaseModel):
    status: bool
    detail: str


class RobotInfo(BaseModel):
    robot_id: Optional[int] = 0
    command: int
