from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="routers/templates")


@router.get("/")
async def home(request: Request):
    return  templates.TemplateResponse("index.html", context={"request": request})
