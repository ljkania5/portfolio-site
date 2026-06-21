from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core import BASE_DIR
from app.routes import home, projects, resume
from app.seed import init_db


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    # Runs once when the app starts: create tables + seed data.
    init_db()
    yield
    # (Nothing to tear down on shutdown yet.)


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(home.router)
app.include_router(projects.router)
app.include_router(resume.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}
