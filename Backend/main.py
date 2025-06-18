from fastapi import FastAPI

from database import engine
from domain.entities import User
from routers import auth, rooms

app = FastAPI()

app.include_router(auth.router)
app.include_router(rooms.router)

User.Base.metadata.create_all(bind=engine)

