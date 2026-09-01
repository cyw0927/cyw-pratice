from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(100), unique=True)


class Concept(Base):
    __tablename__ = "concepts"
    name: Mapped[str] = mapped_column(String(200), unique=True)
    description: Mapped[str | None] = mapped_column(Text)


class Task(Base):
    __tablename__ = "tasks"
    concept_id: Mapped[int] = mapped_column(ForeignKey("concepts.id"))
    title: Mapped[str] = mapped_column(String(200))
    type: Mapped[str] = mapped_column(String(30))
    difficulty: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(Text)
    template_code: Mapped[str] = mapped_column(Text)
    test_cases: Mapped[str] = mapped_column(Text)
    hint_text: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Attendance(Base):
    __tablename__ = "attendances"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    check_in_date: Mapped[date] = mapped_column(Date)
    __table_args__ = (UniqueConstraint("user_id", "check_in_date", name="uq_attendance_day"),)


class AttendanceTask(Base):
    __tablename__ = "attendance_tasks"
    attendance_id: Mapped[int] = mapped_column(ForeignKey("attendances.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    task_order: Mapped[int] = mapped_column(Integer)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    __table_args__ = (
        UniqueConstraint("attendance_id", "task_id", name="uq_attendance_task"),
        UniqueConstraint("attendance_id", "task_order", name="uq_attendance_order"),
        UniqueConstraint("id", "task_id", name="uq_attendance_task_id_task_id"),
        CheckConstraint("task_order > 0", name="ck_attendance_order_positive"),
    )


class Room(Base):
    __tablename__ = "rooms"
    host_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(20), default="WAITING")
    max_participants: Mapped[int] = mapped_column(Integer)
    __table_args__ = (CheckConstraint("max_participants > 0", name="ck_room_capacity"),)


class RoomParticipant(Base):
    __tablename__ = "room_participants"
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_ready: Mapped[bool] = mapped_column(Boolean, default=False)
    __table_args__ = (UniqueConstraint("room_id", "user_id", name="uq_room_user"),)


class RoomTask(Base):
    __tablename__ = "room_tasks"
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    task_order: Mapped[int] = mapped_column(Integer)
    __table_args__ = (
        UniqueConstraint("room_id", "task_id", name="uq_room_task"),
        UniqueConstraint("room_id", "task_order", name="uq_room_order"),
        UniqueConstraint("id", "task_id", name="uq_room_task_id_task_id"),
    )


class TaskAttempt(Base):
    __tablename__ = "task_attempts"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    attendance_task_id: Mapped[int | None] = mapped_column(Integer)
    room_task_id: Mapped[int | None] = mapped_column(Integer)
    context_type: Mapped[str] = mapped_column(String(20))
    submitted_code: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="PENDING")
    is_correct: Mapped[bool | None] = mapped_column(Boolean)
    attempted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    __table_args__ = (
        ForeignKeyConstraint(
            ["attendance_task_id", "task_id"], ["attendance_tasks.id", "attendance_tasks.task_id"]
        ),
        ForeignKeyConstraint(["room_task_id", "task_id"], ["room_tasks.id", "room_tasks.task_id"]),
        CheckConstraint(
            "(context_type = 'LEARNING' AND attendance_task_id IS NULL AND room_task_id IS NULL) OR "
            "(context_type = 'DAILY' AND attendance_task_id IS NOT NULL AND room_task_id IS NULL) OR "
            "(context_type = 'BATTLE' AND attendance_task_id IS NULL AND room_task_id IS NOT NULL)",
            name="ck_attempt_context",
        ),
    )
