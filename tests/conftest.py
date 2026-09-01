import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.models import Concept, Task, User
from app.db.session import get_db
from app.main import create_app


@pytest.fixture()
def db():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, expire_on_commit=False)()
    session.add_all([User(username="host"), User(username="guest")])
    concept = Concept(name="Variables", description="Variable basics")
    session.add(concept)
    session.flush()
    session.add(
        Task(
            concept_id=concept.id,
            title="Add two numbers",
            type="CODE",
            difficulty="EASY",
            description="Return a + b",
            template_code="def add(a, b): ...",
            test_cases='[{"input": [1, 2], "output": 3}]',
            hint_text="Use +",
        )
    )
    session.commit()
    yield session
    session.close()


@pytest.fixture()
def client(db):
    app = create_app()
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as test_client:
        yield test_client
