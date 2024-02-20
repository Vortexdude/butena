from beanie import Document, Indexed
from datetime import datetime
from pydantic import Field, BaseModel
from uuid import UUID, uuid4
from typing import Optional


class UserBase(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    email: Indexed(str, unique=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_name: Optional[str] = None
    hashed_password: str
    enabled: Optional[bool] = True

    def __init__(self, **data):
        data['user_name'] = f"{data['first_name'][0]}.{data['last_name']}".lower()
        super().__init__(**data)


class User(Document, UserBase):

    def __repr__(self) -> str:
        return f"<USER  {self.email}>"

    def __str__(self):
        return self.email

    @property
    def create(self) -> datetime:
        return self.id.generation_time

    class Settings:
        name = "Users"
