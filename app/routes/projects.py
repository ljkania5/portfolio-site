from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.core import templates

router = APIRouter()


@router.get("/projects", response_class=HTMLResponse)
async def projects(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="projects.html")