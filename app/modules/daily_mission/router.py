from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.daily_mission import service
from app.modules.daily_mission.schemas import (
    AttendanceResponse,
    CheckInRequest,
    DailyTaskResponse,
    TodayMissionResponse,
)
from app.modules.learning.schemas import TaskResponse

router = APIRouter(prefix="/daily-missions", tags=["daily-mission"])


@router.post("/check-in", response_model=AttendanceResponse, status_code=201)
def check_in(payload: CheckInRequest, db: Session = Depends(get_db)):
    return service.check_in(db, payload.user_id)


@router.get("/today", response_model=TodayMissionResponse)
def today(user_id: int, db: Session = Depends(get_db)):
    attendance, rows = service.get_today(db, user_id)
    tasks = [
        DailyTaskResponse(
            id=item.id,
            task_order=item.task_order,
            is_completed=item.is_completed,
            task=TaskResponse.model_validate(task),
        )
        for item, task in rows
    ]
    return TodayMissionResponse(attendance=attendance, tasks=tasks)


@router.patch("/tasks/{item_id}/complete")
def complete(item_id: int, user_id: int, db: Session = Depends(get_db)):
    item = service.complete_task(db, user_id, item_id)
    return {"id": item.id, "is_completed": item.is_completed}
