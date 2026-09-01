from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import Room, RoomParticipant, RoomTask, Task, User
from app.modules.battle.schemas import RoomCreate


def room_or_404(db: Session, room_id: int, lock: bool = False):
    query = select(Room).where(Room.id == room_id)
    room = db.scalar(query.with_for_update() if lock else query)
    if room is None:
        raise HTTPException(404, "Room not found")
    return room


def create_room(db: Session, payload: RoomCreate):
    if db.get(User, payload.host_user_id) is None:
        raise HTTPException(404, "Host user not found")
    if len(set(payload.task_ids)) != len(payload.task_ids):
        raise HTTPException(422, "task_ids must be unique")
    tasks = list(
        db.scalars(select(Task).where(Task.id.in_(payload.task_ids), Task.is_active.is_(True)))
    )
    if len(tasks) != len(payload.task_ids):
        raise HTTPException(422, "Unknown or inactive task")
    room = Room(
        host_user_id=payload.host_user_id,
        title=payload.title,
        max_participants=payload.max_participants,
    )
    db.add(room)
    db.flush()
    db.add(RoomParticipant(room_id=room.id, user_id=payload.host_user_id))
    db.add_all(
        [
            RoomTask(room_id=room.id, task_id=task_id, task_order=order)
            for order, task_id in enumerate(payload.task_ids, 1)
        ]
    )
    db.commit()
    db.refresh(room)
    return room


def list_rooms(db: Session):
    return db.execute(
        select(Room, func.count(RoomParticipant.id))
        .outerjoin(RoomParticipant)
        .group_by(Room.id)
        .order_by(Room.id)
    ).all()


def get_room(db: Session, room_id: int):
    room = room_or_404(db, room_id)
    count = db.scalar(
        select(func.count(RoomParticipant.id)).where(RoomParticipant.room_id == room_id)
    )
    return room, count or 0


def join_room(db: Session, room_id: int, user_id: int):
    if db.get(User, user_id) is None:
        raise HTTPException(404, "User not found")
    room = room_or_404(db, room_id, lock=True)
    if room.status != "WAITING":
        raise HTTPException(409, "Room is not accepting participants")
    count = db.scalar(
        select(func.count(RoomParticipant.id)).where(RoomParticipant.room_id == room_id)
    )
    if (count or 0) >= room.max_participants:
        raise HTTPException(409, "Room is full")
    participant = RoomParticipant(room_id=room_id, user_id=user_id)
    db.add(participant)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "User already joined") from None
    db.refresh(participant)
    return participant


def set_ready(db: Session, room_id: int, user_id: int, is_ready: bool):
    participant = db.scalar(
        select(RoomParticipant).where(
            RoomParticipant.room_id == room_id, RoomParticipant.user_id == user_id
        )
    )
    if participant is None:
        raise HTTPException(404, "Participant not found")
    participant.is_ready = is_ready
    db.commit()
    db.refresh(participant)
    return participant


def room_tasks(db: Session, room_id: int):
    room_or_404(db, room_id)
    return db.execute(
        select(RoomTask, Task)
        .join(Task)
        .where(RoomTask.room_id == room_id)
        .order_by(RoomTask.task_order)
    ).all()
