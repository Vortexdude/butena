from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from enum import IntEnum


class StatusCode(IntEnum):
    OK_200 = 200
    CREATED_201 = 201
    BAD_REQUEST_400 = 400
    UNAUTHORIZED_401 = 401
    FORBIDDEN_403 = 403
    NOTFOUND_404 = 404
    CONFLICT_409 = 409


class JWTException(HTTPException):
    def __init__(self, status_code, details=None):
        self.status_code = status_code
        self.detail = details
        self.headers = {"WWW-Authenticate": "Bearer"}
        if status_code == 401:
            self.detail = "Token expired"
        if status_code == 403:
            self.detail = "Could not validate credentials"
        if status_code == 404:
            self.detail = "Could not find user"


class UserException(HTTPException):
    def __init__(self, status_code, details=None):
        self.status_code = status_code
        self.detail = details
        if status_code == 409:
            self.detail = "User already present in the database"
        if status_code == 404:
            self.detail = "Incorrect email or password"


def init_exceptions(app: FastAPI):
    @app.exception_handler(UserException)
    async def user_exception_handler(request: Request, exc: UserException):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )

    @app.exception_handler(JWTException)
    async def jwt_exception_handler(request: Request, exc: JWTException):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,
            headers=exc.headers
        )
