from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from infrastructure.database import get_db
from domain.entities.User import User
from use_cases.exceptions import EntityNotFoundError
from starlette import status


router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency):
    return db.query(User).all()


@router.get("/users/{id}", status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency, user_id: int = Path(gt=0)):
    model = db.query(User).filter(user_id == User.id).first()
    if model is not None:
        return model
    raise EntityNotFoundError(user_id)
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
