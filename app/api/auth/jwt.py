from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any
from fastapi.security import OAuth2PasswordRequestForm
from .service import UserService
from lib.utils import JWT

auth_router = APIRouter()


@auth_router.post("/login", summary="Create access Token and Refresh Token")
async def create_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    return {
        "access_token": JWT.create_access_token(str(user.user_id)),
        "refresh_token": JWT.create_refresh_token(user.user_id),
    }

