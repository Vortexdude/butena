from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class UserAuth(BaseModel):
    email: str = Field(..., description="User Email")
    username: str = Field(..., min_length=5,max_length=20, description="User username")
    password: str = Field(..., min_length=5,max_length=24, description="User password")


class UserOut(BaseModel):
    user_id: UUID
    username: str
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    disabled: Optional[bool] = False


class UserUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
