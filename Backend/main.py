from fastapi import FastAPI

from domain.entities import User
from infrastructure.database import engine
from routers import auth, rooms
from use_cases.exception_handlers import exception_container

app = FastAPI()

app.include_router(auth.router)
app.include_router(rooms.router)

User.Base.metadata.create_all(bind=engine)

exception_container(app)