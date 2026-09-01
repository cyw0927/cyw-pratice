from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.session import engine

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database tables created.")
