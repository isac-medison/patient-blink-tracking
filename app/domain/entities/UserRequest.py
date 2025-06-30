from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    username : str = Field(min_length=3, max_length=100)
    is_admin : bool
    password: str