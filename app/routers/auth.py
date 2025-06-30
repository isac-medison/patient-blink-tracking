from typing import Annotated
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from domain.entities.User import User
from domain.entities.UserRequest import UserRequest
from use_cases.exceptions import EntityNotFoundError
from starlette import status
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

SECRET_KEY = "ab72194801799663e57274591797d1cc6375e2ee021c93c1da4b7dba1e019786"
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

db_dependency = Annotated[Session, Depends(get_db)]

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency):
    return db.query(User).all()


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency, user_id: int = Path(gt=0)):
    model = db.query(User).filter(User.id == user_id).first()
    if model is not None:
        return model
    raise EntityNotFoundError(user_id)


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def post_user(db: db_dependency, user_request: UserRequest):
    new_user = User(
        username=user_request.username,
        is_admin=user_request.is_admin,
        password_hash=bcrypt_context.hash(user_request.password),
    )
    db.add(new_user)
    db.commit()


@router.put("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(
    db: db_dependency, user_request: UserRequest, user_id: int = Path(gt=0)
):
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model is None:
        raise EntityNotFoundError(user_id)
    user_model.username = user_request.username
    user_model.is_admin = user_request.is_admin

    db.add(user_model)
    db.commit()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: db_dependency, user_id: int = Path(gt=0)):
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model is None:
        raise EntityNotFoundError(user_id)
    user_model.deleted_at = datetime.now(timezone.utc)

    db.add(user_model)
    db.commit()


@router.post("/token", status_code=status.HTTP_200_OK)
async def get_users(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return token


@router.delete("/logout", status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency):
    return "logout"


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password_hash):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {
        "sub": username,
        "id": user_id,
        "exp": datetime.now(timezone.utc) + expires_delta
    }
    token =  jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


