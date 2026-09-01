from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.battle import service
from app.modules.battle.schemas import (
    JoinRequest,
    ReadyRequest,
    RoomCreate,
    RoomResponse,
    RoomTaskResponse,
)
from app.modules.learning.schemas import TaskResponse

router = APIRouter(prefix="/battle/rooms", tags=["battle"])


def response(room, count):
    return RoomResponse(
        id=room.id,
        host_user_id=room.host_user_id,
        title=room.title,
        status=room.status,
        max_participants=room.max_participants,
        participant_count=count,
    )


@router.post("", response_model=RoomResponse, status_code=201)
def create(payload: RoomCreate, db: Session = Depends(get_db)):
    return response(service.create_room(db, payload), 1)


@router.get("", response_model=list[RoomResponse])
def rooms(db: Session = Depends(get_db)):
    return [response(room, count) for room, count in service.list_rooms(db)]


@router.get("/{room_id}", response_model=RoomResponse)
def detail(room_id: int, db: Session = Depends(get_db)):
    return response(*service.get_room(db, room_id))


@router.post("/{room_id}/participants", status_code=201)
def join(room_id: int, payload: JoinRequest, db: Session = Depends(get_db)):
    item = service.join_room(db, room_id, payload.user_id)
    return {"id": item.id, "user_id": item.user_id, "is_ready": item.is_ready}


@router.patch("/{room_id}/ready")
def ready(room_id: int, payload: ReadyRequest, db: Session = Depends(get_db)):
    item = service.set_ready(db, room_id, payload.user_id, payload.is_ready)
    return {"user_id": item.user_id, "is_ready": item.is_ready}


@router.get("/{room_id}/tasks", response_model=list[RoomTaskResponse])
def tasks(room_id: int, db: Session = Depends(get_db)):
    return [
        RoomTaskResponse(
            id=item.id, task_order=item.task_order, task=TaskResponse.model_validate(task)
        )
        for item, task in service.room_tasks(db, room_id)
    ]
