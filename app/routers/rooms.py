from fastapi import APIRouter, Depends, HTTPException
from starlette.templating import Jinja2Templates
from .auth import get_current_user
from typing import Annotated

router = APIRouter()
templates = Jinja2Templates(directory="routers/templates")
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/spectate/{room_id}")
async def spectate(user: user_dependency, room_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return f"You are spectating room {room_id}"


@router.get("/host/{room_id}")
async def video_feed(room_id: int):
    return f"You are hosting room {room_id}"
