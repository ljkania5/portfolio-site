from pathlib import Path

from fastapi.templating import Jinja2Templates

# This file lives in app/, so parent is the app/ directory.
BASE_DIR = Path(__file__).resolve().parent

# Single shared templates object that every route file imports.
templates = Jinja2Templates(directory=BASE_DIR / "templates")
