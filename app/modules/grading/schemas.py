from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AttemptCreate(BaseModel):
    user_id: int
    task_id: int
    context_type: Literal["LEARNING", "DAILY", "BATTLE"]
    submitted_code: str = Field(min_length=1)
    attendance_task_id: int | None = None
    room_task_id: int | None = None

    @model_validator(mode="after")
    def validate_context(self):
        expected = {"LEARNING": (False, False), "DAILY": (True, False), "BATTLE": (False, True)}[
            self.context_type
        ]
        actual = (self.attendance_task_id is not None, self.room_task_id is not None)
        if actual != expected:
            raise ValueError("Context must match attendance_task_id/room_task_id")
        return self


class AttemptResponse(BaseModel):
    id: int
    user_id: int
    task_id: int
    context_type: str
    submitted_code: str
    status: str
    is_correct: bool | None
    attempted_at: datetime
    model_config = ConfigDict(from_attributes=True)
