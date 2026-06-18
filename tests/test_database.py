"""Tests for the database wiring in app.database."""

import contextlib
import subprocess
import sys

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db


def _exhaust(gen):
    """Advance a one-shot dependency generator past its single yield, which
    runs the `with SessionLocal()` exit and closes the session."""
    with contextlib.suppress(StopIteration):
        next(gen)


def test_get_db_yields_usable_session():
    gen = get_db()
    session = next(gen)
    try:
        assert isinstance(session, Session)
        # The session is bound and can execute against the configured engine.
        assert session.scalar(text("SELECT 1")) == 1
    finally:
        _exhaust(gen)


def test_get_db_closes_session_after_use():
    gen = get_db()
    session = next(gen)
    _exhaust(gen)  # triggers SessionLocal context manager __exit__
    # A closed session has no active transaction / connection bound.
    assert not session.in_transaction()


def test_missing_database_url_raises_at_import():
    """app.database fails fast with a clear error when DATABASE_URL is unset."""
    code = "import app.database"
    proc = subprocess.run(
        [sys.executable, "-c", code],
        env={"PATH": ""},  # deliberately strip DATABASE_URL from the environment
        capture_output=True,
        text=True,
    )
    assert proc.returncode != 0
    assert "DATABASE_URL" in proc.stderr
