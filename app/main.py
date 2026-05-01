from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")


@app.get("/projects", response_class=HTMLResponse)
async def projects(request: Request):
    return templates.TemplateResponse(request=request, name="projects.html")


@app.get("/resume", response_class=HTMLResponse)
async def resume(request: Request):
    return templates.TemplateResponse(request=request, name="resume.html")

@app.get("/health")
async def health():
    return {"status": "healthy"}