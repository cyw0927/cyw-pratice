from pydantic import BaseModel, Field

from app.modules.learning.schemas import TaskResponse


class RoomCreate(BaseModel):
    host_user_id: int
    title: str = Field(min_length=1, max_length=200)
    max_participants: int = Field(ge=1)
    task_ids: list[int] = Field(min_length=1)


class JoinRequest(BaseModel):
    user_id: int


class ReadyRequest(BaseModel):
    user_id: int
    is_ready: bool


class RoomResponse(BaseModel):
    id: int
    host_user_id: int
    title: str
    status: str
    max_participants: int
    participant_count: int


class RoomTaskResponse(BaseModel):
    id: int
    task_order: int
    task: TaskResponse
