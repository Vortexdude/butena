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


async def get_current_user(token: str = Depends(reusable_oauth)) -> dict:
    """
    Dependency to get the current user based on the provided JWT token.

    Args:
        token (str): JWT token obtained during user authentication.

    Returns:
        dict: Dictionary containing user details excluding sensitive information.

    Raises:
        HTTPException: Raises appropriate HTTP exceptions for JWT decoding errors and user not found.

    Note:
        This function should be used as a dependency to extract user information from JWT tokens.
    """
    try:
        # Decode JWT token and validate its payload
        payload = jwt.decode(token, conf.JWT_SECRET_KEY, algorithms=[conf.ALGORITHM])
        token_data = TokenPayload(**payload)
        # Check if the token is expired
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise JWTException(status_code=StatusCode.UNAUTHORIZED_401)

    except (jwt.JWTError, ValidationError):
        raise JWTException(status_code=StatusCode.FORBIDDEN_403)

    # Retrieve user information from the database based on user ID from the token
    user = await UserService.find_by_id(str(token_data.sub))

    # If user not found, raise an exception
    if not user:
        raise JWTException(status_code=StatusCode.NOTFOUND_404)

    # Exclude sensitive information from the user dictionary
    user_dict = {key: value for key, value in user.__dict__.items() if key not in ['enabled', 'created_at', 'hashed_password', 'id']}

    return user_dict

# Example of using the get_current_user dependency in a route:
# @app.get("/protected-route")
# async def protected_route(current_user: dict = Depends(get_current_user)):
#     return {"message": "This route is protected", "user": current_user}
