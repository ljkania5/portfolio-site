from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.core import templates

router = APIRouter()


@router.get("/resume", response_class=HTMLResponse)
async def resume(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="resume.html")