from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.learning import service
from app.modules.learning.schemas import ConceptResponse, TaskResponse

router = APIRouter(prefix="/learning", tags=["learning"])


@router.get("/concepts", response_model=list[ConceptResponse])
def concepts(db: Session = Depends(get_db)):
    return service.list_concepts(db)


@router.get("/concepts/{concept_id}/tasks", response_model=list[TaskResponse])
def concept_tasks(concept_id: int, db: Session = Depends(get_db)):
    return service.list_tasks(db, concept_id)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def task_detail(task_id: int, db: Session = Depends(get_db)):
    return service.get_task(db, task_id)
