from fastapi import APIRouter

router = APIRouter()


@router.get("/rooms")
async def get_rooms():
    return "hello"


@router.get("/spectate/{room_id}")
async def spectate(room_id: int):
    return f"room {room_id}"
