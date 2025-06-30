from fastapi import APIRouter
from starlette.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="routers/templates")


@router.get("/spectate/{room_id}")
async def spectate(room_id: int):
    return f"You are spectating room {room_id}"


@router.get("/host/{room_id}")
async def video_feed(room_id: int):
    return f"You are hosting room {room_id}"
