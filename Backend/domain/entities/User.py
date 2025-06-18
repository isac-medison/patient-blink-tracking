from sqlalchemy import Column, String, Boolean, DATETIME, Integer
from infrastructure.database import Base


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(16))
    is_admin = Column(Boolean, default=False)
    password_hash = Column(String(16))
    deleted_at = Column(DATETIME, nullable=True)