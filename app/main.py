from fastapi import FastAPI

from domain.entities import User
from infrastructure.database import engine
from routers import auth, rooms, public
from use_cases.exception_handlers import exception_container

app = FastAPI()
routers = [auth.router,rooms.router, public.router]
for router in routers:
    app.include_router(router)

User.Base.metadata.create_all(bind=engine)

exception_container(app)
