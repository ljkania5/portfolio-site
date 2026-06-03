from app.database import Base, SessionLocal, engine
from app.models import Project

# Mirrors what was hardcoded in projects.html.
INITIAL_PROJECTS = [
    {
        "title": "This Website",
        "description": (
            "A self-referential project: a portfolio site built with FastAPI, "
            "containerized with Docker, deployed on AWS using Terraform, and "
            "continuously deployed via GitHub Actions."
        ),
        "tech": "FastAPI · PostgreSQL · Docker · Terraform · AWS",
    },
    {
        "title": "Coming soon",
        "description": "More projects will land here as I build them.",
        "tech": None,
    },
]


def init_db():
    # Create tables for any models that don't exist yet.
    Base.metadata.create_all(bind=engine)

    # Seed only when the table is empty, so restarts don't create duplicates.
    db = SessionLocal()
    try:
        if db.query(Project).count() == 0:
            db.add_all(Project(**data) for data in INITIAL_PROJECTS)
            db.commit()
    finally:
        db.close()