"""Tests for the database seeding logic in app.seed."""

from sqlalchemy import func, select

from app.models import Project
from app.seed import INITIAL_PROJECTS, init_db


def test_init_db_creates_and_seeds(db_session):
    # clean_db (via db_session) dropped the tables; init_db should recreate and
    # populate them.
    init_db()

    count = db_session.scalar(select(func.count(Project.id)))
    assert count == len(INITIAL_PROJECTS)

    titles = set(db_session.scalars(select(Project.title)).all())
    assert titles == {"This Website", "Coming soon"}


def test_init_db_is_idempotent(db_session):
    init_db()
    init_db()  # second call must not duplicate the seed rows

    count = db_session.scalar(select(func.count(Project.id)))
    assert count == len(INITIAL_PROJECTS)


def test_init_db_does_not_seed_when_table_non_empty(db_session):
    # Pre-existing data means the seed should be skipped entirely.
    db_session.add(Project(title="Pre-existing", description="already here"))
    db_session.commit()

    init_db()

    count = db_session.scalar(select(func.count(Project.id)))
    assert count == 1
    only = db_session.scalar(select(Project))
    assert only.title == "Pre-existing"


def test_seeded_tech_values_match_definition(db_session):
    init_db()
    by_title = {p.title: p for p in db_session.scalars(select(Project)).all()}

    assert by_title["This Website"].tech is not None
    assert by_title["Coming soon"].tech is None
