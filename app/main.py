from fastapi import FastAPI

from domain.entities import User
from infrastructure.database import engine
from routers import auth, rooms, public
from use_cases.exception_handlers import exception_container
# from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
routers = [auth.router,rooms.router, public.router]
for router in routers:
    app.include_router(router)
# # app.add_middleware(
# #  CORSMiddleware,
# #  allow_origins=["http://localhost:3000"], # Add your frontend origin here
# #  allow_credentials=True,
# #  allow_methods=["*"],
# #  allow_headers=["*"],
# #  )

User.Base.metadata.create_all(bind=engine)

exception_container(app)
