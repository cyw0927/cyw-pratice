from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.grading import service
from app.modules.grading.schemas import AttemptCreate, AttemptResponse

router = APIRouter(prefix="/grading/attempts", tags=["grading-stub"])


@router.post("", response_model=AttemptResponse, status_code=202)
def submit(payload: AttemptCreate, db: Session = Depends(get_db)):
    return service.submit(db, payload)


@router.get("", response_model=list[AttemptResponse])
def attempts(user_id: int, db: Session = Depends(get_db)):
    return service.list_attempts(db, user_id)


@router.get("/{attempt_id}", response_model=AttemptResponse)
def detail(attempt_id: int, user_id: int, db: Session = Depends(get_db)):
    return service.get_attempt(db, attempt_id, user_id)
