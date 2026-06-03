import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Read the connection string from the environment (set in docker-compose.yml).
# The fallback lets the app still start if the var is somehow missing.
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    f"postgresql://portfolio_user:{os.getenv('DB_PASSWORD')}@db:5432/portfolio_db",
)

# The engine manages the pool of actual connections to Postgres.
engine = create_engine(DATABASE_URL)

# A session factory — each request gets its own short-lived session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Every model inherits from this. SQLAlchemy uses it to track table definitions.
class Base(DeclarativeBase):
    pass


# FastAPI dependency: hands a session to a route, guarantees it's closed after.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()