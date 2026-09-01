from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import Attendance, AttendanceTask, Task, User


def check_in(db: Session, user_id: int):
    if db.get(User, user_id) is None:
        raise HTTPException(404, "User not found")
    attendance = Attendance(user_id=user_id, check_in_date=datetime.now().astimezone().date())
    db.add(attendance)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Already checked in today") from None
    db.refresh(attendance)
    return attendance


def get_today(db: Session, user_id: int):
    today = datetime.now().astimezone().date()
    attendance = db.scalar(
        select(Attendance).where(Attendance.user_id == user_id, Attendance.check_in_date == today)
    )
    if attendance is None:
        raise HTTPException(404, "No check-in for today")
    rows = db.execute(
        select(AttendanceTask, Task)
        .join(Task)
        .where(AttendanceTask.attendance_id == attendance.id)
        .order_by(AttendanceTask.task_order)
    ).all()
    return attendance, rows


def complete_task(db: Session, user_id: int, item_id: int):
    item = db.scalar(
        select(AttendanceTask)
        .join(Attendance)
        .where(AttendanceTask.id == item_id, Attendance.user_id == user_id)
        .with_for_update()
    )
    if item is None:
        raise HTTPException(404, "Daily mission task not found")
    item.is_completed = True
    db.commit()
    db.refresh(item)
    return item
