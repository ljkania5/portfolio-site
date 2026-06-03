from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core import templates
from app.database import get_db
from app.models import Project

router = APIRouter()


@router.get("/projects", response_class=HTMLResponse)
async def projects(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    project_list = db.query(Project).order_by(Project.id).all()
    return templates.TemplateResponse(
        request=request,
        name="projects.html",
        context={"projects": project_list},
    )