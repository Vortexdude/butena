import uuid
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class UserBase(BaseModel):
    email: str = Field(..., description="User Email")
    username: str = Field(..., min_length=5, max_length=20, description="User username")
    password: str = Field(..., min_length=5, max_length=24, description="User password")


class UserCreation(UserBase):
    user_id: Optional[str] = uuid.uuid4()
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "Nitin",
                    "last_name": "Namdev",
                    "email": "nnamdev@google.com",
                    "username": 'nnamdev',
                    "password": "Nothingspecial"
                }
            ]
        }
    }

class UserAuth(BaseModel):
    email: str = Field(..., description="User Email")
    username: str = Field(..., min_length=5, max_length=20, description="User username")
    password: str = Field(..., min_length=5, max_length=24, description="User password")


class UserOut(BaseModel):
    user_id: UUID
    user_name: Optional[str]
    enabled: bool


class TokenPayload(BaseModel):
    sub: UUID = None
    exp: int = None

class UserUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
