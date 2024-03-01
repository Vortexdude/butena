from datetime import datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from .service import UserService
from .schema import TokenPayload
from pydantic import ValidationError
from app.settings import conf
from app.exceptions import JWTException, StatusCode

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl=f"/api/{conf.API_VERSION}/auth/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reusable_oauth)):
    try:
        payload = jwt.decode(
            token, conf.JWT_SECRET_KEY, algorithms=[conf.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise JWTException(status_code=StatusCode.UNAUTHORIZED_401)

    except (jwt.JWTError, ValidationError):
        raise JWTException(status_code=StatusCode.FORBIDDEN_403)

    user = await UserService.find_by_id(str(token_data.sub))   # specify the string type

    if not user:
        raise JWTException(status_code=StatusCode.NOTFOUND_404)

    user_dict = {key: value for key, value in user.__dict__.items() if
                 key not in ['enabled', 'created_at', 'hashed_password', 'id']}

    return user_dict
