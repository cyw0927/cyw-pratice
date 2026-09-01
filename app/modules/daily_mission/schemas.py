from datetime import date

from pydantic import BaseModel, ConfigDict

from app.modules.learning.schemas import TaskResponse


class CheckInRequest(BaseModel):
    user_id: int


class AttendanceResponse(BaseModel):
    id: int
    user_id: int
    check_in_date: date
    model_config = ConfigDict(from_attributes=True)


class DailyTaskResponse(BaseModel):
    id: int
    task_order: int
    is_completed: bool
    task: TaskResponse


class TodayMissionResponse(BaseModel):
    attendance: AttendanceResponse
    tasks: list[DailyTaskResponse]
