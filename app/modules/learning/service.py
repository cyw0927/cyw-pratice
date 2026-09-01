from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Concept, Task


def list_concepts(db: Session):
    return list(db.scalars(select(Concept).order_by(Concept.id)))


def list_tasks(db: Session, concept_id: int):
    if db.get(Concept, concept_id) is None:
        raise HTTPException(404, "Concept not found")
    return list(
        db.scalars(
            select(Task)
            .where(Task.concept_id == concept_id, Task.is_active.is_(True))
            .order_by(Task.id)
        )
    )


def get_task(db: Session, task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id, Task.is_active.is_(True)))
    if task is None:
        raise HTTPException(404, "Task not found")
    return task
