# from pydantic import BaseModel, Field
# from datetime import datetime, UTC
# from typing import Optional
    # def __init__(self, id, username, is_admin, deleted_at):
    #     self.id = id
    #     self.username = username
    #     self.is_admin = is_admin
    #     self.deleted_at = deleted_at

#
# class UserDTO(BaseModel):
#     id: Optional[int] = None
#     title: str = Field(min_length=3, max_length=100)
#     description: Optional[str] = Field(min_length=3, max_length=100)
#     is_admin: Optional[bool] = False
#     deleted_at: Optional[datetime] = None
#
#     model_config = {
#         "json_schema_extra": {
#             "example": {
#                 "id": 1,
#                 "title": "A title for user",
#                 "description": "Short description of user",
#                 "is_admin": False
#             }
#         }
#     }
