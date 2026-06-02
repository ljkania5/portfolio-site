from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core import BASE_DIR
from app.routes import home, projects, resume

app = FastAPI()

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Plug each router into the app.
app.include_router(home.router)
app.include_router(projects.router)
app.include_router(resume.router)

# Health stays here — it's an infrastructure endpoint, not a page.
@app.get("/health")
async def health():
    return {"status": "healthy"}