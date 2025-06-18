from datetime import datetime, UTC
from typing import Annotated

from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from database import get_db
from domain.entities import User

# from models import User, UserDTO

router = APIRouter()


@router.get("/users")
async def get_users(db: Annotated[Session, Depends(get_db)]):
    return db.query(User.User).all()


# @router.get("/users/{id}")
# async def get_users(user_id: int):
#     for user in USERS:
#         if user.id == user_id:
#             return user
#     return None
#
#
# @router.post("/users", status_code=HTTP_201_CREATED)
# async def post_user(user: UserDTO):
#     new_user = User(**user.model_dump())
#     USERS.append(set_user_id(new_user))
#
#
# @router.put("/users", status_code=HTTP_204_NO_CONTENT)
# async def update_user(user: UserDTO):
#     for i in range(len(USERS)):
#         if USERS[i].id == user.id:
#             USERS[i] = User(**user.model_dump())
#
#
# @router.delete("/users/{user_id}", status_code=HTTP_204_NO_CONTENT)
# async def update_user(user_id: int = Path(gt=0)):
#     for i in range(len(USERS)):
#         if USERS[i].id == user_id:
#             USERS[i].deleted_at = datetime.now(UTC)
#
#
# def set_user_id(user):
#     if len(USERS) > 0:
#         user.id = USERS[-1].id + 1
#     else:
#         user.id = 1
#     return user
