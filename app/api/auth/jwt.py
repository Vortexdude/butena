from fastapi import APIRouter, Depends
from typing import Any
from fastapi.security import OAuth2PasswordRequestForm
from .service import UserService
from app.core.utils import JWT
from app.exceptions import UserException, StatusCode

auth_router = APIRouter()


@auth_router.post("/login", summary="Create access Token and Refresh Token")
async def create_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise UserException(status_code=StatusCode.NOTFOUND_404)

    return {
        "access_token": JWT.create_access_token(str(user.user_id)),
        "refresh_token": JWT.create_refresh_token(user.user_id),
    }
