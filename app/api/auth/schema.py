import uuid
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class UserBase(BaseModel):
    email: str = Field(..., description="User Email")
    user_name: str = Field(..., min_length=5, max_length=20, description="User username")
    password: str = Field(..., min_length=5, max_length=24, description="User password")


class UserCreation(UserBase):
    user_id: Optional[str] = str(uuid.uuid4())
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        orm_mod = True
        json_schema_extra = {
            "examples": [
                {
                    "first_name": "Nitin",
                    "last_name": "Namdev",
                    "email": "nnamdev@google.com",
                    "user_name": 'nnamdev',
                    "password": "Nothingspecial"
                }
            ]
        }


class TokenPayload(BaseModel):
    sub: UUID = None
    exp: int = None
