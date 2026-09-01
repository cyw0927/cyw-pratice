from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import (
    Attendance,
    AttendanceTask,
    RoomParticipant,
    RoomTask,
    Task,
    TaskAttempt,
    User,
)
from app.modules.grading.schemas import AttemptCreate


def submit(db: Session, payload: AttemptCreate):
    if db.get(User, payload.user_id) is None:
        raise HTTPException(404, "User not found")
    if db.get(Task, payload.task_id) is None:
        raise HTTPException(404, "Task not found")
    valid = True
    if payload.context_type == "DAILY":
        valid = db.scalar(
            select(AttendanceTask)
            .join(Attendance)
            .where(
                AttendanceTask.id == payload.attendance_task_id,
                AttendanceTask.task_id == payload.task_id,
                Attendance.user_id == payload.user_id,
            )
        )
    elif payload.context_type == "BATTLE":
        valid = db.scalar(
            select(RoomTask)
            .join(RoomParticipant, RoomParticipant.room_id == RoomTask.room_id)
            .where(
                RoomTask.id == payload.room_task_id,
                RoomTask.task_id == payload.task_id,
                RoomParticipant.user_id == payload.user_id,
            )
        )
    if not valid:
        raise HTTPException(422, "Invalid attempt context")
    attempt = TaskAttempt(**payload.model_dump(), status="PENDING", is_correct=None)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


def list_attempts(db: Session, user_id: int):
    return list(
        db.scalars(
            select(TaskAttempt)
            .where(TaskAttempt.user_id == user_id)
            .order_by(TaskAttempt.id.desc())
        )
    )


def get_attempt(db: Session, attempt_id: int, user_id: int):
    attempt = db.scalar(
        select(TaskAttempt).where(TaskAttempt.id == attempt_id, TaskAttempt.user_id == user_id)
    )
    if attempt is None:
        raise HTTPException(404, "Attempt not found")
    return attempt
