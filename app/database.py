import os
from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Fail fast with a clear error if DATABASE_URL isn't set.
DATABASE_URL = os.environ["DATABASE_URL"]

# The engine manages the pool of actual connections to Postgres.
engine = create_engine(DATABASE_URL)

# A session factory — each request gets its own short-lived session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Every model inherits from this. SQLAlchemy uses it to track table definitions.
class Base(DeclarativeBase):
    pass


# FastAPI dependency: hands a session to a route, guarantees it's closed after.
def get_db() -> Iterator[Session]:
    with SessionLocal() as db:
        yield db
