from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from enum import IntEnum


class StatusCode(IntEnum):
    OK_200 = 200
    CREATED_201 = 201
    ALREADY_202 = 202
    NOT_FOUND_204 = 204
    BAD_REQUEST_400 = 400
    UNAUTHORIZED_401 = 401
    FORBIDDEN_403 = 403
    NOTFOUND_404 = 404
    CONFLICT_409 = 409
    BAD_GATEWAY_502 = 502


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
        if status_code == 400:
            self.detail = "User is not present in the database"


class DatabaseException(HTTPException):
    def __init__(self, status_code, details=None):
        self.status_code = status_code
        self.detail = details
        if self.status_code == 502:
            self.detail = "Error with the database"
        if self.status_code == 404:
            self.detail = "Deployment not found"
        if self.status_code == 403:
            self.detail = "No file found in the s3"
        if self.status_code == 204:
            self.detail = "No record found"
        if self.status_code == 202:
            self.detail = "Record already exists"


class FileException(HTTPException):
    def __init__(self, status_code=None, detail=None):
        self.status_code = StatusCode.NOTFOUND_404 if not status_code else status_code
        self.detail = "File not found!" if not detail else detail
        if self.status_code == 502:
            self.detail = "No index file found in the repo!"


class AWSExceptions(HTTPException):
    def __init__(self, status_code=None, detail=None):
        self.status_code = status_code
        self.detail = detail
        if self.status_code == 500:
            self.detail = "Failed to verify AWS credentials"


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

    @app.exception_handler(DatabaseException)
    async def database_exception_handler(request: Request, exc: DatabaseException):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )

    @app.exception_handler(FileException)
    async def file_exception_handler(request: Request, exc: FileException):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )

    @app.exception_handler(AWSExceptions)
    async def aws_creds_verify_handler(request: Request, exc: AWSExceptions):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )
