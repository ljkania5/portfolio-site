"""Tests for the Project ORM model: schema, persistence, and nullability."""

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models import Project


def test_tablename():
    assert Project.__tablename__ == "projects"


def test_persist_and_read_back(db_session):
    project = Project(
        title="Test Project",
        description="A description.",
        tech="Python · pytest",
    )
    db_session.add(project)
    db_session.commit()

    fetched = db_session.scalar(select(Project).where(Project.title == "Test Project"))
    assert fetched is not None
    assert fetched.id is not None  # autoincrement primary key assigned
    assert fetched.description == "A description."
    assert fetched.tech == "Python · pytest"


def test_tech_is_optional(db_session):
    project = Project(title="No Tech", description="No tech listed.")
    db_session.add(project)
    db_session.commit()

    fetched = db_session.scalar(select(Project).where(Project.title == "No Tech"))
    assert fetched.tech is None


def test_title_is_required(db_session):
    # title is a non-nullable column; committing without it must fail.
    db_session.add(Project(description="Missing a title."))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_description_is_required(db_session):
    db_session.add(Project(title="Missing description"))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
