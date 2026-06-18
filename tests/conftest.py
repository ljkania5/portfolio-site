"""Shared pytest fixtures and test configuration.

`app.database` reads ``DATABASE_URL`` from the environment *at import time* and
builds the SQLAlchemy engine immediately. So we must set it here, at module
import, before any ``app.*`` module is imported by a test.

We force a throwaway SQLite file (never ``setdefault``) so the suite can never
accidentally connect to — and drop tables on — a real Postgres database that
happens to be configured in the developer's shell.
"""

import atexit
import contextlib
import os
import tempfile

import pytest

# A temp file (not ``:memory:``) so every connection in the pool sees the same
# data: the lifespan seed and the request handlers use separate connections.
_db_fd, _db_path = tempfile.mkstemp(suffix=".db")
os.close(_db_fd)
os.environ["DATABASE_URL"] = f"sqlite:///{_db_path}"


@atexit.register
def _cleanup_tmp_db() -> None:
    with contextlib.suppress(OSError):
        os.unlink(_db_path)


@pytest.fixture
def clean_db():
    """Drop and recreate all tables so each test starts from an empty schema."""
    from app.database import Base, engine

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(clean_db):
    """A SQLAlchemy session against a freshly created, empty schema."""
    from app.database import SessionLocal

    with SessionLocal() as session:
        yield session


@pytest.fixture
def client():
    """A TestClient that runs the app lifespan (so tables are created + seeded).

    Used as a context manager, Starlette's TestClient triggers startup/shutdown
    events, which is what invokes ``init_db()``.
    """
    from fastapi.testclient import TestClient

    from app.database import Base, engine
    from app.main import app

    # Start from a known-empty schema so the seed runs deterministically.
    Base.metadata.drop_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)
