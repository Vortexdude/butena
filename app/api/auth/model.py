from beanie import Document, Indexed
from datetime import datetime
from pydantic import Field
from uuid import UUID, uuid4
from typing import Optional


class User(Document):
    user_id: UUID = Field(default_factory=uuid4)
    email: Indexed(str, unique=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    hashed_password: str
    disabled: Optional[bool] = None

    def __repr__(self) -> str:
        return f"<USER  {self.email}>"

    def __str__(self):
        return self.email

    @property
    def create(self) -> datetime:
        return self.id.generation_time

    class Settings:
        name = "Users"
